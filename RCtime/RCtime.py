#!/usr/bin/python
 
# Example for RC timing reading for Raspberry Pi
# Must be used with GPIO 0.3.1a or later - earlier verions
# are not fast enough!
 
import RPi.GPIO as GPIO
import time, os
import httplib, urllib
 
DEBUG = 1
GPIO.setmode(GPIO.BCM)
 
def RCtime (RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)
 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading
 
def readAndUpload():
    rct = RCtime(18) # Read RC timing using pin #18
    params = urllib.urlencode({'field2': rct,'key':'0RI7KXKAPBE9V3YL'})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print time.strftime("%d %b %Y %H:%M:%S", time.localtime()), response.status, response.reason, rct
        data = response.read()
        conn.close()
    except:
        print "connection failed"

if __name__ == "__main__":
    readAndUpload()
