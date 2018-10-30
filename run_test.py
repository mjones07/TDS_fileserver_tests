#!/usr/bin/env python2.7

import sys
import os
import datetime
import subprocess
import time, os, json, requests
from mpi4py import MPI
from glob import glob
from random import shuffle
from time import time



comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# clear the node cache
for i in range(0,256):
    with open('/group_workspaces/jasmin4/hiresgw/mj07/cacheclear%s'%i,'r') as f:
        cachedata = f.read()

comm.barrier()

conc_num = 1

testfilesloc = 2

if testfilesloc == 1: #od4gws test data
    files = glob('/group_workspaces/jasmin2/atsrrepro/mjones07/test*.nc')
    ser_add = 'http://opendap4gws.jasmin.ac.uk/thredds/atsrrepro/fileServer/testAll/'
    file_list = [ser_add+x.split('/')[-1] for x in files]
    shuffle(file_list)
elif testfilesloc == 2: # same files on 
    files = glob('/group_workspaces/jasmin4/hiresgw/mj07/test*.nc')
    ser_add = 'http://host298.jc.rl.ac.uk/thredds/fileServer/data/hiresgw/'
    file_list = [ser_add+x.split('/')[-1] for x in files]
    shuffle(file_list)


#elif testfilesloc == 2: # same files on 
#    files = glob('/group_workspaces/jasmin2/atsrrepro/mjones07/test*.nc')
#    ser_add = 'http://host298.jc.rl.ac.uk/thredds/fileServer/data/mjones07/'
#    file_list = [ser_add+x.split('/')[-1] for x in files]
#    shuffle(file_list)

if rank<64:
    floc=file_list[rank]
elif rank<128:
    floc=file_list[rank-64]
elif rank<192:
    floc=filelist[rank-128]
elif rank<256:
    floc=filelist[rank-192]

run_path = '/home/users/mjones07/tds_testing/comparing_fileServer/'


file_size = 34359750521 
start = time()
os.system('curl %s > /dev/null' % (floc))
end = time()-start
rate = file_size/end/10**6

with open('%sresults.csv'%run_path,'a') as f:
    f.write('%s,%s,%s,%s,%s\n' % (size,floc,file_size,end,rate))
