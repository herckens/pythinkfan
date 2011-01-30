#!/usr/bin/python
import os, time, sys, subprocess
from subprocess import *
import logging
import datetime
 
# Change vars:
LOG_FILENAME = "/tmp/tpfan_log.txt"
timestep=1.0 # in [s] sleep time between samples
temp_desired = 60
temp_desired_forIntegral = 75
hysteresis = 0.6
### PID parameters: ###
pid_P = 0.28
pid_I = 0.01
pid_integral_max = 7
pid_integral_min = 0
#####################
 
# Do not change
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
level_old = 0.0
integral = 0.0
 

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
    error_forIntegral = maxtemp - temp_desired_forIntegral
    print("error_forIntegral = " + str(error_forIntegral))
    integral += pid_I * error_forIntegral
    if integral > pid_integral_max:
      integral = pid_integral_max
    if integral < pid_integral_min:
      integral = pid_integral_min
    print("integral = " + str(integral))

    level = pid_P * error + integral
    print("level = " + str(level))
    if level > 7.0:
      level = 7
    if level < 0:
      level = 0
    if abs(level_old - level) > hysteresis or level == 7 or level == 0:
      level_old = level
      level = int(level)
      set_fanlevel(level)
      print("new level = " + str(level))

  except KeyboardInterrupt:                                                                                                                                                                                                           
    print 'Caught Ctrl-c. Preparing for shutdown...'
    set_fanlevel("auto") # TODO Maybe better set to 7 instead of "auto"?!
    break
