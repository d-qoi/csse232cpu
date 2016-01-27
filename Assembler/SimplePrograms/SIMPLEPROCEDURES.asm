# Simple procedure testing

main:
	jal test1
	jal test2
	jal test3
	sudo 0
test1:
	rsh 12
	cpy $h0 1
	sudo 10
	jr $ra
test2:
	rsh 12
	cpy $h0 2
	sudo 10
	jr $ra
test:3
	rsh 12
	cpy $h0 3
	sudo 10
	jr $ra