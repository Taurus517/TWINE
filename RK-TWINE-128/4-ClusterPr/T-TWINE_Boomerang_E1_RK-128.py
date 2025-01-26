## T-TWINE-128

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

r1 = 7 #
total_Pr_E1 = 64 #

Deta_E1 = [
            ["0900807000000000", "0000000000000000", "0000000000000000A000000000000000", "0000000000000A000000000000000000"],
            ["0400B0E000000000", "0000000000000000", "0000000000000000C000000000000000", "0000000000000C000000000000000000"],
            ["0200A05000000000", "0000000000000000", "00000000000000006000000000000000", "00000000000006000000000000000000"],
            ["0F00603000000000", "0000000000000000", "00000000000000008000000000000000", "00000000000008000000000000000000"],
            ["0500206000000000", "0000000000000000", "0000000000000000F000000000000000", "0000000000000F000000000000000000"],
            ["0100C0D000000000", "0000000000000000", "0000000000000000B000000000000000", "0000000000000B000000000000000000"],
            ["0B00D04000000000", "0000000000000000", "0000000000000000E000000000000000", "0000000000000E000000000000000000"],
            ["0D0010B000000000", "0000000000000000", "00000000000000004000000000000000", "00000000000004000000000000000000"],
            ["0800309000000000", "0000000000000000", "00000000000000007000000000000000", "00000000000007000000000000000000"],
            ["070090A000000000", "0000000000000000", "00000000000000002000000000000000", "00000000000002000000000000000000"],
            ["060050F000000000", "0000000000000000", "00000000000000003000000000000000", "00000000000003000000000000000000"],
            ["0300F08000000000", "0000000000000000", "00000000000000009000000000000000", "00000000000009000000000000000000"],
            ["0C00E01000000000", "0000000000000000", "0000000000000000D000000000000000", "0000000000000D000000000000000000"],
            ["0A00702000000000", "0000000000000000", "00000000000000005000000000000000", "00000000000005000000000000000000"],
            ["0E0040C000000000", "0000000000000000", "00000000000000001000000000000000", "00000000000001000000000000000000"]
            ]

for count in range(15): #

    filename2 = "T-TWINE_Boomerang_E1_RK_" + str(r1) + "R-" + str(count) + ".cvc"
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

    # ********************************************** Lower E1 init **********************************************

    Set_Init(f2, 'E1_X0', Deta_E1[count][0], 0, 1, 16, 1)
    Set_Init(f2, 'E1_X0', Deta_E1[count][1], r1, r1+1, 16, 1)

    Set_Init(f2, 'E1_K0', Deta_E1[count][2], 0, 1, 32, 1)
    Set_Init(f2, 'E1_K0', Deta_E1[count][3], r1, r1+1, 32, 1)
    f2.write("\n")

    # ********************************************************************************************

    f2.write("QUERY FALSE;\n")
    f2.write("COUNTEREXAMPLE;")
    f2.close()