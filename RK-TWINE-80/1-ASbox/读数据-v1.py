Data = ((11,1,11),
        (10,2,11),(11,2,10),
        (10,3,10),
        (9,4,10),(10,4,9),
        (9,5,9),
        (8,6,9),(9,6,8),
        (8,7,8),
        (7,8,8),(8,8,7),
        (7,9,7),
        (6,10,7),(7,10,6),
        (6,11,6),
        (5,12,6),(6,12,5),
        (5,13,5),
        (4,14,5),(5,14,4),
        (4,15,4),
        (3,16,4),(4,16,3),
        (3,17,3),
        (2,18,3),(3,18,2),
        (2,19,2),
        (1,20,2),(2,20,1),
        (1,21,1)
        )


f = open("nohup.out")

count = 0
c = 0

for line in f.readlines():
    str_find1 = "E0+Em+E1 = " + str(Data[count][0]) + "+" + str(Data[count][1]) + "+" + str(Data[count][2]) + ", "
    str_find2 = "have trail"
    pos1 = line.find(str_find1)
    pos2 = line.find(str_find2)
    if(pos1 >= 0):
        if(pos2 >= 0):
            if(c == 0):
                print(line)
                c = 1            
    else:
        count += 1
        c = 0
        


f.close()    

    


