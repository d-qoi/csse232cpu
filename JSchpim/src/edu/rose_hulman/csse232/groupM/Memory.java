package edu.rose_hulman.csse232.groupM;

import java.util.HashMap;

public class Memory {
	HashMap<Integer, Short> mem;
	
	public Memory() {
		mem = new HashMap<Integer, Short>();
	}
	
	public short[] getMemoryBlock(int address, int shorts) {
		short[] vals = new short[shorts];
		for (int i = 0; i < shorts; i++) {
			vals[i] = getMemory(address + (2 * i));
		}
		return vals;
	}
	
	public short getMemory(int address) {
		return (mem.containsKey(new Integer(address)))?mem.get(new Integer(address)):0;
	}
	
	public void setMemory(int address, short value) {
		mem.put(new Integer(address), value);
	}

	public void clear() {
		mem.clear();
	}
}
