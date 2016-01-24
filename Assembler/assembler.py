import re

class Assembler:

    debug = False
    progStart = 0
    programCounter = 0
    symOff = -1 #I am not sure how much to offset the symbols, this will be the thing to change
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
    #RTypeList = {'r','w'}
    #STypeList = {'sudo'}


    PseudoList = {'jal','j','psh','pop'} # Please update and see the method

    def __init__(self, progStart):
        import re
        progStart = 0
        self.progStart = progStart

    def checkInst(self, inst):
        if not inst[0] in self.binaryMapInst.keys()|self.PseudoList:
            raise Exception('Instruction not in instructions', inst[0])
        for i in inst:
            if '$' in i and not i in self.binaryMapRegs:
                raise Exception('Register not real',i)


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

                #inst = [x for x in [item for item in instruction.split()] if x] #Brilliant!
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
                    print(self.program)
                    print(self.programCounter, str(len(self.program)))


    # for updating things after expanding with pseudo instructions
    def updateSymbols(self, line, offset):
        for sym, val in self.symbolDef.items():
            if val > line:
                self.symbolDef[sym] += offset


    def assemble(self):
        self.programCounter = 0
        while self.programCounter < len(self.program):
            if self.debug:
                temp = "{0} =>".format(self.program[self.programCounter])
            if self.program[self.programCounter][0] in self.ATypeList:
                self.AType(self.program[self.programCounter])
            elif self.program[self.programCounter][0] in self.BTypeList:
                self.BType(self.program[self.programCounter])
            elif self.program[self.programCounter][0] in self.HTypeList:
                self.HType(self.program[self.programCounter])
            elif self.program[self.programCounter][0] in self.JTypeList:
                self.JType(self.program[self.programCounter])
#           elif self.program[self.programCounter][0] in self.RTypeList:
#               self.RType(self.program[self.programCounter])
#           elif self.program[self.programCounter][0] in self.STypeList:
#                self.SType(self.program[self.programCounter])
#            elif self.program[self.programCounter][0] in self.PseudoList: #sudo instruction expansion
#                self.pseudoExpand(self.program[self.programCounter])
#                if self.debug:
#                    print(self.program[-3:],self.program[self.programCounter-1])
            if self.debug:
                print(temp,self.program[self.programCounter])
            self.programCounter += 1
            

    def assembleCurrentLine(self):
        if self.debug:
            temp = "{0} =>".format(self.program[self.programCounter])
            if self.program[self.programCounter][0] in self.ATypeList:
                self.AType(self.program[self.programCounter])
            elif self.program[self.programCounter][0] in self.BTypeList:
                self.BType(self.program[self.programCounter])
            elif self.program[self.programCounter][0] in self.HTypeList:
                self.HType(self.program[self.programCounter])
            elif self.program[self.programCounter][0] in self.JTypeList:
                self.JType(self.program[self.programCounter])
            if self.debug:
                print(temp,self.program[self.programCounter])

    def branchToJump(self, i):
        #self.program[i][3] = hex((self.symbolDef[self.program[i][3]] - i + 2) & 0xF)[2:] + " Needs to be changed, BTJD"
        if self.debug:
            temp = self.program[i] #debugging var to see what was going on.
            print(temp,"became:")
        self.updateSymbols(i,1)
        sym = self.program[i][3]
        # jr $pc :sym
        jump = ['jr','$pc',sym]
        self.program[i][3] = 1;
        #print(self.program[i][0])
        if self.program[i][0] == 'beq':
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
    def jumpToBigJump(self, i):
        if self.debug:
            temp = self.program[i]
        sym = self.program[i][2]
        offset = self.symbolDef[sym]
        if self.debug:
            print('jump to',sym,'being converted to big jump')
        self.program.insert(i,['cpy','$a1',offset])
        self.program[i+1] = ['jr','$a1',0]

        if self.debug:
            print(temp,"became:\n",self.program[i],'\n',self.program[i+1])


    def symToOffset(self, sym, line):
        if self.debug:
            print("creating offset from line",line,'to',self.symbolDef[sym],'for sym',sym)
            print('calculated as',self.symbolDef[sym] - line + self.symOff,'for', self.program[line])
        return self.symbolDef[sym] - line + self.symOff

    #two byte mostly for jumps
    def toHexSigned(self, num):
        out = hex(num & 0xFF)[2:]
        if len(out) == 1:
            out = '0' + out

        if self.debug:
            print('converted',num,'to',hex(num & 0xFF)[2:])

        return out

    # one byte, mostly for branches
    def toHexUnsigned(self, num):
        if self.debug:
            print('converted',num,'to',hex(num)[2:])
        return hex(num)[2:]

    def expandSymbols(self):
        offset = 0
        if self.debug:
            print(self.symbolDef)
        self.programCounter = 0
        while self.programCounter < len(self.program):

            if not isinstance(self.program[self.programCounter], list):
                self.programCounter += 1 #whoops
                continue
            # Branching l0gic
            if (self.program[self.programCounter][0] in ['beq','bne','bgt','blt'] and
                            self.program[self.programCounter][3] in self.symbolDef):
                offset = self.symToOffset(self.program[self.programCounter][3], self.programCounter)
                if offset > 15 or offset < 0:
                    self.branchToJump(self.programCounter)
                else:
                    self.program[self.programCounter][3] = self.toHexUnsigned(offset)
            # Jumping logic
            elif (self.program[self.programCounter][0] in ['jr'] and
                  len(self.program[self.programCounter]) > 2 and
                  self.program[self.programCounter][2] in self.symbolDef):
                offset = self.symToOffset(self.program[self.programCounter][2], self.programCounter)
                if offset > 127 or offset < -128: #2^8 signed is 127 to -128
                    self.jumpToBigJump(self.programCounter)
                else:
                    self.program[self.programCounter][2] = self.toHexSigned(offset)

            self.assembleCurrentLine() #trying this here

            self.programCounter += 1 #NOT MISSING THIS AGAIN

    def expandSymbolsold(self):
        if self.debug:
            print(self.symbolDef)
        i = 0
        while i < len(self.program):
            if self.debug:
                temp = self.program[i]
            if len(self.program[i]) is 4: # to make sure that constants don't crash this
                if self.program[i][3] in self.symbolDef: # to make sure that it is a correct symbol
                    if self.program[i][0] in [self.binaryMapInst['beq'],
                                              self.binaryMapInst['bne'],
                                              self.binaryMapInst['bgt'],
                                              self.binaryMapInst['blt']]: # This is all of the branching instructions
                        if (self.symbolDef[self.program[i][3]] - i + self.symOff) > 15:
                            self.branchToJump(i)
                        elif (self.symbolDef[self.program[i][3]] - i + self.symOff) < 0:
                            self.branchToJump(i)
                        else:
                            if self.debug:
                                print(self.program[i], hex((self.symbolDef[self.program[i][3]] - i + self.symOff) & 0xF))
                            self.program[i][3] = hex((self.symbolDef[self.program[i][3]] - i + self.symOff) & 0xF)[2:]
                            if self.debug:
                                print(self.program[i])
                    else:
                        raise Exception("Unknown use of Synmbols: " + str(self.program[i]))
            elif len(self.program[i]) is 3: #to make sure that it can handel jumps
                if self.program[i][0] in [self.binaryMapInst['jr']]:
                    if self.program[i][2] in self.symbolDef:
                        if self.debug:
                            print(self.program[i], hex((self.symbolDef[self.program[i][2]] - i + self.symOff) & 0xFF))
                        self.program[i][2] = hex((self.symbolDef[self.program[i][2]] - i + self.symOff) & 0xFF)[2:]
                        if len(self.program[i][2]) < 2:
                            self.program[i][2] = '0'+self.program[i][2]
                        if self.debug:
                            print(self.program[i])
            i += 1 #because I can't use the for loop and expand the list


    def pseudoExpandHelper(self, inst): #less Hacky bullshit
    #I can make this work maybe
        if self.debug:
            print(inst,'=>')
        if 'j' in inst:
            out = [['jr','$pc',inst[1]]]
        elif 'jal' in inst:
            out = [['cpy','$ra','4'],
                ['add','$ra','$pc'],
                ['jr','$pc',inst[1]]]
        elif 'psh' in inst:
            out = [['sub','$sp','4'],
                    ['w',inst[1],'$sp','0']]
        elif 'pop' in inst:
            out = [['r',inst[1],'$sp','0'],
                    ['add','$sp','4']]

        if len(out) > 1:
            self.updateSymbols(self.programCounter, len(out)-1)

        self.program.pop(self.programCounter)
        out.reverse()
        for i in out:
            self.program.insert(self.programCounter,i)

        if self.debug:
            print(out)


    def expandPseudo(self):
        self.programCounter = 0;
        while self.programCounter < len(self.program):
            if self.program[self.programCounter][0] in self.PseudoList:
                self.pseudoExpandHelper(self.program[self.programCounter])

            self.programCounter += 1


    def printAsm(self, outFile):
        with open(outFile, 'w') as dest:
            dest.write("""THIS IS NOT DONE YET
The pseudo instructions are not yet finished, they still need to be implemented.
Please be careful with this.


""")
            for line in self.program:
                if not isinstance(line, str):
                    dest.write('0x')
                else:
                    if line.isdigit():
                        dest.write(hex(int(line)))
                    else:
                        dest.write(line)
                    dest.write('\n')
                    continue
                for inst in line:
                    if isinstance(inst, str):
                        dest.write(inst)
                    else:
                        dest.write(hex(inst)[2:])
                dest.write('\n')


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
            out[1] = 0x1 
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
            # w s o(d)
            # w d s o
    def BType(self, inst):
        out = ['','','','']
        if inst[0] in ['r','w']:
            out[0] = self.binaryMapInst[inst[0]]
            out[3] = inst[2]
            if inst[0] is 'r':
                out[1] = self.binaryMapRegs[inst[1]] #setting destination
                out[2] = self.binaryMapRegs[inst[3]] #setting source
            else:
                out[1] = self.binaryMapRegs[inst[3]] #setting dest
                out[2] = self.binaryMapRegs[inst[1]] #setting srouce
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
        if not isinstance(inst[1], int) and '$' in inst[1]: 
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = inst[2]
        elif not isinstance(inst[2], int) and '$' in inst[2]:
            out[1] = self.binaryMapRegs[inst[2]]
            out[2] = inst[1]
        if len(out[2]) is 1:
                out[2] = '0' + out[2]
        else:
            out[2] = '00'
        self.program[self.programCounter] = out

    def RType(self, inst):
        out = ['','','','']
        out[0] = self.binaryMapInst[inst[0]]
        out[1] = self.binaryMapRegs[inst[1]]
        out[2] = self.binaryMapRegs[inst[2]]
        out[3] = int(inst[3])
        self.program[self.programCounter] = out

    def SType(self, inst):
        out = ['',0,0,0]
        out[0] = self.binaryMapInst[inst[0]]
        self.program[self.programCounter] = out


    def run(self, inPath, outPath):
        self.readFile(inPath)
        self.expandPseudo()
        #self.assemble()
        self.expandSymbols()
        self.printAsm(outPath)

if __name__ == '__main__':
    import sys

    sys.argv = [sys.argv[0], "RelPrime.asm","RelPrime.bin","debug"]
    
    helpPrint = """The use of this program:
assembler infile.asm <outfile.bin> <debug>
-h:     Prints this message

if the outfile is not specified, it will write to out.bin
if 'debug'(all lower) is passed anywhere, it will toggle debugging mode

This is still a work in progress"""

    if '-h' in sys.argv:
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

    if inFile is '':
        print(helpPrint)
        sys.exit(0)
    
    asm.run(inFile, outFile)
