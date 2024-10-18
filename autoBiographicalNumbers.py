for i in range(10000000):
    numLen = len(str(i))
    sum = 0
    k = i
    posAr = [0 for i in range(numLen)]
    while k > 0:
        try:
            numLast = k%10
            posAr[numLast] += 1
            sum += numLast
            k = int(k / 10)
        except:
            k = int(k / 10)
            pass

    numUsingPos = ''
    for numTimes in posAr:
        numUsingPos+=str(numTimes)

    finNum = int(numUsingPos)

    if sum == numLen:
        if finNum == i:
            print(f'Num is {i}')
