

f = open("命令.txt", "w")
Upper = (0,  
          
        11, 
        9, 
        14, 
        5, 
        12, 
        7, 
        13, 
        4, 
        8, 
        2, 
        3, 
        6
        )
Lower = ((0,0,0,0),
         
        (4,13,1, 11), 
        (13,13,1, 11), 
        (14,11,13, 4), 
        (6,2,10, 5), 
        (12,4,11, 14), 
        (3,3,15, 8), 
        (5,5,2, 6), 
        (7,8,3, 9), 
        (11,11,13, 4), 
        (14,14,4, 12), 
        (5,10,7, 2), 
        (4,4,11, 14), 
        (2,2,10, 5), 
        (9,9,8, 7), 
        (11,1,12, 13), 
        (8,15,6, 3)
        )

for i in range(1,len(Upper)):
    ua1 = Upper[i-1]

    ua = Upper[i]

    f.write("sed -i 's/delta_upper = {0,0,0,0,"+str(ua1)+",0,0,0,0,0,0,0,0,0,0,0}/delta_upper = {0,0,0,0,"+str(ua)+",0,0,0,0,0,0,0,0,0,0,0}/g' Em.cpp\n")
    f.write("sed -i 's/key_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"+str(ua1)+",0,0}/key_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"+str(ua)+",0,0}/g' Em.cpp\n\n")

    for j in range(1,len(Lower)+1):
        if(j==len(Lower)):
            f.write("sed -i 's/delta_lower = {0,0,0,0,0,0,"+str(la)+",0,0,0,"+str(lb)+","+str(lc)+",0,0,0,0}/delta_lower = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}/g' Em.cpp\n")
            f.write("sed -i 's/key_lower = {0,0,0,0,0,0,0,"+str(ld)+",0,0,0,0,0,0,0,0,0,0,0,0}/key_lower = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}/g' Em.cpp\n\n")

        else:
            la1 = Lower[j-1][0]
            lb1 = Lower[j-1][1]
            lc1 = Lower[j-1][2]
            ld1 = Lower[j-1][3]

            la = Lower[j][0]
            lb = Lower[j][1]
            lc = Lower[j][2]
            ld = Lower[j][3]
            

            f.write("sed -i 's/delta_lower = {0,0,0,0,0,0,"+str(la1)+",0,0,0,"+str(lb1)+","+str(lc1)+",0,0,0,0}/delta_lower = {0,0,0,0,0,0,"+str(la)+",0,0,0,"+str(lb)+","+str(lc)+",0,0,0,0}/g' Em.cpp\n")
            f.write("sed -i 's/key_lower = {0,0,0,0,0,0,0,"+str(ld1)+",0,0,0,0,0,0,0,0,0,0,0,0}/key_lower = {0,0,0,0,0,0,0,"+str(ld)+",0,0,0,0,0,0,0,0,0,0,0,0}/g' Em.cpp\n\n")
            
        f.write("g++ -std=c++11 Em.cpp -o Em_21R_O2_8-5-8 -lpthread\n")
        f.write("nohup ./Em_21R_O2_8-5-8 & \n\n")



k = len(Upper)
ua1 = Upper[k-1]
ub1 = Upper[k-1]
f.write("\n\nsed -i 's/delta_upper = {0,0,0,0,"+str(ua1)+",0,0,0,0,0,0,0,0,0,0,0}/delta_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}/g' Em.cpp\n")
f.write("sed -i 's/key_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"+str(ua1)+",0,0}/key_upper = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}/g' Em.cpp\n\n")

f.close()

