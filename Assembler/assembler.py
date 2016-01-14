class assembler:

    progStart = 0
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

    binaryMapRegs = {'$0':0x0,'$00':0x0,'$z0':0x0,'$zz',0x0,
                    '$pc':0x1,
                    '$sp':0x2,
                    '$ra':0x3,
                    's0':0x4,
                    's1':0x5,
                    's2':0x6,
                    's3':0x7,
                    't0':0x8,
                    't1':0x9,
                    't2':0xA,
                    't3':0xB,
                    'h0':0xC,
                    'h1':0xD,
                    'h2':0xE,
                    'h3':0xF}


    ATypeList = {'add','adu','sub','sbu','sll','srl','sra','and','orr','or',
                'xor','not','tsc','ldi','cpy'}

    BTypeList = {'beq','bnq','bne','bgt'}
    HTypeList = {'rsh'}
    JTypeList = {'jr'}
    RTypeList = {'r','w'}
    STypeList = {'sudo'}


    def assemble(inPath):
        with open(inPath, r) as in prog:
            while True:
                instruction = prog.readline().strip()
                if instruction is '': #eof
                    break
                instruction = instruction.strip()
                if instruction is '': #empty line
                    continue


                if instruction.contains('#'): #cutting out comments
                    instruction = instruction[0:instruction.index('#')] 

                inst = [item.strip().strip(',') for item in instruction.split()]
                # I don't like this line, but it is shorter than alternatives
                # This line trims the list into specific values

                if inst[0].contains(':'):
                    symbolDef[inst[0].strip()[0:-1]] = len(self.program) #add to the symbol
                    inst = inst[1:] #remove the symbol

                if inst[0] in self.ATypeList:
                    self.AType(inst)
                elif inst[0] in self.BTypeList:
                    self.BType(inst)
                elif inst[0] in self.HTypeList:
                    self.HType(inst)
                elif inst[0] in self.JTypeList:
                    self.JType(inst)
                elif inst[0] in self.RTypeList:
                    self.RType(inst)
                elif inst[0] in self.STypeList:
                    self.SType(inst)

    def AType(self, inst):
        out = [0x0,'','','']
        if '$' in inst[1] and '$' in inst[2]: # two registers
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program.append(out)
        elif len(inst) is 3:
            if '$' in inst[1]:
                out[0] = 0x1
                out[1] = self.binaryMapRegs[inst[1]]
                out[2] = self.binaryMapInst['$zz']
                out[3] = self.binaryMapInst[inst[0]]
            elif '$' in inst[2]
                out[0] = 0x1
                out[1] = self.binaryMapRegs[inst[2]]
                out[2] = self.binaryMapInst['$zz']
                out[3] = self.binaryMapInst[inst[0]]
            self.program.append(out)
            self.program.append(inst[1])
        else:
            out[1] = 0x1
            out[1] = self.binaryMapRegs[inst[1]]
            out[2] = self.binaryMapRegs[inst[2]]
            out[3] = self.binaryMapInst[inst[0]]
            self.program.append(out)
            self.program.append(inst[3])

    def BType(self, inst):
        out = ['','','','']
        out[0] = self.binaryMapInst[inst[0]]
        out[1] = self.binaryMapRegs[inst[1]]
        out[2] = self.binaryMapRegs[inst[2]]
        out[3] = inst[3]

    def HType(self, inst):
        out = ['',0x0,0x0,'']
        out[0] = self.binaryMapInst[inst[0]]
        out[3] = (int(inst[3]) & 0xF)

    def JType(self, inst):
        out = ['','','']
        out[0] = self.binaryMapInst[inst[0]]
        out[1] = self.binaryMapRegs[inst[1]]
        out[3] = (int(inst[3]) & 0xFF)

    def RType(self, inst):
        out = ['','','','']
        out[0] = self.binaryMapInst[inst[0]]
        out[1] =self.binaryMapRegs[inst[1]]
        out[2] = self.binaryMapRegs[inst[2]]
        out[3] = (int(inst[3]))

    def SType(self, inst):
        out = ['',0,0,0]
        out[0] = self.binaryMapInst[inst[0]]

    def __init__(self, progStart):
        self.progStart = progStart

