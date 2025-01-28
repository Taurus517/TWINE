## TWINE-128

import math 

def Var_X(f, X, R0, R1, S, BitValue): 
    for round in range(R0, R1): 
        for state in range(S):
            if(state == S-1):
                f.write(X + "_" + str(round) + "_" + str(state) + ": BITVECTOR(" + str(BitValue) + ");\n")
            else:
                f.write(X + "_" + str(round) + "_" + str(state) + ", ")
    f.write("\n")

def RF_E0(f, X0, X1, X2, X3, RK): 
    for state in range(8):
        f.write("ASSERT " + X3 + "_" + str(round) + "_" + str(state) + " = BVXOR(" + X0 + "_" + str(round) + "_" + str(2*state) + ", " + RK + "_" + str(round) + "_" + str(state) + ");\n")
        f.write("ASSERT (IF " + X3 + "_" + str(round) + "_" + str(state) + " = 0bin0000 THEN " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + X1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        f.write("ASSERT " + X2 + "_" + str(round) + "_" + str(2*state) + " = " + X0 + "_" + str(round) + "_" + str(2*state) + ";\n")
        f.write("ASSERT " + X2 + "_" + str(round) + "_" + str(2*state+1) + " = BVXOR(" + X0 + "_" + str(round) + "_" + str(2*state+1) + ", " + X1 + "_" + str(round) + "_" + str(state) + ");\n\n")
    for state in range(16):
        f.write("ASSERT " + X0 + "_" + str(round+1) + "_" + str(state) + " = " + X2 + "_" + str(round) + "_" + str(Pi[state]) + ";\n")
    f.write("\n") 

def KeySchedule_E0(f, K0, K1, K2, RK):
    for state in range(8):
        f.write("ASSERT " + RK + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(RK_128[state]) + ";\n")
    f.write("\n") 

    for state in range(3):
        if(state == 0):
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_0 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        elif(state == 1):
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_16 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        else:
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_30 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
    f.write("\n")  

    states = 0
    for state in range(32):
        if(state in [1,4,23]):
            f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = BVXOR(" + K0 + "_" + str(round) + "_" + str(state) + ", " + K1 + "_" + str(round) + "_" + str(states) + ");\n")
            states += 1
        else:
            f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(state) + ";\n")
    f.write("\n")    

    for state in range(32):
        f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = " + K2 + "_" + str(round) + "_" + str(Rot_128[state]) + ";\n")
    f.write("\n")

def RF_E1(f, X0, X1, X2, X3, RK): 
    for state in range(16):
        f.write("ASSERT " + X2 + "_" + str(round) + "_" + str(state) + " = " + X0 + "_" + str(round) + "_" + str(Pi_inv[state]) + ";\n")
    f.write("\n") 
    for state in range(8):
        f.write("ASSERT " + X3 + "_" + str(round) + "_" + str(state) + " = BVXOR(" + X2 + "_" + str(round) + "_" + str(2*state) + ", " + RK + "_" + str(round) + "_" + str(state) + ");\n")
        f.write("ASSERT (IF " + X3 + "_" + str(round) + "_" + str(state) + " = 0bin0000 THEN " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + X1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        f.write("ASSERT " + X0 + "_" + str(round+1) + "_" + str(2*state) + " = " + X2 + "_" + str(round) + "_" + str(2*state) + ";\n")
        f.write("ASSERT " + X0 + "_" + str(round+1) + "_" + str(2*state+1) + " = BVXOR(" + X2 + "_" + str(round) + "_" + str(2*state+1) + ", " + X1 + "_" + str(round) + "_" + str(state) + ");\n\n")

def KeySchedule_E1(f, K0, K1, K2, RK):
    for state in range(32):
        f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(Rot_128_inv[state]) + ";\n")
    f.write("\n")

    for state in range(3):
        if(state == 0):
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_0 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        elif(state == 1):
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_16 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        else:
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_30 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
    f.write("\n")  

    states = 0
    for state in range(32):
        if(state in [1,4,23]):
            f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = BVXOR(" + K2 + "_" + str(round) + "_" + str(state) + ", " + K1 + "_" + str(round) + "_" + str(states) + ");\n")
            states += 1
        else:
            f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = " + K2 + "_" + str(round) + "_" + str(state) + ";\n")
    f.write("\n")  

    for state in range(8):
        f.write("ASSERT " + RK + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round+1) + "_" + str(RK_128[state]) + ";\n")
    f.write("\n")   

def Set_Init(f, X, Value, R0, R1, S, Choice): 
    str_name = "str_" + X 
    str_name = ""
    for round in range(R0, R1):
        for state in range(S):
            if(round == R1-1 and state == S-1):
                str_name += (X + "_" + str(round) + "_" + str(state))
            else:
                str_name += (X + "_" + str(round) + "_" + str(state) + " @ ")
    if(Choice==0):
        f.write("ASSERT NOT(" + str_name + " = 0hex" + Value + ");\n") 
    elif(Choice==1):
        f.write("ASSERT (" + str_name + " = 0bin" + Value + ");\n") 

def tobits(num, bit_num):
	res = ""
	
	for pos in range(bit_num):
		res = str(num % 2) + res
		num = int(num / 2)
	
	return res

# ********************************************** Initial Setting **********************************************

Sbox = [0xC, 0x0, 0xF, 0xA, 0x2, 0xB, 0x9, 0x5,
        0x8, 0x3, 0xD, 0x7, 0x1, 0xE, 0x6, 0x4]

Pi = [1, 2, 11, 6, 3, 0, 9, 4, 7, 10, 13, 14, 5, 8, 15, 12]
Pi_inv = [5, 0, 1, 4, 7, 12, 3, 8, 13, 6, 9, 2, 15, 10, 11, 14]

RK_128 = [2, 3, 12, 15, 17, 18, 28, 31]

Rot_128 = [] 
for i in range(4,32):
    Rot_128.append(i)
for i in [1,2,3,0]:
    Rot_128.append(i)

Rot_128_inv = [] 
for i in [31,28,29,30]:
    Rot_128_inv.append(i)
for i in range(0,28):
    Rot_128_inv.append(i)
    
Block = 64
Key = 128

(r0,r1) = (0,0) #

(total_Pr_E0, total_Pr_E1) = (0, 0) #

Data = [
["0000000000000111000000000011000000000000010000000000000000000000", 
"0100101000000000001000000100000000000000001000000000000000000000"],
["00000000000000000000000001000000000000000000000000000100000000000000000000000000010000000000000000000000000001000000000000000000",
"00000000000000001000000000000000000000000000000000001000000000000000000000000000000000001000000000000000000000000000000000001000"]
]


filename1 = "./Upper/TWINE-128_Boomerang_Pr_RK_" + str(r0) + "R_Upper_" + str(total_Pr_E0) + "Pr.cvc"
f1 = open(filename1, "w")

filename2 = "./Lower/TWINE-128_Boomerang_Pr_RK_" + str(r1) + "R_Lower_" + str(total_Pr_E1) + "Pr.cvc"
f2 = open(filename2, "w")


# ********************************************** DDT **********************************************

DDT = [[0 for indc in range(16)] for outdc in range(16)]

for indc in range(16):
    for outdc in range(16):
        for input in range(16):
            if ((Sbox[input] ^ Sbox[input^indc]) == outdc):
                DDT[indc][outdc] += 1 ## 0,2,4,16

for indc in range(16):
    for outdc in range(16):
        if(DDT[indc][outdc] != 0):
            DDT[indc][outdc] = int(abs(math.log2(DDT[indc][outdc])-4)) ## 0,2,3
        else:
            DDT[indc][outdc] = 1 ## -

f1.write("DDT : ARRAY BITVECTOR(8) OF BITVECTOR(4);\n")
f2.write("DDT : ARRAY BITVECTOR(8) OF BITVECTOR(4);\n")
for indc in range(16):
    for outdc in range(16):
        f1.write("ASSERT DDT[0bin" + tobits(indc,4) + tobits(outdc,4) + "] = 0bin" + tobits(DDT[indc][outdc],4) + ";\n")
        f2.write("ASSERT DDT[0bin" + tobits(indc,4) + tobits(outdc,4) + "] = 0bin" + tobits(DDT[indc][outdc],4) + ";\n")
f1.write("\n")
f2.write("\n")


# ********************************************** Upper E0 round function **********************************************

Var_X(f1, 'E0_K0', 0, r0+1, 32, 4)
Var_X(f1, 'E0_RK', 0, r0, 8, 4)
Var_X(f1, 'E0_K1', 0, r0, 3, 4)
Var_X(f1, 'E0_K2', 0, r0, 32, 4)

Var_X(f1, 'E0_X0', 0, r0+1, 16, 4)
Var_X(f1, 'E0_X3', 0, r0, 8, 4)
Var_X(f1, 'E0_X1', 0, r0, 8, 4)
Var_X(f1, 'E0_X2', 0, r0, 16, 4)

for round in range(r0):
    f1.write("%************************************ Upper E0 round = " + str(round+1) + " ************************************\n\n")
   
    KeySchedule_E0(f1, 'E0_K0', 'E0_K1', 'E0_K2', 'E0_RK')
    RF_E0(f1, 'E0_X0', 'E0_X1', 'E0_X2', 'E0_X3', 'E0_RK')
    
# ********************************************** Upper E0 DDT **********************************************

Var_X(f1, 'PrK_E0', 0, r0, 3, 4)
Var_X(f1, 'PrS_E0', 0, r0, 8, 4)

for round in range(r0):
    states = 0
    for state in [0,16,30]:
        f1.write("ASSERT (IF E0_K0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN PrK_E0_" + str(round) + "_" + str(states) + " = 0bin0000 ELSE PrK_E0_" + str(round) + "_" + str(states) + " = DDT[E0_K0_" + str(round) + "_" + str(state) + " @ E0_K1_" + str(round) + "_" + str(states) + "] ENDIF);\n")
        f1.write("ASSERT NOT(DDT[E0_K0_" + str(round) + "_" + str(state) + " @ E0_K1_" + str(round) + "_" + str(states) + "] = 0bin0001);\n")
        states += 1    
    f1.write("\n")

    for state in range(8):
        f1.write("ASSERT (IF E0_X3_" + str(round) + "_" + str(state) + " = 0bin0000 THEN PrS_E0_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE PrS_E0_" + str(round) + "_" + str(state) + " = DDT[E0_X3_" + str(round) + "_" + str(state) + " @ E0_X1_" + str(round) + "_" + str(state) + "] ENDIF);\n")
        f1.write("ASSERT NOT(DDT[E0_X3_" + str(round) + "_" + str(state) + " @ E0_X1_" + str(round) + "_" + str(state) + "] = 0bin0001);\n")
    f1.write("\n")

# ********************************************** E0 totalPr **********************************************

total_Pr_length = 12
str_zero = "0bin"
str_Pr = ""

for length in range(total_Pr_length-4):
    str_zero += "0"

for round in range(r0):
    for state in range(3):
        str_Pr += (str_zero + "@PrK_E0_" + str(round) + "_" + str(state) + ", ")

    for state in range(8):
        if(round == r0-1 and state == 7):
            str_Pr += (str_zero + "@PrS_E0_" + str(round) + "_" + str(state))
        else:
            str_Pr += (str_zero + "@PrS_E0_" + str(round) + "_" + str(state) + ", ")

f1.write("total_Pr : BITVECTOR(" + str(total_Pr_length) + ");\n")
f1.write("ASSERT total_Pr = BVPLUS(" + str(total_Pr_length) + ", " + str(str_Pr) + ");\n")
f1.write("ASSERT BVLE(total_Pr, 0bin" + str(tobits(total_Pr_E0,12)) + ");\n\n")

# ********************************************** Upper E0 APattern **********************************************

Var_X(f1, 'APE0_X0', 0, r0+1, 16, 1)
Var_X(f1, 'APE0_K0', 0, r0+1, 32, 1)

for round in range(r0+1):
    for state in range(16):
        f1.write("ASSERT (IF E0_X0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE0_X0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE0_X0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f1.write("\n")

    for state in range(32):
        f1.write("ASSERT (IF E0_K0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE0_K0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE0_K0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f1.write("\n")


Set_Init(f1, 'APE0_X0', Data[0][0], 0,r0+1, 16, 1)
Set_Init(f1, 'APE0_K0', Data[1][0], 0,r0+1, 32, 1)
f1.write("\n")

# ********************************************************************************************

f1.write("QUERY FALSE;\n")
f1.write("COUNTEREXAMPLE;")
f1.close()



# ********************************************** Lower E1 round function **********************************************

Var_X(f2, 'E1_K0', 0, r1+1, 32, 4)
Var_X(f2, 'E1_K2', 0, r1, 32, 4)
Var_X(f2, 'E1_K1', 0, r1, 3, 4)
Var_X(f2, 'E1_RK', 0, r1, 8, 4)

Var_X(f2, 'E1_X0', 0, r1+1, 16, 4)
Var_X(f2, 'E1_X2', 0, r1, 16, 4)
Var_X(f2, 'E1_X3', 0, r1, 8, 4)
Var_X(f2, 'E1_X1', 0, r1, 8, 4)

for round in range(r1):
    f2.write("%************************************ Lower E1 round = " + str(round+1) + " ************************************\n\n")
    
    KeySchedule_E1(f2, 'E1_K0', 'E1_K1', 'E1_K2', 'E1_RK')
    RF_E1(f2, 'E1_X0', 'E1_X1', 'E1_X2', 'E1_X3', 'E1_RK')
    
# ********************************************** Lower E1 DDT **********************************************

Var_X(f2, 'PrK_E1', 0, r1, 3, 4)
Var_X(f2, 'PrS_E1', 0, r1, 8, 4)

for round in range(r1):
    states = 0
    for state in [0,16,30]:
        f2.write("ASSERT (IF E1_K2_" + str(round) + "_" + str(state) + " = 0bin0000 THEN PrK_E1_" + str(round) + "_" + str(states) + " = 0bin0000 ELSE PrK_E1_" + str(round) + "_" + str(states) + " = DDT[E1_K2_" + str(round) + "_" + str(state) + " @ E1_K1_" + str(round) + "_" + str(states) + "] ENDIF);\n")
        f2.write("ASSERT NOT(DDT[E1_K2_" + str(round) + "_" + str(state) + " @ E1_K1_" + str(round) + "_" + str(states) + "] = 0bin0001);\n")
        states += 1
    f2.write("\n")

    for state in range(8):
        f2.write("ASSERT (IF E1_X3_" + str(round) + "_" + str(state) + " = 0bin0000 THEN PrS_E1_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE PrS_E1_" + str(round) + "_" + str(state) + " = DDT[E1_X3_" + str(round) + "_" + str(state) + " @ E1_X1_" + str(round) + "_" + str(state) + "] ENDIF);\n")
        f2.write("ASSERT NOT(DDT[E1_X3_" + str(round) + "_" + str(state) + " @ E1_X1_" + str(round) + "_" + str(state) + "] = 0bin0001);\n")
    f2.write("\n")

# ********************************************** E1 totalPr **********************************************

total_Pr_length = 12
str_zero = "0bin"
str_Pr = ""

for length in range(total_Pr_length-4):
    str_zero += "0"

for round in range(r1):
    for state in range(3):
        str_Pr += (str_zero + "@PrK_E1_" + str(round) + "_" + str(state) + ", ")

    for state in range(8):
        if(round == r1-1 and state == 7):
            str_Pr += (str_zero + "@PrS_E1_" + str(round) + "_" + str(state))
        else:
            str_Pr += (str_zero + "@PrS_E1_" + str(round) + "_" + str(state) + ", ")

f2.write("total_Pr : BITVECTOR(" + str(total_Pr_length) + ");\n")
f2.write("ASSERT total_Pr = BVPLUS(" + str(total_Pr_length) + ", " + str(str_Pr) + ");\n")
f2.write("ASSERT BVLE(total_Pr, 0bin" + str(tobits(total_Pr_E1,12)) + ");\n\n")

# ********************************************** Lower E1 APattern **********************************************

Var_X(f2, 'APE1_X0', 0, r1+1, 16, 1)
Var_X(f2, 'APE1_K0', 0, r1+1, 32, 1)

for round in range(r1+1):
    for state in range(16):
        f2.write("ASSERT (IF E1_X0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE1_X0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE1_X0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f2.write("\n")

    for state in range(32):
        f2.write("ASSERT (IF E1_K0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE1_K0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE1_K0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f2.write("\n")

Set_Init(f2, 'APE1_X0', Data[0][1], 0,r1+1, 16, 1)
Set_Init(f2, 'APE1_K0', Data[1][1], 0,r1+1, 32, 1)
f2.write("\n")

# ********************************************************************************************

f2.write("QUERY FALSE;\n")
f2.write("COUNTEREXAMPLE;")
f2.close()