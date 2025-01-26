import math

fr = open("result.txt1")

TrueCount = 0
for line in fr.readlines():

    str_find = "TrueCount: "
    pos = line.find(str_find)
    if(pos >= 0):
        str_True = line[pos+len(str_find):len(line)]
        TrueCount += int(str_True)

fr.close()   

print("Pr_Em: ", math.log2(TrueCount/100/2**28))

