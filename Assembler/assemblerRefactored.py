import re
class Assembler:

    debug = False
    progStart = 0
    symOff = -1 #Trust me it works
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
        progStart = 0
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

            self.checkInst(inst)

            nextLine[0] = inst

            out.append(nextLine) 
            nextLine = [[],'','']

        return out


    def pseudoExpandHelper(self, inst, pos):
        if self.debug:
            print(inst,'=>')
        if 'j' in inst:
            out = 'jr $pc %s'%inst[1]

        elif 'jal' in inst:
            out = '''cpy $ra 6
            add $ra $pc
            jr $pc %s'''%inst[1]

        elif 'psh' in inst:
            out = '''sum $sp 2
            w 0($sp) %s'''%inst[1]

        elif 'pop' in inst:
            out = '''r %s 0($sp)
            add $sp 2'''%inst[1]

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



            if self.program[programCounter][0][0] in self.ATypeList:
                if not self.program[programCounter][0][2] in self.binaryMapRegs or len(self.program[programCounter][0]) is 4:
                    imm = int(self.program[programCounter][0][-1])
                    self.program.insert(programCounter+1,[['imm'],'0x%04x'%imm,''])


            programCounter += 1 # Still not missing this

    def debugPrintAll(self):
        for line in self.program:
            print(line)
            
    def run(self,inFile,outFile):
        self.readFile(inFile)
        self.expandPseudoInst()
        self.debugPrintAll()



if __name__ == '__main__':
    import sys

    #sys.argv = [sys.argv[0], "SimplePrograms\\SIMPLEPROCEDURES.asm","debug"]
    
    helpPrint = """

The use of this program:
assembler infile.asm <outfile.bin> <Program Start offset> <debug>
-h or help:     Prints this message

if the outfile is not specified, it will write to out.bin
if 'debug'(all lower) is passed anywhere, it will toggle debugging mode

if an integer is passed, it will offset the program counter so that all direct jumps
are recorded accurately

Version 1.04

"""

    if '-h' in sys.argv or 'help' in sys.argv:
        print(helpPrint) 
        sys.exit(0)

    sys.argv = ["SimplePrograms\SIMPLEPROCEDURES.asm" ,"SimplePrograms\out\SIMPLEPROCEDURES.bin", "4096","debug"]

    inFile = ''
    outFile = 'out.bin'
    asm = Assembler(0)
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
