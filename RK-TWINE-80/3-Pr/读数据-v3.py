fw = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-80/3-Pr/21R/21R_O1/21R_O1_9-4-8_result.cvc", "w") #
f = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-80/3-Pr/21R/21R_O1/21R_O1_9-4-8.cvc") #

Data = [9,4,8] #

count = 0

for line in f.readlines():
    pos = line.find("Upper")
    if(pos >= 0):
        fw.write(line)
    else:
        if(count < 16):
            c1 = ""
            c2 = ""
            
            for i in range( int(len(line)/36) ):
                
                if(i in [0, Data[0]]):
                    c1 += line[i*36 : i*36+16] + ", "
                    c2 += line[i*36+16 : i*36+36] + ", "
            
            fw.write("X_Upper: " + c1 + "\n")
            fw.write("K_Upper: " + c2 + "\n\n")

            count += 1

        else:
            pos = line.find("Lower")
            if(pos >= 0):
                fw.write(line)

            c1 = ""
            c2 = ""
            
            for i in range( int(len(line)/36) ):
                
                if(i in [0, Data[2]]):
                    c1 += line[i*36 : i*36+16] + ", "
                    c2 += line[i*36+16 : i*36+36] + ", "
                
            fw.write("X_Lower: " + c1 + "\n")
            fw.write("K_Lower: " + c2 + "\n\n")

            count += 1

f.close()   
fw.close()

