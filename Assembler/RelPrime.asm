RelPrime:
	rsh	4				#set schwap
	cpy	$h0 $ra			#save $ra
	rsh 8
	cpy	$s0 $h0			#copy n out of schwap
	cpy	$s1 0x2			#load 2 to m
While:
	rsh	8				#set schwap to args
	cpy	$h0 $s0			#set a0 to n
	cpy	$h1 $s1			#set a1 to m
	jal	GCD				#call GCD
	rsh	9				#set schwap
	cpy	$t0 0x1			#load immediate 0x1 to t0
	bne	$h0 $t0 Done	#branch to done if r0 != 1
	add	$s1 0x1			#add 1 to m
	j	While			#jump to the start of the loop
Done:
	rsh	9				#load return registers
	cpy	$h0 $s1			#set r0 to m
	rsh	4				#set schwap
	cpy	$ra $h0			#reload $ra
	jr	$ra 0			#return to the previous function
GCD:
	rsh	8				#schwap to argument register
Base:
	bne	$h0 $z0 GMain	#a!=0 go to GMain
	cpy	$t0 $h1			#copy h1 to t0 for RSH
	rsh	9				#schwap to return registers
	cpy	$h0 $t0			#load t0 to r1
	jr	$ra 0			#return
GMain:
	beq	$h1 $z0 Exit	#jump to exit if b is zero
	bgt	$h0 $h1 If		#jump to If if a>b
Else:
	sub	$h1 $h0			#else: b=b-a
	j	GMain			#loop
If:
	sub	$h0 $h1			#if: a=a-b
	j	GMain			#loop
Exit:
	cpy	$t0 $h0			#copy h0 to t0 for rsh schwap
	rsh	9				#make sure we're in the right spot
	cpy	$h0 $t0			#copy t0 to h0
	jr	$ra	0			#return