
'''
f1 = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R/IO_6/3-17-3/T-TWINE-128_Boomerang_Pr_RK_3R_Upper_6Pr.cvc")
f2 = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R/IO_6/3-17-3/T-TWINE-128_Boomerang_Pr_RK_3R_Lower_6Pr.cvc")

fw = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R/23R_Pr_result", "a+")

fw.write("23R_IO6_3-17-3_Upper: \n")
str_find1 = "hex"
str_find2 = ")"
for line in f1.readlines():
    pos1 = line.find(str_find1)
    pos2 = line.find(str_find2)
    if(pos1 >= 0):
        fw.write(line[pos1+3:pos2]+"\n")  

fw.write("23R_IO6_3-17-3_Lower: \n")
for line in f2.readlines():
    pos1 = line.find(str_find1)
    pos2 = line.find(str_find2)
    if(pos1 >= 0):
        fw.write(line[pos1+3:pos2]+"\n")        

fw.close()

f1.close()    
f2.close()      
'''

f = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R/23R_Pr")
#fw = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R/23R_Pr_result", "w")
fw = open("/Users/wangchen/Desktop/T-TWINE/程序/RK-T-TWINE-128/3-Pr/23R/23R_Pr_result_副本.txt", "w")

str_find = "23R"
for line in f.readlines():
    pos = line.find(str_find)
    if(pos >= 0):
        fw.write(line)
    else:
        len1 = len(line)-1
        #fw.write(line[0:16] + "," + line[16:48] + ",   " + line[len1-48:len1-32] + "," + line[len1-32:len1] + "\n")  
        fw.write("{" + line[len1-48:len1-32] + "},   {" + line[len1-32:len1] + "}\n")  

fw.close()

f.close()    

