start:
	cpy $t3 1
begin:
	cpy $sp 4096
	cpy $t0 $0
	cpy $s0 61441
	rsh 0
	w 0($sp) $s0
	cpy $h0 $t0
	add $t0 1
	rsh 1
	cpy $h0 $t0
	rsh 0
t1:
	beq $h0 $0 correct1
	j incorrect
t2:
	bne $h0 $0 correct2
	j incorrect
correct1:
	rsh 1
	j t2
incorrect:
	and $0 $0
	sudo 0
	and $0 $0
correct2:
	and $s0 1337
	r $s1 0($sp)
	r $t0 0($sp)
	beq $s0 $s1 incorrect
	bne $t0 $s1 incorrect
	sub $t3 1
	beq $t3 $0 begin
	sudo 0