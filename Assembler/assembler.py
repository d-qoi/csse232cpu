class assembler:

	progStart = 0
	memStart = 0
	program = []
	globalDef = {}
	symbolDef = {}

	binaryMapInst = {'add':'0x0', 
				'adu':'0x1',
				'sub':'0x2',
				'sbu':'0x3',
				'sll':'0x4',
				'srl':'0x5',
				'sra':'0x6',
				'and':'0x7',
				'orr':'0x8','or':'0x8',
				'xor':'0x9',
				'not':'0xA',
				'tsc':'0xB',
				'ldi':'0xE',
				'cpy':'0xF',
				'jr':'0x2',
				'rsh':'0x3',
				'beq':'0x4',
				'bnq':'0x5','bne':'0x5',
				'bgt':'0x6',
				'r':'0x7',
				'w':'0x8',
				'sudo':'0xF'}

	binaryMapRegs = {'$0':'0x0','$00':'0x0','$z0':'0x0','$zz','0x0',
					'$pc':'0x1',
					'$sp':'0x2',
					'$ra':'0x3',
					's0':'0x4',
					's1':'0x5',
					's2':'0x6',
					's3':'0x7',
					't0':'0x8',
					't1':'0x9',
					't2':'0xA',
					't3':'0xB',
					'h0':'0xC',
					'h1':'0xD',
					'h2':'0xE',
					'h3':'0xF'}


	ATypeList = {'add','adu','sub','sbu','sll','srl','sra','and','orr','or',
				'xor','not','tsc','ldi','cpy'}

	BTypeList = {'beq','bnq','bne','bgt'}
	HTypeList = {'rsh'}
	JTypeList = {'jr'}
	RTypeList = {'r','w'}
	STypeList = {'sudo'}


	def assemble(inPath, outPath):
		with open(inPath, r) as in instruction:
			inst = instruction.split(' ')


	def getBinaryFor(code):
		if(code)

	def AType(inst):


	def BType(inst):

	def HType(inst):

	def JType(inst):

	def RType(inst):

	def SType(inst):


	def __init__(self, progStart, memStart):

