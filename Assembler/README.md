# Version 2 of the Schwap Assembler

## Simple programs to test the CPU
Provided to help test the assembler as well

1. FIB
	* Standard Fibonacci sequence to test looping and branching
2. ALUTEST
	* arguably the most simple
	* will test all of the ALU instructions
3. PROCEDURES
	* will test jal and ra
	* it is unknown if it works at this time
4. SIMPLEPROCEDURES 
	* will test jal and ra
	* was mostly a test for the assembler, but it will force the CPU to make a lot of jumps.
	* no branching


### Notes

At this time there are a few assumptions

1. Sudo instructions
	- sudo 10 will display everything is schwap 12
	- sudo 0 will end the program
		These are made to deal with the fact that _0000_ is _and $0 $0_ and not good ways to determine the end of a programs.
2. All immediates are in base 10, the current version of the assembler doesn't like hex yet.


Everything in the out file has been assembled with **1000** as the offset.
This assumes that the program will start at 1000, and travel up in memory
eg: 1000, 1002, 1004...
This mean all non PC relative jumps will be jumping to something big if that is not taken into account.

If this needs to be changed, re-assemble things, it is easy to use the python script, it has help text. Pass it -h or help or run it with no arguments to see it.

This does handle the fact that the programs do grow as the numbers being jumped or branched increase, this does deal with it, if the program appears bigger than was initially predicted, that is because one of the edge cases was hit, either a jump grew outside of the offset range, or a branch did. In rare cases, both can happen. (See Test3 symbolic jump in SimpleProcedures.*)

### Predicted things

There may be a bug with the reading from memory, or writing to memory. I am not sure, but it appeared to change something that I was not expecting it to change.
