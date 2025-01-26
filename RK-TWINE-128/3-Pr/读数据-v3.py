fw = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R-AP_result_副本.txt", "w")
f = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R-AP_result.txt")

for line in f.readlines():
    pos = line.find("23R")
    pos1 = line.find("X_Upper")
    pos2 = line.find("X_Lower")
    pos3 = line.find("K_Upper")
    pos4 = line.find("K_Lower")

    c = ""

    if(pos >= 0):
        fw.write(line.strip("\n"))
    
    if(pos1 >= 0):
        c = "[\"" + line.strip("\n")[9:] + "\", "

    if(pos2 >= 0):
        c = "\"" + line.strip("\n")[9:] + "\"],"

    if(pos3 >= 0):
        c = "[\"" + line.strip("\n")[9:] + "\","

    if(pos4 >= 0):
        c = "\"" + line.strip("\n")[9:] + "\"]"
    
    fw.write(c + "\n")
 
 
       

f.close()   
fw.close()
