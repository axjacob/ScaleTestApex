import os, sys
import numpy as np
from multiprocessing import Queue
##Split the large data file up into chunks of 300.
##Get the chunk specific to this machine based in machine launch ID
###Each mnachine has 5 threads. Further divide the chunk by the number of threads
filename = sys.argv[1]
class DataQueue:
    def __init__(self):
        self.q = Queue()
        self.toQueue(sys.argv[1],20,0)

    def parseDataFile(self,l):
        f = open(l,'r')
        f.readline()
        filelines = []
        for line in f.readlines():
            filelines.append(line.split(",")[0])
        return filelines ##File as an array

    def fileSplit(self,l,n):
        
        for i in range(0, len(l), n):  
            yield l[i:i + n]

    def toQueue(self,f, n,i):
        
        fl = self.parseDataFile(sys.argv[1])
        fx = list(self.fileSplit(fl,20))[0] ### This gives Array by the machine ID
        #print(fx)
        fy = list(self.fileSplit(fx,3))
            ### This gives array by thread ID
        fq = fy[i]
        for item in fq:
            self.q.put(item)
    def addToQue(self,item):
        self.q.put(item)
        
    def getItem(self):
        item = self.q.get()
        self.addToQue(item)
        return item

if __name__ == "__main__": 
    #toQueue(filename,20,0)
    d = DataQueue()
    print(d.getItem())
    
    