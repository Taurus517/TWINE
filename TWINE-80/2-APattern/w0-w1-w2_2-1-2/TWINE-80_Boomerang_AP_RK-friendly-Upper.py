## 2*(E0+E1)+Em
## TWINE-80

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

def RF_UEm(f, X0, X1, X2, X3, RK): 
    for state in range(8):
        f.write("ASSERT (IF ((" + X0 + "_" + str(round) + "_" + str(2*state) + " = 0bin1) OR (" + RK + "_" + str(round) + "_" + str(state) + " = 0bin1)) THEN (" + X3 + "_" + str(round) + "_" + str(state) + " = 0bin1) ELSE (" + X3 + "_" + str(round) + "_" + str(state) + " = 0bin0) ENDIF);\n")
        f.write("ASSERT (IF " + X3 + "_" + str(round) + "_" + str(state) + " = 0bin0 THEN " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
        f.write("ASSERT " + X2 + "_" + str(round) + "_" + str(2*state) + " = " + X0 + "_" + str(round) + "_" + str(2*state) + ";\n")
        f.write("ASSERT (IF ((" + X0 + "_" + str(round) + "_" + str(2*state+1) + " = 0bin1) OR (" + X1 + "_" + str(round) + "_" + str(state) + " = 0bin1)) THEN (" + X2 + "_" + str(round) + "_" + str(2*state+1) + " = 0bin1) ELSE (" + X2 + "_" + str(round) + "_" + str(2*state+1) + " = 0bin0) ENDIF);\n\n")
    for state in range(16):
        f.write("ASSERT " + X0 + "_" + str(round+1) + "_" + str(state) + " = " + X2 + "_" + str(round) + "_" + str(Pi[state]) + ";\n")
    f.write("\n") 

def KeySchedule_E0(f, K0, K1, K2, RK):
    for state in range(8):
        f.write("ASSERT " + RK + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(RK_80[state]) + ";\n")
    f.write("\n") 

    for state in range(2):
        if(state == 0):
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_0 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        else:
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_16 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
    f.write("\n")  

    states = 0
    for state in range(20):
        if(state in [1,4]):
            f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = BVXOR(" + K0 + "_" + str(round) + "_" + str(state) + ", " + K1 + "_" + str(round) + "_" + str(states) + ");\n")
            states += 1
        else:
            f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(state) + ";\n")
    f.write("\n")    

    for state in range(20):
        f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = " + K2 + "_" + str(round) + "_" + str(Rot_80[state]) + ";\n")
    f.write("\n")

def KeySchedule_UEm(f, K0, K1, K2, RK):
    for state in range(8):
        f.write("ASSERT " + RK + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(RK_80[state]) + ";\n")
    f.write("\n") 

    for state in range(2):
        if(state == 0):
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_0 = 0bin0 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
        else:
            f.write("ASSERT (IF " + K0 + "_" + str(round) + "_16 = 0bin0 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n") 
    
    states = 0
    for state in range(20):
        if(state in [1,4]):
            f.write("ASSERT (IF ((" + K0 + "_" + str(round) + "_" + str(state) + " = 0bin1) OR (" + K1 + "_" + str(round) + "_" + str(states) + " = 0bin1)) THEN (" + K2 + "_" + str(round) + "_" + str(state) + " = 0bin1) ELSE (" + K2 + "_" + str(round) + "_" + str(state) + " = 0bin0) ENDIF);\n")
            states += 1
        else:
            f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(state) + ";\n")
    f.write("\n")    

    for state in range(20):
        f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = " + K2 + "_" + str(round) + "_" + str(Rot_80[state]) + ";\n")
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

def RF_LEm(f, X0, X1, X2, X3, RK): 
    for state in range(16):
        f.write("ASSERT " + X2 + "_" + str(round) + "_" + str(state) + " = " + X0 + "_" + str(round) + "_" + str(Pi_inv[state]) + ";\n")
    f.write("\n") 
    for state in range(8):
        f.write("ASSERT (IF ((" + X2 + "_" + str(round) + "_" + str(2*state) + " = 0bin1) OR (" + RK + "_" + str(round) + "_" + str(state) + " = 0bin1)) THEN (" + X3 + "_" + str(round) + "_" + str(state) + " = 0bin1) ELSE (" + X3 + "_" + str(round) + "_" + str(state) + " = 0bin0) ENDIF);\n")
        f.write("ASSERT (IF " + X3 + "_" + str(round) + "_" + str(state) + " = 0bin0 THEN " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
        f.write("ASSERT " + X0 + "_" + str(round+1) + "_" + str(2*state) + " = " + X2 + "_" + str(round) + "_" + str(2*state) + ";\n")
        f.write("ASSERT (IF ((" + X2 + "_" + str(round) + "_" + str(2*state+1) + " = 0bin1) OR (" + X1 + "_" + str(round) + "_" + str(state) + " = 0bin1)) THEN (" + X0 + "_" + str(round+1) + "_" + str(2*state+1) + " = 0bin1) ELSE (" + X0 + "_" + str(round+1) + "_" + str(2*state+1) + " = 0bin0) ENDIF);\n\n")

def KeySchedule_E1(f, K0, K1, K2, RK):
    for state in range(20):
        f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(Rot_80_inv[state]) + ";\n")
    f.write("\n")

    for state in range(2):
        if(state == 0):
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_0 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
        else:
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_16 = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0000 ELSE BVGT(" + K1 + "_" + str(round) + "_" + str(state) + ", 0bin0000) ENDIF);\n")
    f.write("\n")  

    states = 0
    for state in range(20):
        if(state in [1,4]):
            f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = BVXOR(" + K2 + "_" + str(round) + "_" + str(state) + ", " + K1 + "_" + str(round) + "_" + str(states) + ");\n")
            states += 1
        else:
            f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = " + K2 + "_" + str(round) + "_" + str(state) + ";\n")
    f.write("\n")  

    for state in range(8):
        f.write("ASSERT " + RK + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round+1) + "_" + str(RK_80[state]) + ";\n")
    f.write("\n")   

def KeySchedule_LEm(f, K0, K1, K2, RK):
    for state in range(20):
        f.write("ASSERT " + K2 + "_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round) + "_" + str(Rot_80_inv[state]) + ";\n")
    f.write("\n")

    for state in range(2):
        if(state == 0):
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_0 = 0bin0 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
        else:
            f.write("ASSERT (IF " + K2 + "_" + str(round) + "_16 = 0bin0 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n")  

    states = 0
    for state in range(20):
        if(state in [1,4]):
            f.write("ASSERT (IF ((" + K2 + "_" + str(round) + "_" + str(state) + " = 0bin1) OR (" + K1 + "_" + str(round) + "_" + str(states) + " = 0bin1)) THEN (" + K0 + "_" + str(round+1) + "_" + str(state) + " = 0bin1) ELSE (" + K0 + "_" + str(round+1) + "_" + str(state) + " = 0bin0) ENDIF);\n")
            states += 1
        else:
            f.write("ASSERT " + K0 + "_" + str(round+1) + "_" + str(state) + " = " + K2 + "_" + str(round) + "_" + str(state) + ";\n")
    f.write("\n")  

    for state in range(8):
        f.write("ASSERT "+ RK +"_" + str(round) + "_" + str(state) + " = " + K0 + "_" + str(round+1) + "_" + str(RK_80[state]) + ";\n")
    f.write("\n")  

def Join_Em(f, X0, X1, K0, K1): 
    for state in range(20):
        f.write("ASSERT (IF " + K0 + "_" + str(round) + "_" + str(state) + " = 0bin0000 THEN " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + K1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n") 
    for state in range(16):
        f.write("ASSERT (IF " + X0 + "_" + str(round) + "_" + str(state) + " = 0bin0000 THEN " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin0 ELSE " + X1 + "_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n")

def Set_Init(f, X, Value, R, S): 
    str_name = "str_" + X 
    str_name = ""
    for round in range(R-1,R):
        for state in range(S):
            if(state == S-1):
                str_name += (X + "_" + str(round) + "_" + str(state))
            else:
                str_name += (X + "_" + str(round) + "_" + str(state) + " @ ")
        f.write("ASSERT NOT(" + str_name + " = 0hex" + Value + ");\n") 

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

RK_80 = [1, 3, 4, 6, 13, 14, 15, 16]

Rot_80 = [] 
for i in range(4,20):
    Rot_80.append(i)
for i in [1,2,3,0]:
    Rot_80.append(i)

Rot_80_inv = [] 
for i in [19,16,17,18]:
    Rot_80_inv.append(i)
for i in range(0,16):
    Rot_80_inv.append(i)
    
Block = 64
Key = 80

total_RKE0 = 1 #

(r0,rm,r1) = (5,10,6) #
totalASAK = 30 #

filename = "TWINE-80_Boomerang_AP_RK_" + str(r0) + "+" + str(rm) + "+" + str(r1) + "R.cvc"
f = open(filename, "w")

# ********************************************** Upper E0+Em round function **********************************************

Var_X(f, 'E0_K0', 0, r0+1, 20, 4)
Var_X(f, 'E0_RK', 0, r0, 8, 4)
Var_X(f, 'E0_K1', 0, r0, 2, 4)
Var_X(f, 'E0_K2', 0, r0, 20, 4)

Var_X(f, 'UEm_K0', r0, r0+rm+1, 20, 1)
Var_X(f, 'UEm_RK', r0, r0+rm, 8, 1)
Var_X(f, 'UEm_K1', r0, r0+rm, 2, 1)
Var_X(f, 'UEm_K2', r0, r0+rm, 20, 1)

Var_X(f, 'E0_X0', 0, r0+1, 16, 4)
Var_X(f, 'E0_X3', 0, r0, 8, 4)
Var_X(f, 'E0_X1', 0, r0, 8, 4)
Var_X(f, 'E0_X2', 0, r0, 16, 4)

Var_X(f, 'UEm_X0', r0, r0+rm+1, 16, 1)
Var_X(f, 'UEm_X3', r0, r0+rm, 8, 1)
Var_X(f, 'UEm_X1', r0, r0+rm, 8, 1)
Var_X(f, 'UEm_X2', r0, r0+rm, 16, 1)

for round in range(r0+rm):
    f.write("%************************************ Upper E0+Em round = " + str(round+1) + " ************************************\n\n")
    if(round < r0):
        KeySchedule_E0(f, 'E0_K0', 'E0_K1', 'E0_K2', 'E0_RK')
        RF_E0(f, 'E0_X0', 'E0_X1', 'E0_X2', 'E0_X3', 'E0_RK')
    elif(round == r0):
        Join_Em(f, 'E0_X0', 'UEm_X0', 'E0_K0', 'UEm_K0')
        KeySchedule_UEm(f, 'UEm_K0', 'UEm_K1', 'UEm_K2', 'UEm_RK')
        RF_UEm(f, 'UEm_X0', 'UEm_X1', 'UEm_X2', 'UEm_X3', 'UEm_RK')
    else:
        KeySchedule_UEm(f, 'UEm_K0', 'UEm_K1', 'UEm_K2', 'UEm_RK')
        RF_UEm(f, 'UEm_X0', 'UEm_X1', 'UEm_X2', 'UEm_X3', 'UEm_RK')

# ********************************************** Lower Em+E1 round function **********************************************

Var_X(f, 'E1_K0', 0, r1+1, 20, 4)
Var_X(f, 'E1_K2', 0, r1, 20, 4)
Var_X(f, 'E1_K1', 0, r1, 2, 4)
Var_X(f, 'E1_RK', 0, r1, 8, 4)

Var_X(f, 'LEm_K0', r1, r1+rm+1, 20, 1)
Var_X(f, 'LEm_K2', r1, r1+rm, 20, 1)
Var_X(f, 'LEm_K1', r1, r1+rm, 2, 1)
Var_X(f, 'LEm_RK', r1, r1+rm, 8, 1)

Var_X(f, 'E1_X0', 0, r1+1, 16, 4)
Var_X(f, 'E1_X2', 0, r1, 16, 4)
Var_X(f, 'E1_X3', 0, r1, 8, 4)
Var_X(f, 'E1_X1', 0, r1, 8, 4)

Var_X(f, 'LEm_X0', r1, r1+rm+1, 16, 1)
Var_X(f, 'LEm_X2', r1, r1+rm, 16, 1)
Var_X(f, 'LEm_X3', r1, r1+rm, 8, 1)
Var_X(f, 'LEm_X1', r1, r1+rm, 8, 1)

for round in range(r1+rm):
    f.write("%************************************ Lower Em+E1 round = " + str(round+1) + " ************************************\n\n")
    if(round < r1):
        KeySchedule_E1(f, 'E1_K0', 'E1_K1', 'E1_K2', 'E1_RK')
        RF_E1(f, 'E1_X0', 'E1_X1', 'E1_X2', 'E1_X3', 'E1_RK')
    elif(round == r1):
        Join_Em(f, 'E1_X0', 'LEm_X0', 'E1_K0', 'LEm_K0')
        KeySchedule_LEm(f, 'LEm_K0', 'LEm_K1', 'LEm_K2', 'LEm_RK')
        RF_LEm(f, 'LEm_X0', 'LEm_X1', 'LEm_X2', 'LEm_X3', 'LEm_RK')
    else:
        KeySchedule_LEm(f, 'LEm_K0', 'LEm_K1', 'LEm_K2', 'LEm_RK')
        RF_LEm(f, 'LEm_X0', 'LEm_X1', 'LEm_X2', 'LEm_X3', 'LEm_RK')

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

f.write("DDT : ARRAY BITVECTOR(8) OF BITVECTOR(4);\n")
for indc in range(16):
    for outdc in range(16):
        f.write("ASSERT DDT[0bin" + tobits(indc,4) + tobits(outdc,4) + "] = 0bin" + tobits(DDT[indc][outdc],4) + ";\n")
f.write("\n")

# ********************************************** Upper E0+Em DDT **********************************************

Var_X(f, 'AK_E0', 0, r0, 2, 2)
Var_X(f, 'AK_UEm', r0, r0+rm, 2, 2)

Var_X(f, 'AS_E0', 0, r0, 8, 2)
Var_X(f, 'AS_UEm', r0, r0+rm, 8, 2)
for round in range(r0+rm):
    if(round < r0):
        states = 0
        for state in [0,16]:
            f.write("ASSERT (IF E0_K0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN AK_E0_" + str(round) + "_" + str(states) + " = 0bin00 ELSE AK_E0_" + str(round) + "_" + str(states) + " = 0bin10 ENDIF);\n")
            states += 1    
        f.write("\n")

        for state in range(8):
            f.write("ASSERT (IF E0_X3_" + str(round) + "_" + str(state) + " = 0bin0000 THEN AS_E0_" + str(round) + "_" + str(state) + " = 0bin00 ELSE AS_E0_" + str(round) + "_" + str(state) + " = 0bin10 ENDIF);\n")
            f.write("ASSERT NOT(DDT[E0_X3_" + str(round) + "_" + str(state) + " @ E0_X1_" + str(round) + "_" + str(state) + "] = 0bin0001);\n")
        f.write("\n")
    else:
        states = 0
        for state in [0,16]:
            f.write("ASSERT (IF UEm_K0_" + str(round) + "_" + str(state) + " = 0bin0 THEN AK_UEm_" + str(round) + "_" + str(states) + " = 0bin00 ELSE AK_UEm_" + str(round) + "_" + str(states) + " = 0bin01 ENDIF);\n")
            states += 1
        f.write("\n")

        for state in range(8):
            f.write("ASSERT (IF UEm_X3_" + str(round) + "_" + str(state) + " = 0bin0 THEN AS_UEm_" + str(round) + "_" + str(state) + " = 0bin00 ELSE AS_UEm_" + str(round) + "_" + str(state) + " = 0bin01 ENDIF);\n")
        f.write("\n")

# ********************************************** Lower Em+E1 DDT **********************************************

Var_X(f, 'AK_E1', 0, r1, 2, 2)
Var_X(f, 'AK_LEm', r1, r1+rm, 2, 2)

Var_X(f, 'AS_E1', 0, r1, 8, 2)
Var_X(f, 'AS_LEm', r1, r1+rm, 8, 2)
for round in range(r1+rm):
    if(round < r1):
        states = 0
        for state in [0,16]:
            f.write("ASSERT (IF E1_K2_" + str(round) + "_" + str(state) + " = 0bin0000 THEN AK_E1_" + str(round) + "_" + str(states) + " = 0bin00 ELSE AK_E1_" + str(round) + "_" + str(states) + " = 0bin10 ENDIF);\n")
            states += 1
        f.write("\n")

        for state in range(8):
            f.write("ASSERT (IF E1_X3_" + str(round) + "_" + str(state) + " = 0bin0000 THEN AS_E1_" + str(round) + "_" + str(state) + " = 0bin00 ELSE AS_E1_" + str(round) + "_" + str(state) + " = 0bin10 ENDIF);\n")
            f.write("ASSERT NOT(DDT[E1_X3_" + str(round) + "_" + str(state) + " @ E1_X1_" + str(round) + "_" + str(state) + "] = 0bin0001);\n")
        f.write("\n")
    else:
        states = 0
        for state in [0,16]:
            f.write("ASSERT (IF LEm_K2_" + str(round) + "_" + str(state) + " = 0bin0 THEN AK_LEm_" + str(round) + "_" + str(states) + " = 0bin00 ELSE AK_LEm_" + str(round) + "_" + str(states) + " = 0bin01 ENDIF);\n")
            states += 1
        f.write("\n")

        for state in range(8):
            f.write("ASSERT (IF LEm_X3_" + str(round) + "_" + str(state) + " = 0bin0 THEN AS_LEm_" + str(round) + "_" + str(state) + " = 0bin00 ELSE AS_LEm_" + str(round) + "_" + str(state) + " = 0bin01 ENDIF);\n")
        f.write("\n")

# ********************************************** Em totalAS, total AK **********************************************

Var_X(f, 'AK_Em', 0, rm, 2, 2)
Var_X(f, 'AS_Em', 0, rm, 8, 2)
rounds = r1+rm-1
for round in range(r0, r0+rm):
    for state in range(2):
        f.write("ASSERT (IF ((AK_UEm_" + str(round) + "_" + str(state) + " = 0bin01) AND (AK_LEm_" + str(rounds) + "_" + str(state) + " = 0bin01)) THEN (AK_Em_" + str(round-r0) + "_" + str(state) + " = 0bin01) ELSE (AK_Em_" + str(round-r0) + "_" + str(state) + " = 0bin00) ENDIF);\n")
    f.write("\n")

    for state in range(8):
        f.write("ASSERT (IF ((AS_UEm_" + str(round) + "_" + str(state) + " = 0bin01) AND (AS_LEm_" + str(rounds) + "_" + str(state) + " = 0bin01)) THEN (AS_Em_" + str(round-r0) + "_" + str(state) + " = 0bin01) ELSE (AS_Em_" + str(round-r0) + "_" + str(state) + " = 0bin00) ENDIF);\n")

    rounds -= 1
    f.write("\n")

# ********************************************** E0+Em+E1 totalAS, totalAK **********************************************

total_ASAK_length = 12
str_zero = "0bin"
str_ASAK = ""

for length in range(total_ASAK_length-2):
    str_zero += "0"

for round in range(r0):
    for state in range(2):
        str_ASAK += (str_zero + "@AK_E0_" + str(round) + "_" + str(state) + ", ")

    for state in range(8):
        str_ASAK += (str_zero + "@AS_E0_" + str(round) + "_" + str(state) + ", ")

for round in range(r1):
    for state in range(2):
        str_ASAK += (str_zero + "@AK_E1_" + str(round) + "_" + str(state) + ", ")

    for state in range(8):
        str_ASAK += (str_zero + "@AS_E1_" + str(round) + "_" + str(state) + ", ")

for round in range(rm):
    for state in range(2):
        str_ASAK += (str_zero + "@AK_Em_" + str(round) + "_" + str(state) + ", ")

    for state in range(8):
        if(round == rm-1 and state == 7):
            str_ASAK += (str_zero + "@AS_Em_" + str(round) + "_" + str(state))
        else:
            str_ASAK += (str_zero + "@AS_Em_" + str(round) + "_" + str(state) + ", ")

f.write("total_ASAK : BITVECTOR(" + str(total_ASAK_length) + ");\n")
f.write("ASSERT total_ASAK = BVPLUS(" + str(total_ASAK_length) + ", " + str(str_ASAK) + ");\n")
f.write("ASSERT BVLE(total_ASAK, 0bin" + str(tobits(totalASAK,12)) + ");\n\n")

# ********************************************** E0+E1 setting **********************************************

Set_Init(f, 'E0_K0', '00000000000000000000', 1, 20)
Set_Init(f, 'E1_K0', '00000000000000000000', 1, 20)
f.write("\n")

# ********************************************** friendly key recovery **********************************************

Var_X(f, 'RK_E0', 0, 1, 16, 1)

for state in range(16):
    f.write("ASSERT (IF E0_X0_0_" + str(state) + " = 0bin0000 THEN RK_E0_0_" + str(state) + " = 0bin0 ELSE RK_E0_0_" + str(state) + " = 0bin1 ENDIF);\n")
f.write("\n")

total_RK_length = 8
str_zero = "0bin"
str_RK = ""

for length in range(total_RK_length-1):
    str_zero += "0"

for state in range(16):
    if(state == 15):
        str_RK += (str_zero + "@RK_E0_0_" + str(state))
    else:
        str_RK += (str_zero + "@RK_E0_0_" + str(state) + ", ")

f.write("total_RK : BITVECTOR(" + str(total_RK_length) + ");\n")
f.write("ASSERT total_RK = BVPLUS(" + str(total_RK_length) + ", " + str(str_RK) + ");\n")
f.write("ASSERT total_RK = 0bin" + str(tobits(total_RKE0, 8)) + ";\n\n")

# ********************************************** APattern **********************************************

Var_X(f, 'APE0_X0', 0, r0+1, 16, 1)
Var_X(f, 'APE1_X0', 0, r1+1, 16, 1)

Var_X(f, 'APE0_K0', 0, r0+1, 20, 1)
Var_X(f, 'APE1_K0', 0, r1+1, 20, 1)

for round in range(r0+1):
    for state in range(16):
        f.write("ASSERT (IF E0_X0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE0_X0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE0_X0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n")

    for state in range(20):
        f.write("ASSERT (IF E0_K0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE0_K0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE0_K0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n")

for round in range(r1+1):
    for state in range(16):
        f.write("ASSERT (IF E1_X0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE1_X0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE1_X0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n")

    for state in range(20):
        f.write("ASSERT (IF E1_K0_" + str(round) + "_" + str(state) + " = 0bin0000 THEN APE1_K0_" + str(round) + "_" + str(state) + " = 0bin0 ELSE APE1_K0_" + str(round) + "_" + str(state) + " = 0bin1 ENDIF);\n")
    f.write("\n")

# ********************************************************************************************

f.write("QUERY FALSE;\n")
f.write("COUNTEREXAMPLE;")
f.close()