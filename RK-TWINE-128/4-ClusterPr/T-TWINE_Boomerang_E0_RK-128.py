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

r0 = 4 #
total_Pr_E0 = 10 #

Deta_E0 = [
            ["0000000065002A05", "0000000000000000", "00000000000000000000000000000F00", "0000000000000F000000000000000000"],
            ["00000000A7009807", "0000000000000000", "00000000000000000000000000000200", "00000000000002000000000000000000"],
            ["000000003F00650F", "0000000000000000", "00000000000000000000000000000800", "00000000000008000000000000000000"],
            ["000000005200A702", "0000000000000000", "00000000000000000000000000000600", "00000000000006000000000000000000"],
            ["000000002A00790A", "0000000000000000", "00000000000000000000000000000500", "00000000000005000000000000000000"],
            ["00000000E400BD04", "0000000000000000", "00000000000000000000000000000C00", "0000000000000C000000000000000000"],
            ["0000000098003F08", "0000000000000000", "00000000000000000000000000000700", "00000000000007000000000000000000"],
            ["0000000079008309", "0000000000000000", "00000000000000000000000000000A00", "0000000000000A000000000000000000"],
            ["00000000BD001C0D", "0000000000000000", "00000000000000000000000000000400", "00000000000004000000000000000000"],
            ["00000000F6005206", "0000000000000000", "00000000000000000000000000000300", "00000000000003000000000000000000"],
            ["000000001C00E40C", "0000000000000000", "00000000000000000000000000000D00", "0000000000000D000000000000000000"],
            ["00000000D100CE01", "0000000000000000", "00000000000000000000000000000B00", "0000000000000B000000000000000000"],
            ["000000004B00D10B", "0000000000000000", "00000000000000000000000000000E00", "0000000000000E000000000000000000"],
            ["000000008300F603", "0000000000000000", "00000000000000000000000000000900", "00000000000009000000000000000000"],
            ["00000000CE004B0E", "0000000000000000", "00000000000000000000000000000100", "00000000000001000000000000000000"]
          ]

for count in range(15): #

    filename1 = "T-TWINE-128_Boomerang_E0_RK_" + str(r0) + "R-" + str(count) + ".cvc"
    f1 = open(filename1, "w")

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
    for indc in range(16):
        for outdc in range(16):
            f1.write("ASSERT DDT[0bin" + tobits(indc,4) + tobits(outdc,4) + "] = 0bin" + tobits(DDT[indc][outdc],4) + ";\n")
    f1.write("\n")

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

    # ********************************************** Upper E0 Init **********************************************

    Set_Init(f1, 'E0_X0', Deta_E0[count][0], 0, 1, 16, 1)
    Set_Init(f1, 'E0_X0', Deta_E0[count][1], r0, r0+1, 16, 1)

    Set_Init(f1, 'E0_K0', Deta_E0[count][2], 0, 1, 32, 1)
    Set_Init(f1, 'E0_K0', Deta_E0[count][3], r0, r0+1, 32, 1)
    f1.write("\n")

    # ********************************************************************************************

    f1.write("QUERY FALSE;\n")
    f1.write("COUNTEREXAMPLE;")
    f1.close()