## T-TWINE-80

import math 

def Var_X(f, X, R0, R1, S, BitValue): 
    for round in range(R0, R1): 
        for state in range(S):
            if(state == S-1):
                f.write(X + "_" + str(round) + "_" + str(state) + ": BITVECTOR(" + str(BitValue) + ");\n")
            else:
                f.write(X + "_" + str(round) + "_" + str(state) + ", ")
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
        f.write("ASSERT (" + str_name + " = 0hex" + Value + ");\n") 

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

r1 = 8 #
total_Pr_E1 = 11 #

Deta_E1 = [
            ["000000040000B000", "000000E000BD0000", "00000000000004000000", "00000004000000000000"], 
            ["0000000500002000", "00000060002A0000", "00000000000005000000", "00000005000000000000"], 
            ["0000000E00004000", "000000C0004B0000", "0000000000000E000000", "0000000E000000000000"], 
            ["0000000B0000D000", "0000004000D10000", "0000000000000B000000", "0000000B000000000000"], 
            ["0000000800003000", "00000030003F0000", "00000000000008000000", "00000008000000000000"], 
            ["0000000600005000", "0000005000520000", "00000000000006000000", "00000006000000000000"], 
            ["0000000900008000", "0000007000830000", "00000000000009000000", "00000009000000000000"], 
            ["000000040000B000", "000000B000BD0000", "00000000000004000000", "00000004000000000000"], 
            ["0000000C0000E000", "000000E000E40000", "0000000000000C000000", "0000000C000000000000"], 
            ["000000020000A000", "0000005000A70000", "00000000000002000000", "00000002000000000000"], 
            ["0000000B0000D000", "000000D000D10000", "0000000000000B000000", "0000000B000000000000"], 
            ["0000000E00004000", "00000040004B0000", "0000000000000E000000", "0000000E000000000000"], 
            ["0000000500002000", "00000020002A0000", "00000000000005000000", "00000005000000000000"], 
            ["0000000700009000", "0000009000980000", "00000000000007000000", "00000007000000000000"], 
            ["0000000D00001000", "000000B0001C0000", "0000000000000D000000", "0000000D000000000000"], 
            ["000000030000F000", "0000008000F60000", "00000000000003000000", "00000003000000000000"] 
            ]

for count in range(16): #

    filename2 = "T-TWINE-80_Boomerang_E1_RK_" + str(r1) + "R-" + str(count) + ".cvc"
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

    f2.write("DDT : ARRAY BITVECTOR(8) OF BITVECTOR(4);\n")
    for indc in range(16):
        for outdc in range(16):
            f2.write("ASSERT DDT[0bin" + tobits(indc,4) + tobits(outdc,4) + "] = 0bin" + tobits(DDT[indc][outdc],4) + ";\n")
    f2.write("\n")

    # ********************************************** Lower E1 round function **********************************************

    Var_X(f2, 'E1_K0', 0, r1+1, 20, 4)
    Var_X(f2, 'E1_K2', 0, r1, 20, 4)
    Var_X(f2, 'E1_K1', 0, r1, 2, 4)
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

    Var_X(f2, 'PrK_E1', 0, r1, 2, 4)
    Var_X(f2, 'PrS_E1', 0, r1, 8, 4)

    for round in range(r1):
        states = 0
        for state in [0,16]:
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
        for state in range(2):
            str_Pr += (str_zero + "@PrK_E1_" + str(round) + "_" + str(state) + ", ")

        for state in range(8):
            if(round == r1-1 and state == 7):
                str_Pr += (str_zero + "@PrS_E1_" + str(round) + "_" + str(state))
            else:
                str_Pr += (str_zero + "@PrS_E1_" + str(round) + "_" + str(state) + ", ")

    f2.write("total_Pr : BITVECTOR(" + str(total_Pr_length) + ");\n")
    f2.write("ASSERT total_Pr = BVPLUS(" + str(total_Pr_length) + ", " + str(str_Pr) + ");\n")
    f2.write("ASSERT BVLE(total_Pr, 0bin" + str(tobits(total_Pr_E1,12)) + ");\n\n")

    # ********************************************** Lower E1 init **********************************************

    Set_Init(f2, 'E1_X0', Deta_E1[count][0], 0, 1, 16, 1)
    Set_Init(f2, 'E1_X0', Deta_E1[count][1], r1, r1+1, 16, 1)

    Set_Init(f2, 'E1_K0', Deta_E1[count][2], 0, 1, 20, 1)
    Set_Init(f2, 'E1_K0', Deta_E1[count][3], r1, r1+1, 20, 1)
    f2.write("\n")

    # ********************************************************************************************

    f2.write("QUERY FALSE;\n")
    f2.write("COUNTEREXAMPLE;")
    f2.close()