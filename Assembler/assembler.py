class Assembler:

    debug = False
    progStart = 0
    programCounter = 0
    program = []
    globalDef = {}
    symbolDef = {}

    binaryMapInst = {'add':0x0, 
                'adu':0x1,
                'sub':0x2,
                'sbu':0x3,
                'sll':0x4,
                'srl':0x5,
                'sra':0x6,
                'and':0x7,
                'orr':0x8,'or':0x8,
                'xor':0x9,
                'not':0xA,
                'tsc':0xB,
                'ldi':0xE, 'li':0xE,
                'cpy':0xF,
                'jr':0x2,
                'rsh':0x3,
                'beq':0x4,
                'bnq':0x5,'bne':0x5,
                'bgt':0x6,
                'r':0x7,
                'w':0x8,
                'sudo':0xF}

    binaryMapRegs = {'$0':0x0,'$00':0x0,'$z0':0x0,'$zz':0x0,
                    '$pc':0x1,
                    '$sp':0x2,
                    '$ra':0x3,
                    '$s0':0x4,
                    '$s1':0x5,
                    '$s2':0x6,
                    '$s3':0x7,
                    '$t0':0x8,
                    '$t1':0x9,
                    '$t2':0xA,
                    '$t3':0xB,
                    '$h0':0xC,
                    '$h1':0xD,
                    '$h2':0xE,
                    '$h3':0xF}


    ATypeList = {'add','adu','sub','sbu','sll','srl','sra','and','orr','or',
                'xor','not','tsc','ldi','li','cpy'}

    PseudoList = {'jl','j','li','ldi'} # Please update and see the method

    BTypeList = {'beq','bnq','bne','bgt'}
    HTypeList = {'rsh'}
    JTypeList = {'jr'}
    RTypeList = {'r','w'}
    STypeList = {'sudo'}

    def assemble(self, inPath):
        # This cannot be a file read in, it must be a list to pass
        with open(inPath, 'r') as prog:
            while True:
                instruction = prog.readline().strip()
                if instruction is '': #eof
                    break
                instruction = instruction.strip().lower()
                if instruction is '': #empty line
                    continue


                if '#' in instruction: #cutting out comments
                    instruction = instruction[0:instruction.index('#')] 

                inst = [item.strip().strip(',') for item in instruction.split()]
                # I don't like this line, but it is shorter than alternatives
                # This line trims the list into specific values

                if ':' in inst[0]:
                    self.symbolDef[inst[0].strip()[0:-1]] = len(self.program) #add to the symbol
                    if self.debug:
                        print(self.symbolDef)
                    inst = inst[1:] #remove the symbol
                    if len(inst) is 0:
                        continue

                self.program.append(inst) # append program to inst
                #Appending the new line of asm to the end of the program, and reading from the program counter to update the program to contain the converted line
                # I am doing this to account for the fact that all pseudo instructions are going to make this code bigger
                # If I were to continue reading from the file, then things would go badly,
                # in this case, we can just append to the Program and let the following code take care of converting the extended program into binary/hex

                while self.programCounter < len(self.program):
                    if self.program[self.programCounter][0] in self.ATypeList:
                        self.AType(self.program[self.programCounter])
                    elif self.program[self.programCounter][0] in self.BTypeList:
                        self.BType(self.program[self.programCounter])
                    elif self.program[self.programCounter][0] in self.HTypeList:
                        self.HType(self.program[self.programCounter])
                    elif self.program[self.programCounter][0] in self.JTypeList:
                        self.JType(self.program[self.programCounter])
                    elif self.program[self.programCounter][0] in self.RTypeList:
                        self.RType(self.program[self.programCounter])
                    elif self.program[self.programCounter][0] in self.STypeList:
                        self.SType(self.program[self.programCounter])
                    elif self.program[self.programCounter][0] in self.PseudoList: #sudo instruction expansion
                        self.pseudoExpand(self.program[self.programCounter])
                        if self.debug:
                            print(self.program[-3:],self.program[self.programCounter-1])
                        continue
                    else:
                        raise NameError("Unknown Instruction:", self.program[self.programCounter][0])

                    self.programCounter += 1
                    #debugging
                    if self.debug:
                        print(self.program)
                        print(self.programCounter, str(len(self.program)))


    def branchToJumpDown(self, i):
        self.program[i][3] = hex((self.symbolDef[self.program[i][3]] - i + 2) & 0xF)[2:] + " Needs to be changed, BTJD"

    def branchToJumpUp(self, i):
        self.program[i][3] = hex((self.symbolDef[self.program[i][3]] - i + 2) & 0xF)[2:] + " Needs to be changed, BTJU"

    def expandSymbols(self):
        if self.debug:
            print(self.symbolDef)
        for i in range(0,len(self.program)):
            if self.debug:
                temp = self.program[i]
            if len(self.program[i]) is 4: # to make sure that constants don't crash this
                if self.program[i][3] in self.symbolDef: # to make sure that it is a correct symbol
                    if self.program[i][0] in [0x4,0x5,0x6]: # This is all of the branching instructions
                        if (self.symbolDef[self.program[i][3]] - i + 2) > 15:
                            branchToJumpDown(i)
                        elif (self.symbolDef[self.program[i][3]] - i + 2) < 0:
                            branchToJumpUp(i)
                        else:
                            if self.debug:
                                print(self.program[i], hex((self.symbolDef[self.program[i][3]] - i + 2) & 0xF))
                            self.program[i][3] = hex((self.symbolDef[self.program[i][3]] - i + 2) & 0xF)[2:]
                            if self.debug:
                                print(self.program[i])
                    else:
                        raise NameError("Unknown use of Synmbols: " + str(self.program[i]))
            elif len(self.program[i]) is 3: #to make sure that it can handel jumps
                if self.program[i][0] in [0x2]:
                    if self.program[i][2] in self.symbolDef:
                        if self.debug:
                            print(self.program[i], hex((self.symbolDef[self.program[i][2]] - i + 2) & 0xFF))
                        self.program[i][2] = hex((self.symbolDef[self.program[i][2]] - i + 2) & 0xFF)[2:]
                        if len(self.program[i][2]) < 2:
                            self.program[i][2] = '0'+self.program[i][2]
                        if self.debug:
                            print(self.program[i])


    def printAsm(self, outFile):
        with open(outFile, 'w') as dest:
            dest.write("""THIS IS NOT DONE YET
The pseudo instructions are not yet finished, they still need to be implemented.
Please be careful with this.


""")
            for line in self.program:
                if not isinstance(line, str):
                    dest.write('0x')
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
        if '$' in inst[1] and '$' in inst[2]: # two registers
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
            self.program.insert(self.programCounter + 1, inst[2])
            self.programCounter += 1 #because I am inserting the immediate, the PC needs to be increased
        else: # case for which we are loading an immediate into the second source on the same line
            out[1] = 0x1 
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out
            self.program.insert(self.programCounter + 1, inst[3])
            self.programCounter += 1 # because I am inserting the PC, the immeadiate needs to be increased

    def BType(self, inst):
        out = ['','','','']
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
        out[0] = self.binaryMapInst[inst[0]]
        out[1] = self.binaryMapRegs[inst[1]]
        if len(out) is 3:
            out[2] = hex(int(inst[2]) & 0xFF)[2:]
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

    def pseudoExpand(self, inst):
        if 'jl' in inst or 'j' in inst:
            if self.debug:
                print(inst)
            out = ['','','']
            out[0] = self.binaryMapInst['jr']
            out[1] = self.binaryMapRegs['$pc']
            out[2] = inst[1]
            self.program[self.programCounter] = out #Hacky bullshit to make surethat I change this later
            self.programCounter += 1


    def run(self, inPath, outPath):
        self.assemble(inPath)
        self.expandSymbols()
        self.printAsm(outPath)

    def __init__(self, progStart):
        progStart = 0
        self.progStart = progStart

if __name__ == '__main__':
    import sys
    
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