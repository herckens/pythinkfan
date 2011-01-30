#!/usr/bin/python
import os, time, sys, subprocess
from subprocess import *
import logging
import datetime
 
# Change vars:
LOG_FILENAME = "/tmp/tpfan_log.txt"
deamonTIME=5.0 # in [s] sleep time between samples
#####################
 
# Do not change
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
 
while 1:
        temp = []
        # check sensors in laptop # not systen specific! great
####   cat /proc/acpi/ibm/thermal | awk '{ for (i=2; i<=NF; i++) printf("%s\n" , $i)}'
        st1="cat /proc/acpi/ibm/thermal | awk '{ for (i=2; i<=NF; i++) printf("
        st1=st1+('"%s\\n" , $i)}')+("'")
        f=os.popen(st1)
        for i in f.readlines():
                intw = float(i)
                temp.append(intw)
        #print temp
        #  check cpu sensors # not systen specific! great
        f=os.popen("sensors 2>/dev/null | grep Core | awk '{print $3}' | sed s/+// | sed 's/..$//'")
        for i in f.readlines():
                intw = float(i)
                temp.append(intw)
        print temp
        logging.info(" ---------------------------------------------------------------------")
        tmp=max(temp)



        time.sleep(deamonTIME)
