# testing branching down more than 16
test:
beq $t0 $0 test3
# should become
# 0x3801
# 0x6310


r $t1 0($t1) 
#should become 0x7990

add $t1 $t2 15 
#should become 
# 0x19A9
# 0xF

beq $h1 $t0 test2
# should become 
# 0x2d80

test2:
jr $pc test
# should become 
# 0x63fc

#expanding for testing
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
and $0 $0
test3:
slt $0 $0

#now testing branch up
beq $0 $t1 test3

# don't know what this does
jal test3

#and now testing pushing and poping

psh $t0
pop $t0

# read and write
r $t0 0($sp)
w 0($sp) $t0