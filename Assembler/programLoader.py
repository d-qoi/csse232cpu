class ProgramLoader:
    userStart = 4096
    kernelStart = 1
    fill = 0

    kernelFile = "LINUKS.bin"


    outFile = "out.coe"
    inFile = ""

    def __init__(self, inFile, outFile, kernelFile):
        self.inFile = inFile
        if outFile:
            self.outFile = outFile
        if kernelFile:
            self.kernelFile = kernelFile

    def createFile(self):
        with open(outFile,'w') as dest:
            dest.write(""";File generated by the Schwap Program Loader
;This expects a memory unit that has a width of 16 and a length of 20480
;program created by Alexander Hirsschfeld (@d-qoi)
memory_initialization_radix=16;
memory_initialization_vector=
0000,
""")


    def writeKernel(self):
        linenum = 1
        with open(outFile,'a') as dest:
            with open(kernelFile,'r') as src:
                for line in src:
                    dest.write(line[2:].strip())
                    dest.write(',\n')
                    linenum += 1
            while (linenum < self.userStart - 1):
                dest.write('0000,\n')
                linenum += 1


    def writeUser(self):
        code = []
        with open(inFile,'r') as src:
            for line in src:
                if '0x' in line:
                    code.append(line[2:].strip())
                elif '=' in line:
                    pos = int(line[0:line.index('=')].strip()) - self.userStart
                    while len(code) <= pos:
                        code.insert(pos,'0000,')
                    code[pos] = line[line.index('=') + 1:].strip()

        with open(outFile,'a') as dest:
            for line in code:
                dest.write(line)
                dest.write(',\n')

                

    def run(self):
        self.createFile()
        self.writeKernel()
        self.writeUser()


if __name__ == "__main__":
    import sys
    helpPrint = """
Welcome to the Schwappable CPU Coe Creator!
Use:
    programLoader program.bin <memory.coe> <kernel.bin>

Data can be preloaded into the memory file by adding:

            loc = data

to the end of the assembly

loc being the exact location above the program
and below 15480 (15480 to 20480 is user stack, can use but be careful)
and above 10000 or the end of your program, your decision

data is a 4 digit hex number, must be at most 4 digits, and hex
please augment with zeroes, not is untested because coe files are weird.

example : 10101 = abcd

there is not a lot of checking in this code, if it fails, that is on you ;)

kernel code     [0:4096)
user code       [4096:10000) <can be more, your call>
user space      [10000:15480)
stack           [15480:20480] <will underflow if you let it, grows down>

"""
    if '-h' in sys.argv or 'help' in sys.argv:
        print(helpPrint)
        sys.exit(0)

    if (len(sys.argv) < 2):
        print(helpPrint) 
        sys.exit(0)

    inFile = ''
    outFile = 'memory.coe'
    kernelFile = 'kernel.bin'

    inFile = sys.argv[1]

    sys.argv = sys.argv[2:]
    for arg in sys.argv:
        if '.coe' in arg:
            outFile = arg
        if '.bin' in arg:
            kernelFile = arg


    builder = ProgramLoader(inFile, outFile, kernelFile)

    if inFile is '':
        print(helpPrint)
        sys.exit(0)

    builder.run()