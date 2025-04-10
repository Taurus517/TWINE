# 《Related-Key Rectangle Attacks on Reduced-Round TWINE》
take TWINE-80 as an example, we use "*" to represent the constants to be modified

    1-ASbox: search for the minimum number of active S-boxes (Table 4 and Table 5)
        take TWINE-80_Boomerang_ASbox_RK.py as an example
        
            modify the constants in TWINE-80_Boomerang_ASbox_RK.py: 
                'for (r0,rm,r1) in ((*,*,*),...,(*,*,*))', 
                'for totalASAK in range(*,*)'.
            run 'python3 TWINE-80_Boomerang_ASbox_RK.py'.
            
            modify the constants in run-v1.cpp: 
                'Data[*][3] = {{*,*,*},...,{*,*,*}};', 
                'for(int count = 0; count < *; count++)', 
                'for(int totalASAK = *; totalASAK < *; totalASAK++)'.
            run 'g++ run-v1.cpp    nohup ./a.out &'.
            
    2-APattern: search for the active patterns
    
        take TWINE-80_Boomerang_AP_RK-friendly.py as an example
        
            modify the constants in TWINE-80_Boomerang_AP_RK-friendly.py: 
                'total_RK = *', '(r0,rm,r1) = (*,*,*)', 'totalASAK = *'.
            run 'TWINE-80_Boomerang_AP_RK-friendly.py'.
            
            modify the constants in run-v2.cpp: 
                'r0 = *', 'rm = *', 'r1 = *', 'totalASAK = *'.
            run 'g++ run-v2.cpp    nohup ./a.out &'.
            
            from TWINE-80_Boomerang_AP_RK_8+4+9R.cvc, we will get the active patterns for the (*+*+*)-round boomerang distinguisher
        
    3-Pr: evaluate the differential characteristic probabilities of E0 and E1 (Table 6)
          take evaluate the differential characteristic probabilities of E0 as an example
          
            modify the constants in TWINE-80_Boomerang_Pr_RK.py: 
                '(r0,r1) = (*,*)', '(total_Pr_E0, total_Pr_E1) = (*,*)', 
                the active pattern in 'Data = [*...*]'. 
            run "python3 TWINE-80_Boomerang_Pr_RK.py".

            modify the constants in run-v3-Upper.cpp: 
                'r0 = *', 'total_Pr_E0 = *'
            run "g++ run-v3-Upper.cpp   nohup ./a.out &"
    
    4-ClusterPr: evaluate the probability of Em (Table 6)

            modify the constants in TWINE-80_Boomerang_Em_RK.cpp: 
                'r0 = *', 'rm = *', 'r1 = *',
                the difference of \beta: 'delta_upper = {*,...,*}',
                the difference of \bigtriangleup_K': 'key_upper = {*,...,*}',
                the difference of \gamma: 'delta_lower = {*,...,*}',
                the difference of \bigtriangledown_K': 'key_lower = {*,...,*}',
            
            modify the constants in run-v4-Em.cpp: 
                'g++ -std=c++11 TWINE-80_Boomerang_Em_RK.cpp -lpthread',
                'TotalData = 2^*'.
            run 'g++ run-v4-Em.cpp'
    
    5-KeyRecovery: 

          modify the constants in TWINE-80_masterkey.py and run (Table 10)
          
          compute the data, time (Table 11), and memory complexities: modify the constants in TWINE-80_rk.py and run
