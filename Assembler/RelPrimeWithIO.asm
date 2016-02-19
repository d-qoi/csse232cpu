Main:
	cpy $h0@8 $h1@11
	jal RELPrime
	and $0 $0
	cpy $h1@11 $h0@9
	sudo 0
RELPrime:
	rsh	4
	cpy $h0 $ra
	rsh 8
	cpy $s0 $h0
	cpy $s1 2
RELPrimeWhile:
	rsh 8
	cpy $h0 $s0
	cpy $h1 $s1
	jal GCD
	rsh 9
	cpy $t0 1
	beq $h0 $t0 RELPrimeRet
	add $s1 1
	j RELPrimeWhile
RELPrimeRet:
	rsh 9
	cpy $h0 $s1
	rsh 4
	jr $h0 0
GCD:
	rsh 8
	beq $h0 $0 GCDReturn
GCDWhile:
	beq $h1 $0 GCDReturn
	bgt $h0 $h1 GCDif
GCDelse:
	sub $h1 $h0
	j GCDWhile
GCDif:
	sub $h0 $h1
	j GCDWhile
GCDReturn:
	rsh 8
	cpy $t0 $h0
	rsh 9
	cpy $h0 $t0
	jr $ra 0
