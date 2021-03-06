package edu.rose_hulman.csse232.groupM;

import java.io.IOException;
import java.util.ArrayList;

public class Emulator {
	Memory mem;
	Register[] registers;
	Register scp;
	short activeSchwap;
	Appendable console;
	boolean halt;
	ArrayList<Short> breakpoints;
	
	public Emulator(short sp, short pc) {
		halt = false;
		mem = new Memory();
		scp = new Register();
		this.registers = new Register[16];
		for (short i = 0; i < 12; i++)
			this.registers[i] = new Register();
		for (short i = 12; i < 16; i++)
			this.registers[i] = new SchwapRegister();
		this.setRegister((short) 4, sp);
		this.setRegister((short) 3, pc);
		this.breakpoints = new ArrayList<Short>();
	}
	
	
	/**
	 * Steps the emulator. Gets instruction at pc, increments pc by 2, then runs instruction.
	 * @return True if reached a breakpoint.
	 */
	public boolean step() {
		if (halt)
			return true;
		short pc = this.getRegister((short) 3);//pc
		short inst = mem.getMemory(pc);
//		write("Step: $PC=%04x ==> %04x", pc, inst);
		this.setRegister((short) 3, (short) (pc + 1));
		this.cmd(inst);
		this.setRegister((short) 0, (short) 0);
		return this.breakpoints.contains(this.getRegister((short) 3));
	}


	/**
	 * Runs an instruction. 
	 * @param inst
	 */
	public void cmd(short inst) {
		short opcode = (short) ((inst & 0xF000) >> 12);
		short temp = -2;
		switch (opcode) {
			case 0: aluRegisters(
					(short) ((inst & 0x0F00) >> 8), // Destination
					(short) ((inst & 0x00F0) >> 4), // Source
					(short) ((inst & 0x000F))		// Function
				);
				break;
			case 1: 
				short pc = this.getRegister((short) 3);//pc
				short imm = mem.getMemory(pc); //instuction after
				this.setRegister((short) 3, (short) (pc + 1)); //skip over the immediate
				aluImmediate(
					(short) ((inst & 0x0F00) >> 8), // Destination
					(short) ((inst & 0x00F0) >> 4), // Source
					imm,							// Immediate
					(short) ((inst & 0x000F))		// Function
				);
				break;
			case 2: temp = 0;						// BEQ
			case 3: temp = (temp!=-2)?temp:2;		// BNE
			case 4: temp = (temp!=-2)?temp:1;		// BGT
			case 5: temp = (temp!=-2)?temp:-1;		// BLT
					branch(
						temp,							// Condition
						(short) ((inst & 0x0F00) >> 8), // Reg0
						(short) ((inst & 0x00F0) >> 4), // Reg1
						(byte) ((inst & 0x000F))	// offset
					);
					break;
			case 6: jumpRegister(
						(short) ((inst & 0x0F00) >> 8), // Register
						(byte) ((inst & 0x00FF)) 		// Offset
					);
					break;
			case 7: temp = 0;							// read
			case 8: temp = (temp!=-2)?temp:1;			// write
					memoryOp(
						temp == 1,						// write flag
						(short) ((inst & 0x0F00) >> 8), // Destination
						(short) ((inst & 0x00F0) >> 4), // Source
						(short) ((inst & 0x000F))		// Offset
					);
			case 0xA: SCP(); break;
			case 0xE: setSchwap((short) ((inst & 0x000F))); break;
			case 0xF: syscall((short) ((inst & 0x000F))); break;
		}
	}
	
	/** 
	 * Switches out stuff
	 */
	private void SCP() {
		Register temp = this.scp;
		this.scp = this.registers[2];
		this.registers[2] = temp;
	}


	private void syscall(short s) {
		write("Syscall %d", s);
//		switch(s) {
//			case 10:
//				write("%04x\t%04x\t%04x\t%04x",
//					this.getSchwapRegister((short) 12, (short) 12),
//					this.getSchwapRegister((short) 12, (short) 13),
//					this.getSchwapRegister((short) 12, (short) 14),
//					this.getSchwapRegister((short) 12, (short) 15)
//				);
//				break;
//			case 0:
//				write("Shutdown received. Halting emulator.");
//				halt = true;
//				break;
//		}
		SCP();
		this.setRegister((short) 3, s);
	}
	
	private void setSchwap(short s) {
		this.activeSchwap = s;
	}

	private void jumpRegister(short reg, byte offset) {
//		this.write("Jumping to register $%d, offset = %d", reg, offset);
		this.setRegister((short) 3, (short) (this.getRegister(reg) + offset));
	}

	private void memoryOp(boolean write, short d, short s, short o) {
		if (!write) {
			this.setRegister(d, 
					mem.getMemory( this.getRegister(s) + o )
				);
		}
		else {
			mem.setMemory( 
					this.getRegister(s) + o,
					this.getRegister(d)
				);
		}
	}

	private void branch(short condition, short s, short t, byte offset) {
		boolean branch = false;
		switch (condition) {
			case 0: branch = (this.getRegister(s) == this.getRegister(t)); break;
			case 1: branch = (this.getRegister(s) > this.getRegister(t)); break;
			case -1: branch = (this.getRegister(s) < this.getRegister(t)); break;
			case 2: branch = (this.getRegister(s) != this.getRegister(t)); break;
		}
		if (branch)
			this.setRegister((short) 3, (short) (this.getRegister((short) 3) + offset)); 
	}

	private void aluImmediate(short dest, short src, short imm, short f) {
		this.setRegister(src, imm);
		aluRegisters(dest, src, f);
	}

	private void aluRegisters(short dest, short src, short f) {
		switch (f) {
			case 0: setRegister(dest, (short) (this.getRegister(dest) & this.getRegister(src))); break;
			case 1: setRegister(dest, (short) (this.getRegister(dest) | this.getRegister(src))); break;
			case 2: setRegister(dest, (short) (this.getRegister(dest) ^ this.getRegister(src))); break;
			case 3: setRegister(dest, (short) (~this.getRegister(dest))); break;
			case 4: setRegister(dest, (short) (~this.getRegister(dest) + 1)); break;
			case 5: setRegister(dest, (short) ((this.getRegister(dest) < this.getRegister(src))?1:0)); break;
			case 6: setRegister(dest, (short) ((this.getRegister(dest) > this.getRegister(src))?1:0)); break;
			case 7: setRegister(dest, (short) (this.getRegister(dest) << this.getRegister(src))); break;
			case 8: setRegister(dest, (short) (this.getRegister(dest) >> this.getRegister(src))); break;
			case 9: setRegister(dest, (short) (this.getRegister(dest) >>> this.getRegister(src))); break;
			case 0xA: setRegister(dest, (short) (this.getRegister(dest) + this.getRegister(src))); break;
			case 0xB: setRegister(dest, (short) (this.getRegister(dest) - this.getRegister(src))); break;
			case 0xF: setRegister(dest, this.getRegister(src)); break;
			default: this.write("Uh-oh spaghetti-os that's not a valid ALU function! (0x%x)", f);
		}
	}

	public void write(String s, Object... args) {
		try {
			console.append(String.format(s, args));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void setBreakpoint(int addr) {
		this.write("SET BREAKPOINT:\t%x", (short) addr);
		this.breakpoints.add(new Short((short) addr));
	}
	
	public void setRegister(short register, short v) {
		registers[register].set((short) v);
	}

	/**
	 * Gets value of register $i
	 * @param i Register #
	 * @return Value of register
	 */
	public short getRegister(short i) {
		return registers[i].get();
	}

	/**
	 * Gets the # of the schwap that is active.
	 * @return
	 */
	public short getActiveSchwap() {
		return this.activeSchwap;
	}

	/**
	 * Gets a value of a certain schwap
	 * @param schwap Which swap
	 * @param reg	 Which register in the swap (0 <= reg <= 3)
	 * @return
	 */
	public short getSchwapRegister(short schwap, short reg) {
		if (this.registers[reg] instanceof SchwapRegister) {
			return ((SchwapRegister) registers[reg]).get(schwap);
		}
		return 0;
	}

	/**
	 * Set the stream the console writes to.
	 * @param document
	 */
	public void setConsoleStream(Appendable ap) {
		this.console = ap;
	}
	
	public void loadDataMemory(String[] lines) {
		int loadTo = this.getRegister((short) 3);
		int i = 0;
		if (lines[0].startsWith("#")) {
			loadTo = Integer.parseInt(lines[0].substring(1),16);
			i++;
		}
		write("Loading data to address: %04x", loadTo);
		//this.setRegister((short) 3, (short) loadTo);
		for (; i < lines.length; i++) {
			mem.setMemory(loadTo, (short) Integer.parseInt(lines[i].substring(2), 16));
			loadTo++;
		}
	}

	/**
	 * Gets 4 shorts per line at data memory for {@code lines} number of lines. <br>
	 * 
	 * @param lines
	 * @return String representation, lines lines long.
	 */
	public String debugMemory(int lines) {
		short base = this.getRegister((short) 4); //get sp
		StringBuilder sb = new StringBuilder();
		for (short l = 0; l < lines; l++) {
			short mem = (short) (base - (l * 4));
			if (mem < base) // bottom of stack reached;
				break;
			short[] ln = this.mem.getMemoryBlock(base - (l * 4), 4);
			sb.append(String.format("%s %04X:\t", 
					(this.breakpoints.contains(
							(short) (base - (l * 16))
					))?"*":" ",
					(short) (base - (l * 16))));
			for (short i = 3; i >= 0; i--) {
				sb.append(String.format("%04x ", ln[i]));
			}
			if (l+1 != lines)
				sb.append('\n');
		}
		return sb.toString();
	}
	
	/**
	 * Shows current instructions in memory and disassembled code afterwards.
	 * 
	 * @param lines Number of lines to show
	 */
	public String debugInstructions(int lines) {
		StringBuilder data  = new StringBuilder();
		int pc = this.getRegister((short) 3);
		for (int i = 0; i < lines; i++)
			data.append(String.format("%04x\t%s%n", mem.getMemory(pc + (i*2)), disassemble(pc + (i*2))));
		return data.toString();
	}

	class Register {
		short value;
		public void set(short i) {
			value = i;
		}
		public short get() {return value;}
	}


	class SchwapRegister extends Register {
		Register[] registers;
		
		public SchwapRegister() {
			registers = new Register[16];
			for (int i = 0; i < registers.length; i++)
				registers[i] = new Register();
		}

		public short get(short schwap) {return registers[schwap].get();}
		public short get() {return registers[activeSchwap].get();}
		
		public void set(short schwap, short val) {registers[schwap].set(val);}
		public void set(short val) {registers[activeSchwap].set(val);}
		
	}
	
	public String disassemble(int addr) {
		short ppre = mem.getMemory(addr - 2); 
		short prev = mem.getMemory(addr - 1);
		short curr = mem.getMemory(addr);
		short next = mem.getMemory(addr + 1);
		if (((prev >> 12) == 1) && !((ppre >> 12) == 1)) // this is an immediate
			return "<IMM>";
		// Normal
		String filler = null;
		switch ((curr >> 12) & 0xF) { //opcode
		//alu
		case 0:		filler = "";
		case 1: 	filler = (filler == null)?", " + Integer.toHexString(next):filler;		
					return String.format("%s $%d, $%d%s", FunctionCodes.getByCode(curr & 0xF), (curr>>8) & 0xF, (curr>>4) & 0xF, filler);
		// branches
		case 2: 	filler = "beq";
		case 3:		filler = (filler == null)?"bne":filler;
		case 4:		filler = (filler == null)?"bgt":filler;
		case 5:		filler = (filler == null)?"blt":filler;
					return String.format("%s $%d, $%d, 0x%x", filler, (curr>>8) & 0xF, (curr>>4) & 0xF, curr & 0xF);
		//mem
		case 7:		return String.format("r $%d, 0x%x($%d)", (curr>>8) & 0xF, curr & 0xF, (curr>>4) & 0xF);
		case 8:		return String.format("w 0x%x($%d), $%d", curr & 0xF, (curr>>8) & 0xF, (curr>>4) & 0xF);
		//Jump register
		case 6:		return String.format("jr 0x%x($%d)", curr & 0xFF, (curr>>8) & 0xF);
		//SCP
		case 10: 	return "scp";
		//H-Types
		case 14:	filler = "rsh";
		case 15:	filler = (filler == null)?"sudo":filler;
					return String.format("%s %d", filler, curr & 0xF);
		default: 	return "???";
		}
	}


	public String debugInstructions(int lower, int upper) {
		int line = (upper - lower);
		System.out.printf("L:%d U:%d LN: %d%n", lower, upper, line);
		StringBuilder data  = new StringBuilder();
		for (int i = 0; i < line; i++)
			data.append(String.format(" %04x: %04x\t%s%n", lower + (i), mem.getMemory(lower + (i)), disassemble(lower + (i))));
		return data.toString();
	}
}


enum FunctionCodes {
	and,
	orr, 
	xor,
	not,
	tsc,
	slt,
	sgt,
	sll,
	srl,
	sra,
	add,
	sub,
	INVALID_0xC,
	INVALID_0xD,
	INVALID_0xE,
	cpy;
	
	public static String getByCode(int code) {
		return FunctionCodes.values()[code].name();
	}
}
