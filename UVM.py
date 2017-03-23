import Adafruit_BBIO.ADC as ADC
import time, sys
import os.path
import csv

start_time1 = time.time()
####setup ADC and assign input pin
ADC.setup()
#analog input pins are
# "AIN0", "P9_39", F1
# "AIN2", "P9_37", F2
# "AIN6", "P9_35", F3
# "AIN1", "P9_40", P1
# "AIN3", "P9_38", P2
# "AIN5", "P9_36", P3

fsensor_pin0 = 'P9_39'
fsensor_pin2 = 'P9_37'
fsensor_pin6 = 'P9_35'
psensor_pin1 = 'P9_40'
psensor_pin3 = 'P9_38'
psensor_pin5 = 'P9_36'

newfile = time.strftime('%Y-%b-%d,%H:%M:%S', time.localtime())

print newfile

w1 = "/sys/bus/w1/devices/28-000006390e29/w1_slave" #Device 1 file
w2 = "/sys/bus/w1/devices/28-000006dda5d1/w1_slave" #Device 2 file


def readTemp1():
         raw = open(w1, "r").read()
         f = str((float(raw.split("t=")[-1])/1000)*(9.0/5.0) + 32.0)
         c = str(float(raw.split("t=")[-1])/1000)
         identifier1 = 'T1'
         result1 = 'T1 =\t%s\t\t%s' % (c, f)
         return (result1, identifier1, f, c)

result1, identifier1, f, c = readTemp1() #Assign returned tuple

def readTemp2():
         raw = open(w2, "r").read()
         f2 = str((float(raw.split("t=")[-1])/1000)*(9.0/5.0) + 32.0)
         c2 = str(float(raw.split("t=")[-1])/1000)
         identifier2 = 'T2'
         result2 = 'T2 =\t%s\t\t%s' % (c2, f2)
         return (result2, identifier2, f2, c2)

result2, identifier2, f2, c2 = readTemp2() #Assign returned tuple

data = [[newfile, "degrees C", "degrees C",
        "raw signal", "Volts", "gal/min", "L/min","raw signal", "Volts", "gal/min",
        "L/min", "raw signal", "Volts", "gal/min", "L/min",
        "raw signal", "Volts", "psi", "bar", "raw signal", "Volts", "psi",
        "bar", "raw signal", "Volts", "psi", "bar", 'L/m2/hr', "bar", "%", "L/min"],
        ["Time(s)", "T1", "T2", "F1", "F1", "F1", "F1", "F2", "F2", "F2",
        "F2", "F3", "F3", "F3", "F3", "P1", "P1", "P1", "P1", "P2", "P2", "P2",
        "P2", "P3", "P3", "P3", "P3", "Jp", "TMP", "Recovery", "Total Flow Rate"]] #Sets all tuples in list form
i = open('UVM'+newfile+'.csv', 'ab') #Assigns variable to open file with auto-populated name
tempwriter = csv.writer(i)
for row in data:
    tempwriter.writerow(row) #opens file and writes new data to the list
i.close()

while True:

    raw = open(w1, "r").read()
    raw = open(w2, "r").read()

    reading0 = ADC.read(fsensor_pin0)
    time.sleep(0.1)
    reading2 = ADC.read(fsensor_pin2)
    time.sleep(0.1)
    reading6 = ADC.read(fsensor_pin6)
    time.sleep(0.1)
    reading1 = ADC.read(psensor_pin1)
    time.sleep(0.1)
    reading3 = ADC.read(psensor_pin3)
    time.sleep(0.1)
    reading5 = ADC.read(psensor_pin5)
    time.sleep(0.1)

    #scale reading back to voltage
    volts0=reading0*1.800
    volts2=reading2*1.800
    volts6=reading6*1.800
    volts1=reading1*1.800
    volts3=reading3*1.800
    volts5=reading5*1.800


    #scale 1.8V reading to pressure based on 4-20mA signal read
    #from shunt resistor with a 1.8V max at 20 mA corresponding to
    #100 psi and a 4mA min corresponding to 0 psi
    flow0 = volts0 * 2.083 - 0.743 #gpm
    flow2 = volts2 * 2.083 - 0.743 #gpm
    flow6 = volts6 * 13.873 - 4.95 #gpm
    pressure1 = volts1 * 71.961 - 22.467 #psi and calibrated gauges
    pressure3 = volts3 * 70.483 - 24.505 #psi
    pressure5 = volts5 * 71.826 - 20.636 #psi

    SiC_SA = 0.01628916 #m^2
    permeateflux = flow0 * 3.78541 * 60 / SiC_SA #gpm * L/gal * min/hr / m^2
    Flow_Rate_Total = flow0 + flow2 #Concentrate + Permeate flow
    TMP = (pressure1 + pressure5) / 2 - pressure3 #(pressure feed + pressure reject)/2 - pressure permeate
    Recovery = flow0/(flow0 + flow2) * 100 #permeate flow/(reject + permeate flow)*100

    elapsed_time = time.time()
    deltaT = float(elapsed_time) - float(start_time1) #calculates the number of$

    print deltaT
    print '%s\n%s' % ((result1), (result2)) #This prints on the display screen
    print 'F1=\t%s\t%s\t%s\nF2=\t%s\t%s\t%s' % (reading0, volts0, flow0, reading2, volts2, flow2)
    print 'F3=\t%s\t%s\t%s' % (reading6, volts6, flow6)
    print 'P1=\t%s\t%s\t%s' % (reading1, volts1, pressure1)
    print 'P2=\t%s\t%s\t%s\nP3=\t%s\t%s\t%s' % (reading3, volts3, pressure3, reading5, volts5, pressure5)
    print 'Jp=\t%s' % (permeateflux)
    print 'Ft=\t%s' % (Flow_Rate_Total)
    print 'TMP=\t%s' % (TMP)
    print 'R=\t%s' % (Recovery)
    print

           #prints raw reading, output voltage, and flow
    data1 = [[deltaT, c, c2, reading0, volts0, flow0, flow0*3.78541,
            reading2, volts2, flow2, flow2*3.78541, reading6, volts6,
            flow6, flow6*3.78541, reading1, volts1, pressure1,
            pressure1*0.0689476, reading3, volts3, pressure3,
            pressure3*0.0689476, reading5, volts5, pressure5,
            pressure5*0.0689476, permeateflux, TMP, Recovery, Flow_Rate_Total]] #Sets all tuples in list form
    i = open('UVM'+newfile+'.csv', 'ab') #Assigns variable to open file with auto-populated name
    tempwriter = csv.writer(i)
    for row in data1:
        tempwriter.writerow(row) #opens file and writes new data to the list
    i.close()
    time.sleep(5)
