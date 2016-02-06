# This file will run through all ALU operations on T0 and T2
cpy $t0 $0 10
cpy $t1 $0 7
# loading 1010 and 0101

cpy $s0 $0
add $s0 $t0
and $s0 $t1
# $s0 would be 0

cpy $s0 $0
add $s0 $t0
orr $s0 $t1
#$s0 should be 15

cpy $s0 $0
add $s0 $t0
xor $s0 $t1
#$s0 should be 15

cpy $s0 $0
add $s0 $t0
not $s0 $0
#should be 1111 1111 1111 0101

cpy $s0 $0
add $s0 $t0
tsc $s0 $0
#should be 1111 1111 1111 0110

cpy $s0 $0
add $s0 $t0
slt $s0 $t1
#should be 0

cpy $s0 $0
add $s0 $t0
sll $s0 1
#should be 20

cpy $s0 $0
add $s0 $t0
srl $s0 1
#should be 7

cpy $s0 $0
add $s0 $t0
sra $s0 1
#should be 7

cpy $s0 $0
add $s0 $t0
add $s0 $t1
# $s0 sould be 17

cpy $s0 $0
add $s0 $t0
sub $s0 $t1
# should be 3

sudo 0