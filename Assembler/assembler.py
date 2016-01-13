class assembler:

	progStart = 0
	memStart = 0
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


	def assemble(inPath, outPath):
		with open(inPath, r) as in prog:
			while True:
				instruction = prog.readline().strip()
				if instruction is '': #eof
					break


				if instruction.contains('#'): #cutting out comments
					instruction = instruction[0:instruction.index('#').strip()] 

				inst = [item.strip().strip(',') for item in instruction.split()]
				# I don't like this line, but it is shorter than alternatives
				# This line trims the list into specific values

				if inst[0].contains(':'):
					symbolDef[inst[0].strip()[0:-1]] = len(program) + 1 #add to the symbol
					inst = inst[1:] #remove the symbol

				if inst[0] in ATypeList:
					AType(inst)
				elif inst[0] in BTypeList:
					BType(inst)
				elif inst[0] in HTypeList:
					HType(inst)
				elif inst[0] in JTypeList:
					JType(inst)
				elif inst[0] in RTypeList:
					RType(inst)
				elif inst[0] in STypeList:
					SType(inst)

	def AType(inst):
		out = [0x0,'','','']
		if '$' in inst[1] and '$' in inst[2]: # two registers
			out[1] = binaryMapRegs[inst[1]]
			out[2] = binaryMapRegs[inst[2]]
			out[3] = binaryMapInst[inst[0]]
			program.append(out)
		else:
			if '$' in inst[1]:
				out[0] = 0x1
				out[1] = binaryMapRegs[inst[1]]
				out[2] = binaryMapInst['$zz']
				out[3] = binaryMapInst[inst[0]]
			elif '$' in inst[2]
				out[0] = 0x1
				out[1] = binaryMapRegs[inst[2]]
				out[2] = binaryMapInst['$zz']
				out[3] = binaryMapInst[inst[0]]
			program.append(out)
			program.append(inst[1])

		# Ignoreing 0x1 $r $r 0ximm case for now

	def BType(inst):
		out = ['','','','']
		out[0] = binaryMapInst[inst[0]]
		out[1] = binaryMapRegs[inst[1]]
		out[2] = binaryMapRegs[inst[2]]
		out[3] = inst[3]

	def HType(inst):
		out = ['',0x0,0x0,'']
		out[0] = binaryMapInst[inst[0]]
		out[3] = (int(inst[3]) & 0xF)

	def JType(inst):
		out = ['','','']
		out[0] = binaryMapInst[inst[0]]
		out[1] = binaryMapRegs[inst[1]]
		out[3] = (int(inst[3]) & 0xFF)

	def RType(inst):
		out = ['','','','']
		out[0] = binaryMapInst[inst[0]]
		out[1] = binaryMapRegs[inst[1]]
		out[2] = binaryMapRegs[inst[2]]
		out[3] = (int(inst[3]))

	def SType(inst):
		out = ['',0,0,0]
		out[0] = binaryMapInst[inst[0]]

	def __init__(self, progStart):
