from time import sleep, ticks_ms, ticks_diff, sleep_ms
from line_sensor import LineSensor
import lms_esp32
from machine import Pin, UART
uart=UART(1,rx=lms_esp32.RX_PIN,tx=lms_esp32.TX_PIN,baudrate=115200)
DUT = LineSensor(fresh_ms=10, device_addr=0x33)
TU = LineSensor(device_addr=0x34)




def vector_add(a, b):
    l=len(a)
    s=[0]*l
    for i in range(l):
        s[i] = a[i] + b[i]
    return s

def vector_div(a, d):
    l=len(a)
    s=[0]*l
    for i in range(l):
        s[i] = a[i]/d
    return s
    

def measure_avg(dev, nr):
    avg = [0]*8
    cnt = 0
    for i in range(nr):
        try:
            val = dev.values()
            #print(val)
        except e:
            continue
        cnt += 1
        avg = vector_add(avg, val)
        sleep_ms(10)
    return vector_div(avg, cnt)
    
    
# Check IR sensors
# TU IR off

DUT.ir_power(False)
TU.ir_power(False)
sleep_ms(100)
DUT.led_mode(DUT.LEDS_VALUES)
TU.led_mode(DUT.LEDS_VALUES)
print("meas DUT, TU IR off")
print(measure_avg(DUT, 40))
TU.ir_power(True)
sleep_ms(100)
print("meas DUT, TU IR on")
print(measure_avg(DUT, 40))

DUT.ir_power(False)
TU.ir_power(False)
sleep_ms(100)
print("meas TU, DUT IR off")
print(measure_avg(TU, 40))
DUT.ir_power(True)
sleep_ms(100)
print("meas TU, DUT IR on")
print(measure_avg(TU, 40))




