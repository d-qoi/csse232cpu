#Procedure calls!
# add procedure
# multiply procedure

main:
	rsh 8
	cpy $h0 10
	cpy $h1 3
	sub $pc 4
	w 0($pc) $h0 	# Storing things for later use
	w 1($pc) $h1
	jal mult
	rsh 9
	cpy $t0 $h0
	rsh 12
	r $h0 0($pc)	# reading to print
	r $h1 1($pc)
	add $pc 4
	cpy $h2 $t0
	sudo 10 		#a ssembler sudo for print the assembler regs.
	sudo 0 			# end the program
	and $0 $0 		# no op
	and $0 $0 		# no op

add: 				#takes two numbers and adds them together and returns one number
	cpy $t0 $0
	rsh 8
	add $t0 $h0
	add $t0 $h1
	rsh 9
	cpy $h0 $t0
	jr $ra
	and $0 $0 		# no op
	and $0 $0 		# no op

mult:				# takes two number and multiples them with multiplication
	rsh 4
	cpy $h0 $ra 	# save $ra
	rsh 8
	cpy $t0 $0
	cpy $s0 $h0
	cpy $s1 $h1
	rsh 9
	cpy $h0 $0
loop:
	rsh 8
	cpy $h0 $t0
	cpy $h1 $s0
	jal add
	rsh 9
	add $t0 $h0
	sub $s1 1
	beq $s1 $0 loop	#end the loop
	and $0 $0		# no op
	rsh 4
	jr $h0			#return
end:
