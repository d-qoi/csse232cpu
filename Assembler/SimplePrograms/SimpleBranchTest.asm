start:
	cpy $t0 $0
	cpy $t1 10
	beq $t0 $t1 end
	bne $t0 $t1 end
	and $0 $0
	and $0 $0
	and $0 $0
	and $0 $0
	j start
end:
	beq $t0 $0 realend
	and $0 $0
	and $0 $0
	and $0 $0
	and $0 $0
realend:
	and $0 $0
	and $0 $0
	and $0 $0
	and $0 $0
	sudo 0