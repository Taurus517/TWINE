
def Inv_key_Func(inv_key):
    key = []
    key.append(inv_linear[inv_key])

    keySet = []

    for i in range(len(key)):
        if(key[i]==1):
            keySet.append(0)
            keySet.append(1)
        elif(key[i]==4):
            keySet.append(4)
            keySet.append(16)
        else:
            keySet.append(key[i])

    key = sorted(set(keySet))

    return key


def key_Func(key):
    keySet = []

    if(key==1):
        keySet.append(0)
        keySet.append(1)
    elif(key==4):
        keySet.append(4)
        keySet.append(16)
    else:
        keySet.append(key)

    inv_key = []
    for i in keySet:
        inv_key.append(inv_linear.index(i))

    inv_key = sorted(set(inv_key))

    return inv_key


def inv_keyAll_Func(inv_key, R, name):
    for r in range(R):
        KeyALL = []
        for i in inv_key:
            key = Inv_key_Func(i)

            for j in key:
                KeyALL.append(j)

        inv_key = sorted(set(KeyALL))

    print(name-1-r, sorted(set(KeyALL))) 

    return sorted(set(KeyALL))


def keyAll_Func(key, R, name):
    for r in range(R):
        KeyALL = []
        for i in key:
            inv_key = key_Func(i)

            for j in inv_key:
                KeyALL.append(j)

        key = sorted(set(KeyALL))

    print(name+1+r, sorted(set(KeyALL))) 

    return sorted(set(KeyALL))


inv_linear = []
for i in range(4,20):
    inv_linear.append(i)
inv_linear.append(1)
inv_linear.append(2)
inv_linear.append(3)
inv_linear.append(0)


inv_key = [6,13,14,15,16] #
keyAllSet = []
for i in inv_key:
    setkey = []
    setkey.append(i)
    keyAll = inv_keyAll_Func(setkey, 1, 25) # round, roundname
    for j in keyAll:
        keyAllSet.append(j)



key = [13,15] #
keyAllSet = []
for i in key:
    setkey = []
    setkey.append(i)
    keyAll = keyAll_Func(setkey, 1, 24) # round, roundname
    for j in keyAll:
        keyAllSet.append(j)

