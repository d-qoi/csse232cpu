class Assembler:

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

    PseudoList = {'jl',}

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
                    inst = inst[1:] #remove the symbol
                    if len(inst) is 0:
                        continue

                self.program.append(inst) # append program to inst
                
                #sudo instruction expansion
                

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

                    self.programCounter += 1
                    #debugging
                    print(self.program)
                    print(self.programCounter + ' ' len(self.program))
                


    def AType(self, inst):
        out = [0x0,'','','']
        if '$' in inst[1] and '$' in inst[2]: # two registers
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out
        elif len(inst) is 3:
            if '$' in inst[1]:
                out[0] = 0x1
                out[1] = self.binaryMapRegs[inst[1]]
                out[2] = self.binaryMapInst['$zz']
                out[3] = self.binaryMapInst[inst[0]]
            elif '$' in inst[2]:
                out[0] = 0x1
                out[1] = self.binaryMapRegs[inst[2]]
                out[2] = self.binaryMapInst['$zz']
                out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out
            self.program.append(self.programCounter + 1, inst[1])
            self.programCounter += 1
        else:
            out[1] = 0x1
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program[self.programCounter] = out
            self.program.append(self.programCounter + 1, inst[3])
            self.programCounter += 1

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
        out[3] = (int(inst[1]) & 0xF)
         self.program[self.programCounter] = out

    def JType(self, inst):
        out = ['','','']
        out[0] = self.binaryMapInst[inst[0]]
        out[1] = self.binaryMapRegs[inst[1]]
        out[3] = (int(inst[3]) & 0xFF)
         self.program[self.programCounter] = out

    def RType(self, inst):
        out = ['','','','']
        out[0] = self.binaryMapInst[inst[0]]
        out[1] = self.binaryMapRegs[inst[1]]
        out[2] = self.binaryMapRegs[inst[2]]
        out[3] = (int(inst[3]))
         self.program[self.programCounter] = out

    def SType(self, inst):
        out = ['',0,0,0]
        out[0] = self.binaryMapInst[inst[0]]
         self.program[self.programCounter] = out

    def pseudoExpand(self, inst):
        pass

    def __init__(self, progStart):
        progStart = 0
        self.progStart = progStart

if __name__ == '__main__':
    tempPath = 'RelPrime.asm'
    Assembler(0).assemble(tempPath)
    
