j 0b2f0160-c6b8-49cc-a28e-6b985632a33c
main:
cpy $t1 10
cpy $h0@8 $t1
psh $t0
psh $t1
psh $ra
jal relPrime
pop $ra
pop $t1
pop $t0
cpy $t0 $h0@9
cpy $h0@9 $t0
jr $ra
0b2f0160-c6b8-49cc-a28e-6b985632a33c:
j f668a7e1-8fcb-4305-9e7b-a296a2124643
relPrime:
cpy $t0 $h0@8
cpy $t1 2
2834f639-653e-4388-b69f-fc9c7f20602c:
cpy $h1@8 $t1
cpy $h0@8 $t0
psh $t0
psh $t1
psh $ra
jal gcd
pop $ra
pop $t1
pop $t0
cpy $t0 $h0@9
cpy $t1 1
beq $t0 $t1 14d6cfd9-3c49-4853-a83d-da8ca1fe2573
add $t1 1
j 2834f639-653e-4388-b69f-fc9c7f20602c
14d6cfd9-3c49-4853-a83d-da8ca1fe2573:
cpy $h0@9 $t1
jr $ra
f668a7e1-8fcb-4305-9e7b-a296a2124643:
j b0ae23d3-b887-4fb0-a619-a23d5095e83d
gcd:
cpy $t1 $h1@8
cpy $t0 $h0@8
bne $t0 $t2 649bf365-2b10-4dad-aab8-d6d7c410bbd5
cpy $h0@9 $t1
jr $ra
649bf365-2b10-4dad-aab8-d6d7c410bbd5:
nop
2e264490-72c4-4ceb-98ff-f7b5230d2a88:
cpy $t2 0
beq $t1 $t2 1b900a70-f64a-4957-99f4-c122f232ccdd
ble $t0 $t1 6cf6b0a5-6d0e-4c29-8bb2-bb7338d40237
sub $t0 $t1
j f3f1dd12-4cc1-431b-ab0e-6a59bc34cae3
6cf6b0a5-6d0e-4c29-8bb2-bb7338d40237:
sub $t1 $t0
f3f1dd12-4cc1-431b-ab0e-6a59bc34cae3:
j 2e264490-72c4-4ceb-98ff-f7b5230d2a88
1b900a70-f64a-4957-99f4-c122f232ccdd:
cpy $h0@9 $t0
jr $ra
b0ae23d3-b887-4fb0-a619-a23d5095e83d:
psh $t2
psh $ra
jal main
pop $ra
pop $t2
cpy $t0 $h0@9
sudo 0
