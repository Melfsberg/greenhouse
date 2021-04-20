from machine import Pin
import utime
import select
import sys

re1 = Pin(2, Pin.OUT)
re2 = Pin(3, Pin.OUT)
re3 = Pin(4, Pin.OUT)
re4 = Pin(5, Pin.OUT)
pump = Pin(6, Pin.OUT)
flow = Pin(7, Pin.IN, Pin.PULL_UP)
LEDbuiltin=Pin(25,Pin.OUT)

re1.value(False)
re2.value(False)
re3.value(False)
re4.value(False)
pump.value(False)
LEDbuiltin.value(True)

def pulse_irq(pin):
    global pulses 
    pulses+=1 #1/50 ML PER PULS?

paus=200
pulses=0
new_pulses=False

def Vattna(channel,volume,maxtime):
    global pulses
    
    pulses=0
    start=utime.ticks_ms()
    
    flow.irq(trigger=machine.Pin.IRQ_RISING, handler=pulse_irq)
    pump.value(True)
    
    if channel==1:
        re1.value(True)
    elif channel==2:
        re2.value(True)
    elif channel==3:
        re3.value(True)
    elif channel==4:
        re4.value(True)
    
    while (pulses<volume):
        if (utime.ticks_ms()-start)/1000>maxtime:
            break
        utime.sleep_ms(500)
        print(channel, ',' , pulses, ',' , round((utime.ticks_ms()-start)/1000))
        
            
    
    pump.value(False)
    
    if channel==1:
        re1.value(False)
    elif channel==2:
        re2.value(False)
    elif channel==3:
        re3.value(False)
    elif channel==4:
        re4.value(False)
    
    
    flow.irq(handler=None)
    

while (True): 
    if select.select([sys.stdin],[],[],0)[0]:
        data = sys.stdin.readline()

        data=data.split(',')

        Vattna(int(data[0]),int(data[1]),int(data[2]))
        
        utime.sleep(1)     
  
