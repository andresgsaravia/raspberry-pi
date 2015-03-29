#!/usr/bin/python
#import os
import glob
import time
import httplib, urllib
import time
from time import localtime, strftime
 
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

def doit():
    temp_c = read_temp()
    params = urllib.urlencode({'field1': temp_c,'key':'0RI7KXKAPBE9V3YL'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print strftime("%d %b %Y %H:%M:%S", localtime()), response.status, response.reason, temp_c
        data = response.read()
        conn.close()
    except:
        print "connection failed"

if __name__ == "__main__":
    doit()

