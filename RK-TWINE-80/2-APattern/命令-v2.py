

for (r0,rm,r1, ASAK) in (
        (9,3,9, 29),
        (8,4,9, 28),
        (9,4,8, 28),
        (8,5,8, 27),
        (7,6,8, 27),
        (8,6,7, 27),
        (7,7,7, 27),
        (0,0,0, 0),
        (7,8,6, 25),
        (6,9,6, 29),
        (0,0,0, 0),
        (6,10,5, 29),
        (0,0,0, 0)
        ):
    
    #'''
    print("mkdir " + str(r0) + "-" + str(rm) + "-" + str(r1))
    print("cp APattern.py " + str(r0) + "-" + str(rm) + "-" + str(r1))
    print("cp run.cpp " + str(r0) + "-" + str(rm) + "-" + str(r1))
    print("cd " + str(r0) + "-" + str(rm) + "-" + str(r1) + "\n")

    print("sed -i 's/(r0,rm,r1) = (8,4,9)/(r0,rm,r1) = (" + str(r0) + "," + str(rm) + "," + str(r1) + ")/g' APattern.py")
    print("sed -i 's/totalASAK = 29/totalASAK = " + str(ASAK) + "/g' APattern.py")


    print("sed -i 's/int r0 = 8;/int r0 = " + str(r0) + ";/g' run.cpp")
    print("sed -i 's/int rm = 4;/int rm = " + str(rm) + ";/g' run.cpp")
    print("sed -i 's/int r1 = 9;/int r1 = " + str(r1) + ";/g' run.cpp")
    print("sed -i 's/int totalASAK = 29;/int totalASAK = " + str(ASAK) + ";/g' run.cpp\n")

    print("python3 APattern.py")
    print("g++ run.cpp")
    print("nohup ./a.out & \n\n")
    #'''

    #print("21R_IO6_" + str(r0) + "-" + str(rm) + "-" + str(r1) + ":")