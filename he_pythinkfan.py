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
  st1="cat /proc/acpi/ibm/thermal | awk '{ for (i=2; i<=NF; i++) printf("
  st1=st1+('"%s\\n" , $i)}')+("'")
  f=os.popen(st1)
  for i in f.readlines():
    intw = float(i)
    temp.append(intw)
  maxtemp=max(temp)
  print temp
  print maxtemp



  time.sleep(deamonTIME)
