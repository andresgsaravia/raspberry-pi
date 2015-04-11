#!/usr/bin/python
import httplib, urllib
from time import localtime, strftime
from RCtime.RCtime import RCtime
from thermometer_DS18B20.temp import read_temp

def doit():
    temp_c = read_temp()
    rct = RCtime(18) # GPIO pin 18
    params = urllib.urlencode({'field1': temp_c,'field2': rct,'key':'4WHLY4CAMQKETKPM'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print strftime("%d %b %Y %H:%M:%S", localtime()), response.status, response.reason, temp_c, rct
        data = response.read()
        conn.close()
    except:
        print "connection failed"

if __name__ == "__main__":
    doit()


