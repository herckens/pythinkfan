#!/usr/bin/python
import os, time, sys, subprocess
from subprocess import *
import logging
import datetime
 
# Change vars:
LOG_FILENAME = "/tmp/tpfan_log.txt"
timestep=1.0 # in [s] sleep time between samples
temp_desired = 60
temp_critical = 90
### PID parameters: ###
p = 0.28
#####################
 
# Do not change
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
 

def get_maxtemp():
  """
  Get readings from all temperature sensors.
  return:
    maxtemp (the highest of all temperature)
    temps (vector of all temperature)
  """
  temps = []
  # check sensors in laptop # not systen specific! great
  st1="cat /proc/acpi/ibm/thermal | awk '{ for (i=2; i<=NF; i++) printf("
  st1=st1+('"%s\\n" , $i)}')+("'")
  f=os.popen(st1)
  for i in f.readlines():
    temp = float(i)
    temps.append(temp)

  # for some reason /proc/acpi/ibm/thermal misses the temperature in /proc/acpi/thermal_zone/...
  f=os.popen("cat /proc/acpi/thermal_zone/THM0/temperature")
  line = f.read()
  temp = float(line[line.index(' ')+1:line.rindex(' ')]) # extract the number
  temps.append(temp)
  f=os.popen("cat /proc/acpi/thermal_zone/THM1/temperature")
  line = f.read()
  temp = float(line[line.index(' ')+1:line.rindex(' ')]) # extract the number
  temps.append(temp)

  # Extract the maximum temperature. We will control this one
  maxtemp=max(temps)

  return maxtemp, temps

def set_fanlevel(level):
  """ Set the fan to the desired level """
  ret = os.popen("echo level " + str(level) + " > /proc/acpi/ibm/fan")


while 1:
  try :
    time.sleep(timestep)
    maxtemp, temps = get_maxtemp() # Read current temperatures
    print(temps)
    print("maxtemp = " + str(maxtemp))
    
    error = maxtemp - temp_desired
    print("error = " + str(error))

    level = p * error
    print("level = " + str(level))
    level = int(level)
    if level > 7:
      level = 7
    if level < 0:
      level = 0
    set_fanlevel(level)
    print("int(level) = " + str(level))

  except KeyboardInterrupt:                                                                                                                                                                                                           
    print 'Caught Ctrl-c. Preparing for shutdown...'
    set_fanlevel("auto") # TODO Maybe better set to 7 instead of "auto"?!
    break
