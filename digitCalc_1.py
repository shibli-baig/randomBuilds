def mult(a):
    if a < 10:
        return 0
    else:
        mpl = 1
        while a % 10 > 0:
            k = a % 10
            a = int(a / 10)
            mpl = mpl * k
        # print(mpl)
        return mult(mpl) + 1



