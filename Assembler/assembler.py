import re

class Assembler:

    debug = False
    progStart = 0
    programCounter = 0
    symOff = -1 #Trust me it works
    program = []
    globalDef = {}
    symbolDef = {}

    binaryMapInst = {'and':0x0, 
                'orr':0x1,
                'xor':0x2,
                'not':0x3,
                'tsc':0x4,
                'slt':0x5,
                'sll':0x6,
                'srl':0x7,
                'sra':0x8,
                'add':0x9,
                'sub':0xA,
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


    ATypeList = {'add','adu','sub','slt','sll','srl','sra','and','orr','or',
                'xor','not','tsc','ldi','li','cpy'}

    BTypeList = {'beq','bnq','bne','bgt','blt','r','w'}
    HTypeList = {'rsh','sudo'}
    JTypeList = {'jr'}


    PseudoList = {'jal','j','psh','pop'} # Please update and see the method pseudoExpandHelper

    WarningList = {'$at','$at1','$pc'}
    Warnings = []

    def __init__(self, progStart):
        import re
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
            for instruction in prog: #should read to EOF
                #instruction = prog.readline().strip()
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
                    self.symbolDef[inst[0].strip()[0:-1]] = len(self.program) #add to the symbol
                    if self.debug:
                        print(self.symbolDef)
                    inst = inst[1:] #remove the symbol
                    if not len(inst): #empty line, would break below
                        continue

                #Checking for everything!
                self.checkInst(inst)

                self.program.append(inst) 
                # append program to inst
                #Appending the new line of asm to the end of the program, and reading from the program counter to update the program to contain the converted line
                # I am doing this to account for the fact that all pseudo instructions are going to make this code bigger
                # If I were to continue reading from the file, then things would go badly,
                # in this case, we can just append to the Program and let the following code take care of converting the extended program into binary/hex

                self.programCounter += 1
                #debugging
                if self.debug:
                    print(self.program[-1])
                    print(self.programCounter, str(len(self.program)))


    # for updating things after expanding with pseudo instructions
    def updateSymbols(self, line, offset):
        for sym, val in self.symbolDef.items():
            if val > line:
                self.symbolDef[sym] += offset


    def assembleCurrentLine(self): # wish I had case statements
        if self.debug:
            temp = "{0} =>".format(self.program[self.programCounter])

        if self.program[self.programCounter][0] in self.ATypeList:
            self.AType(self.program[self.programCounter]) # ALU stuff
        elif self.program[self.programCounter][0] in self.BTypeList:
            self.BType(self.program[self.programCounter]) # Branch stuff
        elif self.program[self.programCounter][0] in self.HTypeList:
            self.HType(self.program[self.programCounter]) # sudo and schwap stuff
        elif self.program[self.programCounter][0] in self.JTypeList:
            self.JType(self.program[self.programCounter]) # jump stuff
        if self.debug:
            print(temp,self.program[self.programCounter])

    # if the branch is jumping more than 15 down or up, it must be inverted
    # and changed to a jump.
    def branchToJump(self, i):
        if self.debug:
            temp = self.program[i] #debugging var to see what was going on.
            print(temp,"became:")
        self.updateSymbols(i,1)
        sym = self.program[i][3]
        # jr $pc :sym
        jump = ['jr','$pc',sym] # trying PC relative first, changed below if needed
        self.program[i][3] = 1; 
        if self.program[i][0] == 'beq': # The Jumps need to be inverted
            self.program[i][0] = 'bne'
        elif self.program[i][0] == 'bne':
            self.program[i][0] = 'beq'
        elif self.program[i][0] == 'bgt':
            self.program[i][0] = 'blt'
        elif self.program[i][0] == 'blt':
            self.program[i][0] = 'bgt'
        self.program.insert(i+1,jump)

        if self.debug:
            print(self.program[i],'\n',self.program[i+1])

    # For converting jumps that are too big to the correct form
    # come up with better name later
    def jumpToBigJump(self, i):
        if self.debug:
            temp = self.program[i]
        sym = self.program[i][2]
        # updating branching and JAL code
        #branching
        # the binary map is because this has already been assembled
        if (i > 1 and
            self.program[i-1][0] in [self.binaryMapInst['beq'],
                                    self.binaryMapInst['bne'],
                                    self.binaryMapInst['bgt'],
                                    self.binaryMapInst['blt']] and 
            self.program[i-1][3] == 1):
            self.program[i-1][3] = 2
        #jumping
        # the hardcoding of numbers is because this is hard coded code
        # I like it less than you do
        elif (i > 3 and 
              self.program[i-3] == [0x1,0x5,0x0,0xf] and
              self.program[i-2] == '0x6' and
              self.program[i-1] == [0x0,0x5,0x3,0x9]):
            self.program[i-2] = '0x8' #woo magic number, this is because there is an added instruction

        offset = str(self.symbolDef[sym] + self.progStart) # This is the only place progStart comes into play
        if self.debug:
            print('jump to',sym,'being converted to big jump') # come up with better name 
        self.program.insert(i,['cpy','$a1',offset]) # this is not PC relative, so PC doesn't matter
        self.program[i+1] = ['jr','$a1','0']

        if self.debug:
            print(temp,"became:\n",self.program[i],'\n',self.program[i+1])

    # should be self explanitory, it is one line and debugging code
    def symToOffset(self, sym, line):
        if self.debug:
            print("creating offset from line",line,'to',self.symbolDef[sym],'for sym',sym)
            print('calculated as',self.symbolDef[sym] - line + self.symOff,'for', self.program[line])
        return self.symbolDef[sym] - line + self.symOff

    #two byte mostly for jumps
    # should refactor to string formatting sooner or later
    def toHexSigned(self, num):
        out = hex(num & 0xFF)[2:]
        if len(out) == 1:
            out = '0' + out
        if self.debug:
            print('converted',num,'to',hex(num & 0xFF)[2:])
        return out

    # one byte, mostly for branches
    # this is really silly
    def toHexUnsigned(self, num):
        if self.debug:
            print('converted',num,'to',hex(num)[2:])
        return hex(num)[2:]

    def expandSymbols(self):
        offset = 0 # instance variable, declaring early to let it be known
        if self.debug:
            print(self.symbolDef)
        self.programCounter = 0
        while self.programCounter < len(self.program): #for loops are constant don't hit end if the list changes
            if not isinstance(self.program[self.programCounter], list): # don't non lists pls
                self.programCounter += 1 #whoops
                continue
            # Branching l0gic
            if (self.program[self.programCounter][0] in ['beq','bne','bgt','blt'] and
                            self.program[self.programCounter][3] in self.symbolDef):
                offset = self.symToOffset(self.program[self.programCounter][3], self.programCounter)
                if offset > 15 or offset < 0: # unsigned 4 bit nibble
                    self.branchToJump(self.programCounter)
                else:
                    self.program[self.programCounter][3] = self.toHexUnsigned(offset)
            # Jumping logic
            elif (self.program[self.programCounter][0] in ['jr'] and
                  len(self.program[self.programCounter]) > 2 and  # if there is only a register, offset defaults to zero
                  self.program[self.programCounter][2] in self.symbolDef): #ignore if the offset is hard coded
                offset = self.symToOffset(self.program[self.programCounter][2], self.programCounter)
                if offset > 127 or offset < -128: #2^8 signed is 127 to -128
                    self.jumpToBigJump(self.programCounter)
                else:
                    self.program[self.programCounter][2] = self.toHexSigned(offset)


            self.assembleCurrentLine() # it works!

            self.programCounter += 1 #NOT MISSING woo!


    def pseudoExpandHelper(self, inst): #lesser Hacky bullshit
    # need to split things the way that the read in fuction does
    # split things that would be seperated by anything into seperate index
    # write example:
    # assembly: w 0($sp) $t0
    # list:     ['w','0','$sp','$t0']
    # sorry, all decoding was done on read in, deal with it
        if self.debug:
            print(inst,'=>')
        if 'j' in inst:
            out = [
                ['jr','$pc',inst[1]]]

        elif 'jal' in inst:
            out = [
                ['cpy','$ra','6'],
                ['add','$ra','$pc'],
                ['jr','$pc',inst[1]]]

        elif 'psh' in inst:
            out = [
                ['sub','$sp','2'],
                ['w','0','$sp',inst[1]]]

        elif 'pop' in inst:
            out = [
                ['r',inst[1],'0','$sp'],
                ['add','$sp','2']]

        if len(out) > 1: #updating all symbols comming later
            self.updateSymbols(self.programCounter, len(out)-1)

        self.program.pop(self.programCounter)
        out.reverse() # to be inserted backwards for simple for loop
        for i in out:
            self.program.insert(self.programCounter,i)
        #I can't believe that worked ^
        if self.debug:
            print(out)


    def expandPseudo(self): #I know the helper is longer than the actual function
        self.programCounter = 0;
        while self.programCounter < len(self.program): #really important that this is not a for loop
            if self.program[self.programCounter][0] in self.PseudoList:
                self.pseudoExpandHelper(self.program[self.programCounter])

            self.programCounter += 1 # Still not missing this


# Different types of instructions, may need to change later.
# If this is changed remember to change the list of instructions at the top
    def AType(self, inst):
        out = [0x0,'','','']
        if '$' in inst[1] and '$' in inst[2] and len(inst) is 3: # two registers
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out
        elif len(inst) is 3:
            out[0] = 0x1
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs['$zz']
            out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out
            if '0x' in inst[2]:
                self.program.insert(self.programCounter + 1, inst[2][2:])
            else:
                self.program.insert(self.programCounter + 1, hex(int(inst[2]) & 0xFFFF))
            self.programCounter += 1 #because I am inserting the immediate, the PC needs to be increased
            self.updateSymbols(self.programCounter, 1)
        else: # case for which we are loading an immediate into the second source on the same line
            out[0] = 0x1 
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out 
            if '0x' in inst[2]:
                self.program.insert(self.programCounter + 1, inst[2][2:])
            else:
                self.program.insert(self.programCounter + 1, hex(int(inst[3]) & 0xFFFF))
            self.programCounter += 1 # because I am inserting the PC, the immeadiate needs to be increased
            self.updateSymbols(self.programCounter, 1)

            #read 
            # r d o(s)
            # r d s o

            # write
            # w o(d) s
            # w d s o
    def BType(self, inst):
        out = ['','','','']
        if inst[0] in ['r','w']:
            out[0] = self.binaryMapInst[inst[0]]
            if inst[0] is 'r':
                out[1] = self.binaryMapRegs[inst[1]] #setting destination
                out[2] = self.binaryMapRegs[inst[3]] #setting source
                out[3] = inst[2]
            else:
                out[1] = self.binaryMapRegs[inst[3]] #setting dest
                out[2] = self.binaryMapRegs[inst[2]] #setting srouce
                out[3] = inst[1]
        else: #Handeling Branches
            out[0] = self.binaryMapInst[inst[0]]
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = inst[3]
        self.program[self.programCounter] = out

    def HType(self, inst):
        out = ['',0x0,0x0,'']
        out[0] = self.binaryMapInst[inst[0]]
        out[3] = (int(inst[1]))
        self.program[self.programCounter] = out

    def JType(self, inst):
        out = ['','','']
        if len(inst) is 2:
            inst = inst + ['0']
        out[0] = self.binaryMapInst[inst[0]]
        if '$' in inst[1]: 
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = inst[2]
        elif '$' in inst[2]:
            out[1] = self.binaryMapRegs[inst[2]]
            out[2] = inst[1]
        if len(out[2]) is 1:
                out[2] = '0' + out[2]
        self.program[self.programCounter] = out

    # can remove the '0x' later if needed
    def printAsm(self, outFile):
        with open(outFile, 'w') as dest:
#            dest.write("""Version 1.3
#
#
#""")
            for line in self.program:
                if not isinstance(line, str):
                    dest.write('0x')
                else:
                    if line.isdigit():
                        #dest.write(hex(int(line)))
                        dest.write('0x%04x'%int(line)) # formatting nicely
                    else:
                        dest.write('0x'+'0'*(4-len(line[2:]))+line[2:]); # no explination
                    dest.write('\n')
                    continue
                for inst in line:
                    if isinstance(inst, str):
                        dest.write(inst)
                    else:
                        dest.write(hex(inst)[2:])
                dest.write('\n')

    # this happens to work in this order and only this order.
    def run(self, inPath, outPath):
        self.readFile(inPath)
        self.expandPseudo()
        self.expandSymbols()
        self.printAsm(outPath)
        if len(self.Warnings):
            print("Warnings:")
            for i in self.Warnings:
                print(i)


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

Version 1.03

"""

    if '-h' in sys.argv or 'help' in sys.argv:
        print(helpPrint) 
        sys.exit(0)

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
