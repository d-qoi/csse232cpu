cpy $sp 4090 #setting the SP because it is not currently set
cpy $t0 7
w 0($sp) $t0
cpy $t0 $0
r $t0 0($sp)