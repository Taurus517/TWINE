fw = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-80/2-APattern/w0-w1-w2_2-1-2/21R-AP_result.txt", "w")
f = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-80/2-APattern/w0-w1-w2_2-1-2/21R-AP.txt")

Data = [[5,10,6],
        
        [9,3,9],
        [8,4,9],
        [9,4,8],
        [8,5,8],
        [7,6,8],
        [8,6,7],
        [7,7,7],
        [6,8,7],

        [9,3,9],
        [8,4,9],
        [9,4,8],
        [8,5,8],
        [7,6,8],
        [8,6,7],
        [7,7,7],
        [7,8,6],
        [6,9,6],
        [5,10,6],
        [6,10,5],
        [5,11,5],

        [7,7,7],

        [9,4,8],
        [7,6,8],
        [6,8,7],
        [7,8,6],
        [6,9,6],

        [6,10,5]
        ]

count = 0

for line in f.readlines():
    pos = line.find("21R")

    if(pos >= 0):
        fw.write(line)
        count += 1
        
    else:
        c1 = ""
        c2 = ""

        for i in range( int(len(line) / 36) ):
            if(i == Data[count-1][0]):
                c1 += line[i*36 : i*36+16] + ", \nX_Lower: "
                c2 += line[i*36+16 : i*36+36] + ", \nK_Lower: "
            else:
                c1 += line[i*36 : i*36+16] + ", "
                c2 += line[i*36+16 : i*36+36] + ", "
                
        fw.write("X_Upper: " + c1 + "\n")
        fw.write("K_Upper: " + c2 + "\n\n")

f.close()   
fw.close()
