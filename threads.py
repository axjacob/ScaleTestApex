#runs threads
import sys, importlib, configparser
config = configparser.RawConfigParser()
config.read('testrunner.properties')
scriptname = config['default']['main.script']
mod = importlib.import_module(scriptname, package=None)
TestRunner = getattr(mod,'TestRunner')
#from multiprocessing import Pool, Queue, Process
import multiprocessing
from dataqueue import DataQueue

def testtask(q):
    t=TestRunner(q)
    t()

if __name__ == '__main__':
    q = DataQueue()
    jobs = []
    for i in range(2):
        p = multiprocessing.Process(target=testtask,args=(q,))
        jobs.append(p)
        p.start()
    
#if __name__ == '__main__':
#    workers = config.getint('default','workers')
#    print(workers)
#    chunksize = config.getint('default','chunk')
    #for 
#    with Pool(processes=workers) as pool:
#        result = pool.map(testtask,range(chunksize))
