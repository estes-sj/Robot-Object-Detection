import multiprocessing

NX = 10
NY = 2


def mde(dad, mutex):
    for i in range(NX):
        for j in range(NY):
            mutex.acquire()
            dad[0] = i
            dad[1] = j
            mutex.release()

#idk maybe use this shit
def mda(dad, mutex):
    c = 0
    while c <= NX*NY:
        mutex.acquire()
        print(dad)
        c += 1
        mutex.release()

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    mutex = manager.Lock()
    dado = manager.list([0, 0])
    p1 = multiprocessing.Process(target=mde, args=(dado, mutex,))
    p2 = multiprocessing.Process(target=mda, args=(dado, mutex,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()