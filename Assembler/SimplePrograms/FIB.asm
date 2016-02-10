# FIB loop test with sudo call to print from schwap 12

main:
	cpy $t0 0
	cpy $t1 1

	cpy $s0 $0 #setting up for alt path through loop
	cpy $s1 500 #ending number

	rsh 12 #for sudo call

start:
	beq $s0 $0 two
	cpy $h0 $t1
	add $t1 $t0
	j end
two:
	cpy $h0 $t0
	add $t0 $t1
end:
	not $s0 $0
	sudo 10
	blt $h0 $s1 start
	
	sudo 0

done: