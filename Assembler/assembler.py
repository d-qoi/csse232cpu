import re
class Assembler:

    debug = False
    progStart = 0
    program = []

    binaryMapInst = {'and':0x0, 
                'orr':0x1,'or':0x1,
                'xor':0x2,
                'not':0x3,
                'tsc':0x4,
                'slt':0x5,
                'sgt':0x6,
                'sll':0x7,
                'srl':0x8,
                'sra':0x9,
                'add':0xA,
                'sub':0xB,
                'cpy':0xF,
                'beq':0x2,
                'bne':0x3,
                'bgt':0x4,
                'blt':0x5,
                'jr':0x6,
                'r':0x7,
                'w':0x8,
                'rsh':0xE,
                'sudo':0xF}

    binaryMapRegs = {'$0':0x0,'$00':0x0,'$z0':0x0,'$zz':0x0, '$zero':0x0,
                    '$a0':0x1,
                    '$a1':0x2,
                    '$pc':0x3,
                    '$sp':0x4,
                    '$ra':0x5,
                    '$s0':0x6,
                    '$s1':0x7,
                    '$t0':0x8,
                    '$t1':0x9,
                    '$t2':0xA,
                    '$t3':0xB,
                    '$h0':0xC,
                    '$h1':0xD,
                    '$h2':0xE,
                    '$h3':0xF}


    ATypeList = {'add','sub','slt','sgt','sll','srl','sra','and','orr','or',
                'xor','not','tsc','cpy'}

    BTypeList = {'beq','bnq','bne','bgt','blt','r','w'}
    HTypeList = {'rsh','sudo'}
    JTypeList = {'jr'}


    PseudoList = {'jal','j','psh','pop'} # Please update and see the method pseudoExpandHelper

    WarningList = {'$at','$at1','$pc'}
    Warnings = []
    Symbols = []

##"""
##Layout of the program
##
##This will create a program list that will be formatted in the following way
##
##    [[inst],asm,sym(if any)]
##    inst will be 'const' if it is a constant, update asm immediatly
##
##[inst] will be layed out in the following way:
##    ['ops','arg1',...] or ['imm']
##    If any of the args are a symbol, leave them as the symbol
##    any offsets are to be left as integers.
##
##
##asm will be formatted in the following way:
##    ['0xFFFF'] untill otherwise noted
##    IT IS A STRING
##
##    formatted with '0x%04x'
##
##sym:
##    Will be left as empty list if there is none.
##    otherwise is the symbol until that appears on the line.
##
##
##expected use cases of Symbols:
##
##    Branches, the symbol is a 4bit offset, this is unsigned,
##        If the symbol offset is larger than 16, the branch is converted to a jump,
##    jumps, the symbol is an 8 bit offset, this is signed
##        If the symbol is to big, or small, the jump is converted to a direct jump
##
##    constant the symbol is the line number * 2 plus the program start offset
##        This is a result of a jump being converted to a big jump.
##
##"""

    def __init__(self, progStart):
        #import re
        self.progStart = progStart


    def checkInst(self, inst):
        if not inst[0] in self.binaryMapInst.keys()|self.PseudoList:
            raise Exception('Instruction not in instructions', inst[0])
        for i in inst:
            if '$' in i and not i in self.binaryMapRegs:
                raise Exception('Register not real',i,'at line',len(self.program),'in',inst)
            elif '$' in i and i in self.WarningList:
                self.Warnings.append("Manipulating {0} on line {1} @ {2}".format(i,len(self.program), inst))
                # the line wasn't added yet so len and not len-1

    def readFile(self, inPath):
        # This cannot be a file read in, it must be a list to pass
        with open(inPath, 'r') as prog:
            sym = ''
            nextLine = [[],'','']
            for instruction in prog: #should read to EOF

                instruction = instruction.strip().lower()

                if instruction is '': #empty line?
                    continue

                if '#' in instruction: #cutting out comments
                    instruction = instruction[0:instruction.index('#')] 

                inst = re.split('[\s,\(\)]',instruction)
                inst = [x for x in inst if x]
                # I don't like this line, but it is shorter than alternatives
                # This line trims the list into specific values

                if not len(inst): #empty line, would break below
                    continue
                if ':' in inst[0] and len(inst):
                    nextLine[2] = inst[0].strip()[0:-1]
                    if nextLine[2] in self.Symbols:
                        self.Warnings.append("symbol %s is refrenced more than once."%nextLine[2])
                    else:
                        self.Symbols.append(nextLine[2])
                    inst = inst[1:] #remove the symbol
                    if not len(inst): #empty line, would break below
                        continue

                self.checkInst(inst)

                nextLine[0] = inst

                self.program.append(nextLine) 
                nextLine = [[],'','']
                # append program to inst

                if self.debug:
                    print(self.program[-1])

    # will take instructions ordered as [inst1, inst2, inst3] where inst1 is a line of assembly
    def createNextLine(self, instructionSet):
        nextLine = [[],'','']
        out = []
        for instruction in instructionSet:
            instruction = instruction.strip().lower()

            if instruction is '': #empty line?
                continue

            if '#' in instruction: #cutting out comments
                instruction = instruction[0:instruction.index('#')] 

            inst = re.split('[\s,\(\)]',instruction)
            inst = [x for x in inst if x]
            # I don't like this line, but it is shorter than alternatives
            # This line trims the list into specific values

            if not len(inst): #empty line, would break below
                continue
            if ':' in inst[0] and len(inst):
                nextLine[2] = inst[0].strip()[0:-1]

                inst = inst[1:] #remove the symbol
                if not len(inst): #empty line, would break below
                    continue

            #self.checkInst(inst) Not necessary in assembler create lines

            nextLine[0] = inst

            out.append(nextLine) 
            nextLine = [[],'','']

        return out


    def pseudoExpandHelper(self, inst, pos):
        # New way to handle these
        # just make sure it is a string, seperate things by new lines
        # check below for examples, it workes rather well 
        # use formatting and % to insert things into the strings, examples shown below
        if self.debug:
            print(inst,'=>')
        if 'j' in inst:
            out = 'jr $pc %s'%inst[1]

        elif 'jal' in inst:
            out = '''cpy $ra 2
            add $ra $pc
            jr $pc %s'''%inst[1] # this has been changed, I am jumping 2 lines, this is not shifted that is handled in hardware

        elif 'psh' in inst:
            out = '''sub $sp 1
            w 0($sp) %s'''%inst[1] # this is now -1 from -2, because blocks and this should be shifted to help

        elif 'pop' in inst:
            out = '''r %s 0($sp)
            add $sp 1'''%inst[1] # this is not +1 from +2, see above

        self.program.pop(pos)
        out = self.createNextLine(out.split('\n'))
        if self.debug:
            print(out)
        out.reverse() # to be inserted backwards for simple for loop
        for i in out:
            self.program.insert(pos,i)
        

    def expandPseudoInst(self):
        programCounter = 0;
        while programCounter < len(self.program): #really important that this is not a for loop
            if self.program[programCounter][0][0] in self.PseudoList:
                self.pseudoExpandHelper(self.program[programCounter][0], programCounter)

            # for adding the immediates after the add, Probably don't need to do this here, but I am regardkess because idk, why not?
            if self.program[programCounter][0][0] in self.ATypeList:
                if not self.program[programCounter][0][2] in self.binaryMapRegs or len(self.program[programCounter][0]) is 4:
                    imm = int(self.program[programCounter][0][-1])
                    # this is adding in the immediate lines, this should be the case for ALL immeadiates that are passed to the assembler by the programmer.
                    self.program.insert(programCounter+1,[['imm'],'0x%04x'%imm,''])

            programCounter += 1 # Still not missing this


    def createTempSymbolDict(self):
        out = {}
        for line in range(0,len(self.program)):
            sym = self.program[line][2]
            if sym: #pulling the immediate, if there is one, add it
                out[sym] = line
        return out

    def branchToJump(self, line):
        oldLine = self.program[line]
        if self.debug:
            print(oldLine[0], 'became:')
        jump = [['jr','$pc',oldLine[0][3]],'','']
        oldLine[0][3] = '1'
        if oldLine[0][0] == 'beq':
            oldLine[0][0] = 'bne'
        elif oldLine[0][0] == 'bne':
            oldLine[0][0] = 'beq'
        elif oldLine[0][0] == 'bgt':
            oldLine[0][0] = 'blt'
        elif oldLine[0][0] == 'blt':
            oldLine[0][0] = 'bgt'
        self.program.insert(line+1,jump)
        
        if self.debug:
            print(self.program[line],'\n',self.program[line+1])

    def jumpToBigJump(self, line):
        oldLine = self.program[line]
        sym = str(oldLine[0][2])
        if self.debug:
            print("converting %s to and sym %s:"%(oldLine[0],sym))
        # updating branches
        if (line > 1 and
            self.program[line-1][0][0] in {'beq','bne','bgt','blt'} and
            self.program[line-1][0][3] == '1'):

            self.program[line-1][0][3] = '2'
        # updating jal
        elif (line > 3 and
            self.program[line-3][0] == ['cpy','$ra','2'] and
            self.program[line-1][0] == ['add','$ra','$pc']):

            self.program[line-3][0] = ['cpy','$ra','3'] #should this is now 3 lines, rather than 2, may need to change
            self.program[line-2][1] = '0x0003'

        self.program.insert(line,[['imm'],sym,'']) #inserting the target for the Copy
        if self.debug:
            print(self.program[line], 'adding new immediate')
        self.program.insert(line,[['cpy','$a1','0'],'','']) # 0 to make sure it loads the immediate
        oldLine[0] = ['jr','$a1','0']
        
        if self.debug and line > 3:
            print(self.program[line-3],self.program[line-2],self.program[line-1], self.program[line])

    def getSymOffset(self, sym, programCounter, symDict):
        return symDict[sym] - programCounter - 1


    # this is not assembling the code, it is just making sure symbols line up.
    def convert(self):
        programCounter = 0
        changeCount = 0 #did anything change, will loop this till this remains zero
        symDict = self.createTempSymbolDict()

       
        while programCounter < len(self.program):
            line = self.program[programCounter] 
            #skipping things that don't change
            # ALU codes, sudo, rsh, and r and w
            if line[0][0] in self.ATypeList|self.HTypeList|{'r','w'}:
                programCounter += 1
                continue
        # Branching and jumping remain
            # branching and is there actually a symbol
            if line[0][0] in self.BTypeList and line[0][3] in symDict: 
                offset = self.getSymOffset(line[0][3], programCounter, symDict)
                if offset > 15 or offset < 0:
                    changeCount += 1
                    self.branchToJump(programCounter)

            # jump and jumbol checking
            elif line[0][0] in self.JTypeList and len(line[0]) > 2 and line[0][2] in symDict:
                offset = self.getSymOffset(line[0][2], programCounter, symDict)
                if offset > 127 or offset < -128:
                    changeCount += 1
                    self.jumpToBigJump(programCounter)                

            programCounter += 1

        return changeCount

    def AType(self, line):
        inst = self.program[line][0]
        if len(inst[0]) == 3:
            if '$' in inst[1] and '$' in inst[2] and len(inst) == 3:
                self.program[line][1] = ('0x' + hex(0)[2:] +
                                        hex(self.binaryMapRegs[inst[1]])[2:] +
                                        hex(self.binaryMapRegs[inst[2]])[2:] + 
                                        hex(self.binaryMapInst[inst[0]])[2:])
            else:
                self.program[line][1] = ('0x' + hex(1)[2:] +
                                        hex(self.binaryMapRegs[inst[1]])[2:] +
                                        hex(self.binaryMapRegs['$0'])[2:] + 
                                        hex(self.binaryMapInst[inst[0]])[2:])
        else:
            self.program[line][1] = ('0x' + hex(1)[2:] +
                                    hex(self.binaryMapRegs[inst[1]])[2:] +
                                    hex(self.binaryMapRegs[inst[2]])[2:] + 
                                    hex(self.binaryMapInst[inst[0]])[2:])

    def BType(self, line, symDict):
        inst = self.program[line][0]
        #read 
        # r d o(s)
        # r d s o

        # write
        # w o(d) s
        # w d s o
        if inst[0] == 'r':
            self.program[line][1] = ('0x' + 
                                    hex(self.binaryMapInst[inst[0]])[2:] + # inst 0
                                    hex(self.binaryMapRegs[inst[1]])[2:] + # dest 1
                                    hex(self.binaryMapRegs[inst[3]])[2:] + # source 3
                                    hex(int(inst[2]))[2:])                 # offset 2
                                    
        elif inst[0] == 'w':
            self.program[line][1] = ('0x' + 
                                    hex(self.binaryMapInst[inst[0]])[2:] + # inst 0
                                    hex(self.binaryMapRegs[inst[2]])[2:] + # dest 2
                                    hex(self.binaryMapRegs[inst[3]])[2:] + # source 3
                                    hex(int(inst[1]))[2:])                 # offset 1
        
        elif inst[3] in symDict:
            self.program[line][1] = ('0x' + 
                                    hex(self.binaryMapInst[inst[0]])[2:] +
                                    hex(self.binaryMapRegs[inst[1]])[2:] +
                                    hex(self.binaryMapRegs[inst[2]])[2:] +
                                    hex(self.getSymOffset(inst[3],line, symDict))[2:])

        else:
            self.program[line][1] = ('0x' + 
                                    hex(self.binaryMapInst[inst[0]])[2:] +
                                    hex(self.binaryMapRegs[inst[1]])[2:] +
                                    hex(self.binaryMapRegs[inst[2]])[2:] +
                                    hex(int(inst[3]))[2:])

    def HType(self, line):
        inst = self.program[line][0]
        self.program[line][1] = ('0x' + 
                                hex(self.binaryMapInst[inst[0]])[2:] + 
                                '00' +
                                hex(int(inst[1]))[2:])

    def JType(self,line, symDict):
        inst = self.program[line][0]
        if len(inst) == 2:
            self.program[line][1] = ('0x' + 
                                    hex(self.binaryMapInst[inst[0]])[2:] +
                                    hex(self.binaryMapRegs[inst[1]])[2:] + 
                                    '00')
        else:
            if inst[2] in symDict:
                offset = hex(self.getSymOffset(inst[2],line, symDict) & 0xFF)[2:]
                offset = '0'*(2-len(offset))+offset
            else:
                offset = '00'
            self.program[line][1] = ('0x' +
                                    hex(self.binaryMapInst[inst[0]])[2:] +
                                    hex(self.binaryMapRegs[inst[1]])[2:] +
                                    offset)

    def assemble(self):
        symDict = self.createTempSymbolDict()
        programCounter = 0;
        while programCounter < len(self.program):
            if self.debug:
                temp = self.program[programCounter]
            if self.program[programCounter][0][0] in self.ATypeList:
                self.AType(programCounter)
            elif self.program[programCounter][0][0] in self.BTypeList:
                self.BType(programCounter,symDict)
            elif self.program[programCounter][0][0] in self.HTypeList:
                self.HType(programCounter)
            elif self.program[programCounter][0][0] in self.JTypeList:
                self.JType(programCounter,symDict)
            elif self.program[programCounter][0][0] == 'imm':
                if self.program[programCounter][1] in symDict:
                    self.program[programCounter][1] = '0x%04x'%(symDict[self.program[programCounter][1]] + self.progStart)
            if self.debug:
                print(self.program[programCounter])
            programCounter += 1

    def printAsm(self,outFile):
        with open(outFile, 'w') as dest:
            for line in self.program:
                dest.write(line[1])
                dest.write('\n')

    def debugPrintAll(self):
        for line in self.program:
            print(line)
            
    def run(self,inFile,outFile):
        self.readFile(inFile)
        self.expandPseudoInst()
        #self.debugPrintAll()
        while self.convert() != 0:
            pass
        self.assemble()
        self.printAsm(outFile)
        for line in self.Warnings:
            print(line)


if __name__ == '__main__':
    import sys

    helpPrint = """

The use of this program:
assembler infile.asm <outfile.bin> <Program Start offset> <debug>
-h or help:     Prints this message

if the outfile is not specified, it will write to out.bin
if 'debug'(all lower) is passed anywhere, it will toggle debugging mode

if an integer is passed, it will offset the program counter so that all direct jumps
are recorded accurately, it defaults to 4096 or 0x1000

Version 2.00

"""

    if '-h' in sys.argv or 'help' in sys.argv:
        print(helpPrint) 
        sys.exit(0)

    #sys.argv = ["SimplePrograms\SIMPLEPROCEDURES.asm" ,"SimplePrograms\out\SIMPLEPROCEDURES.bin", "4096","debug"]
    #sys.argv = ['Tests.asm','debug']
    
    inFile = ''
    outFile = 'out.bin'
    asm = Assembler(4096)
    if 'debug' in sys.argv:
        asm.debug = True
    for arg in sys.argv:
        if '.asm' in arg:
            inFile = arg
        elif '.bin' in arg:
            outFile = arg
        elif arg.isdigit(): #don't ask questions
            asm.progStart = int(arg)

    if inFile is '':
        print(helpPrint)
        sys.exit(0)
    
    asm.run(inFile, outFile)
