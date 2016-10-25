import time

w1="/sys/bus/w1/devices/28-000002e34b73/w1_slave"
w2 = "/sys/bus/w1/devices/28-000002e34b73/w1_slave"

while True:
    raw = open(w1, "r").read()
    print "Temperature 1 is "+str(float(raw.split("t=")[-1])/1000)+" degrees Celcius"
    time.sleep(1)

while True:
    raw = open(w2, "r").read()
    print "Temperature 2 is "+str(float(raw.split("t=")[-1])/1000)+" degrees Celcius"
    time.sleep(1)
