def forker(inqueue,out1,out2,killProc):
    while not killProc == 1:
        try:
            item = inqueue.get(True)
        except IOError:
            return
        out1.put(item)
        out2.put(item)
