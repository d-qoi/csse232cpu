# Version 2.1 of the Schwap Assembler

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
5. everything
	* tests some of everything,
	* if a comparison fails or jump fails, it will halt the program in the middle.
6. JumpWat
	* tests jumping
	* weird pattern for error finding
7. sillyMemoryTest
	* Tests Memory read and write
8. SimpleBranchTest
	* Test branching
	* loops if failure state
9. Tests
	* testing the assembler, don't actually recommend running.

### Notes

At this time there are a few assumptions

1. Sudo instructions
	- sudo 10 will display everything is schwap 12
	- sudo 0 will end the program
		These are made to deal with the fact that _0000_ is _and $0 $0_ and not good ways to determine the end of a programs.
2. All immediates are in base 10, the current version of the assembler doesn't like hex yet.


## RelPrime
This is the unit test for this project.
It will find an int that is relativly prime to the one that it is passed
There is a simple wrapper for this procedure, it start at 10, 9 is relativly prime to it.