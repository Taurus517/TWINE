

for (r0,rm,r1, ASAK) in (
        (7,9,8, 30),
        (8,9,7, 30),
        (7,10,7, 29),
        (6,11,7, 29),
        (7,11,6, 29),
        (6,12,6, 29),
        (5,13,6, 29),
        (6,13,5, 29),
        (5,14,5, 29),
        (4,15,5, 29),
        (5,15,4, 29),
        (4,16,4, 29),
        (3,17,4, 29),
        (4,17,3, 29),
        (3,18,3, 29)
        ):
    
    #'''
    print("mkdir " + str(r0) + "-" + str(rm) + "-" + str(r1))
    print("cp APattern.py " + str(r0) + "-" + str(rm) + "-" + str(r1))
    print("cp run.cpp " + str(r0) + "-" + str(rm) + "-" + str(r1))
    print("cd " + str(r0) + "-" + str(rm) + "-" + str(r1) + "\n")

    print("sed -i 's/(r0,rm,r1) = (0,0,0)/(r0,rm,r1) = (" + str(r0) + "," + str(rm) + "," + str(r1) + ")/g' APattern.py")
    print("sed -i 's/totalASAK = 0/totalASAK = " + str(ASAK) + "/g' APattern.py")


    print("sed -i 's/int r0 = 0;/int r0 = " + str(r0) + ";/g' run.cpp")
    print("sed -i 's/int rm = 0;/int rm = " + str(rm) + ";/g' run.cpp")
    print("sed -i 's/int r1 = 0;/int r1 = " + str(r1) + ";/g' run.cpp")
    print("sed -i 's/int totalASAK = 0;/int totalASAK = " + str(ASAK) + ";/g' run.cpp\n")

    print("python3 APattern.py")
    print("g++ run.cpp")
    print("nohup ./a.out & \n\n")

    print("cd .. \n\n")
    #'''

    #print("21R_IO6_" + str(r0) + "-" + str(rm) + "-" + str(r1) + ":")