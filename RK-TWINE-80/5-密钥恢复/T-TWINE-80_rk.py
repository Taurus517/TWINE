import math

def TimeComplexity(GuessKey_Filter, TimeAll, Np, Nk):

    for pos in range(len(GuessKey_Filter)):

        SboxNumber = math.ceil(GuessKey_Filter[pos][0] / 4)

        KeyGuess = 2**GuessKey_Filter[pos][0]
        filter = GuessKey_Filter[pos][1]

        Time = SboxNumber * 4 * KeyGuess * Np
        TimeAll = TimeAll + Time
        
        if(Nk * KeyGuess * filter >= 1):
            Np = Np
            Nk = Nk * KeyGuess * filter
        else:
            Np = Np * KeyGuess * filter
            Nk = Nk
        
        M3 = Np * Nk / 128

        #print("Time: ", math.log2(Time))
        #print("Np: ", math.log2(Np))
        #print("Nk: ", math.log2(Nk))

    return TimeAll, M3, math.log2(Nk)


def RelatedFunc(n,k,rb,rf,mb,mf,s,Pr,UpperAS,LowerAS,GuessKey_Filter):
    ## related-key

    P = math.sqrt( 2**(-Pr) )

    ## structure
    quartet = s * P**(-2) * 2**n #满足区分器的正确四元组

    y = math.sqrt(s) * 2**(n/2-rb) / P
    print("y = 2^", math.log2(y))

    quartet = (y * 2**rb)**2 # 满足区分器头部差分的正确四元组
    #print("quartet2: 2^", math.log2(quartet))


    ## Data
    D = y * 2**rb # P1
    DR = 4 * D # P1,P2,P3,P4
    print("DR = 2^", math.log2(DR))


    ## Memory ## Time
    T1 = DR
    print("T1 = 2^", math.log2(T1)) #加密数据 P1,P2,P3,P4 -> C1,C2,C3,C4
    
    M1 = DR
    print("M1 = 2^", math.log2(M1)) #存数据(P1,C1),(P2,C2),(P3,C3),(P4,C4)


    Set1 = y * 2**(2*rb) #明文处构造
    Set2 = ( y * 2**rb * 2**(-(n-rf)) )**2 * 2**(n-rf) #密文处构造
    M2 = 2 * min(Set1, Set2)
    print("M2 = 2^", math.log2(M2), ", ", math.log2(2 * Set1), ", ", math.log2(2 * Set2)) #存pairs S1,S2

    T2 = 2 * min(Set1, Set2) #构造pairs S1,S2
    print("T2 = 2^", math.log2(T2), ", ", math.log2(2 * Set1), ", ", math.log2(2 * Set2)) 


    u = -(math.log2( y * 2**rb * 2**(-n) )) 
    filter1 = (7/16)**UpperAS
    filter2 = (7/16)**LowerAS
    filtertotal = filter1**2 * filter2**2 
    T3 = min(Set1**2 * 2**(-2*(n-rf)) * filtertotal, Set2**2 * 2**(-2*(n-rb-u)) * filtertotal)
    print("quartet = 2^", math.log2(T3), ", ", math.log2(Set1**2 * 2**(-2*(n-rf)) * filtertotal), ", ", math.log2(Set2**2 * 2**(-2*(n-rb-u)) * filtertotal)) 


    
    (T3, M3, Nk) = TimeComplexity(GuessKey_Filter, 0, T3, 1)
    T3 = T3 / 25 / 8 #
    print("T3 = 2^", math.log2(T3))
    print("M3 = 2^", math.log2(M3)) #计数器

    #T4 = 2**(k-max(mb,mf) + mb+mf-h)
    T4 = 2**(k-max(mb,mf) + Nk)
    h = mb+mf-Nk
    print("h: ", h)
    print("T4 = 2^", math.log2(T4))

    M = M1+M2+M3
    print("M = 2^", math.log2(M*128/8))

    T = T1+T2+T3+T4
    print("T = 2^", math.log2(T))


    #成功率
    SN = ( 2**(-n) * P**2 ) / 2**(-2*n)
    print("SN: 2^", math.log2(SN))
    
    y1 = 1 - 2**(-h)
    print("y1: ", y1)
    x1 = 9 ##
    y1 = 1 - 0.5 * math.erfc( x1 / math.sqrt(2) )
    print("y1: ", y1)


    z1 = math.sqrt(s * SN) - x1
    z2 = math.sqrt(SN + 1)
    z = z1 / z2

    Ps = 1 - 0.5 * math.erfc( z / math.sqrt(2) )

    print("Ps: ", Ps)


GuessKey_Filter_2_21_2 = [(4, (1/7)**2),
                            (4, (1/7)**2),
                            (4, (1/7)**2),

                            (4, (1/7)**2),
                            (4, (1/7)**2),
                            (4, (1/7)**2),
                            (4, (1/7)**2),

                            (8, (1/7)**2),
                            (8, (1/7)**2),

                            (8, (1/7)**2),
                            (8, (1/7)**2),
                            (8, (1/7)**2)
                            ]

n = 64
k = 80
Pr = 54.18 # 区分器概率
s = 1 # 期望的正确对个数


#'''2+21+2

rb = 4*7 # 明文处活跃
rf = 4*5 # 密文处活跃
mb = 4*9 # kb
mf = 4*7 ## kf

UpperAS = 7
LowerAS = 5

RelatedFunc(n,k,rb,rf,mb,mf,s,Pr,UpperAS,LowerAS,GuessKey_Filter_2_21_2)

# DR = 2^61.09
# M = 2^79.18 Bytes (NP*Nk/128)
# T = 2^75.18 (T3/Round/8)
# PS = 75.81%
#'''

