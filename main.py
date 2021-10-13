import pyb
import time

import machine

###
sw = pyb.Switch()
ite = 0
### get led ready
pyb_leds = [pyb.LED(1), pyb.LED(2), pyb.LED(3), pyb.LED(4)]
### reset call back in case of button press
sw.callback(None)
### Waiting for the button to start the measure
while not sw():
    pyb_leds[0].on()
    pyb_leds[1].on()

## switch off led and wait two seconds before starting to avoid the button to be reconnized as a stop signal
pyb_leds[0].off()
pyb_leds[1].off()
time.sleep(2)

### Generate the csv file without ereasing other measurement
a = 0
file = None
while file is None:
    try:
        file = open("/sd/data/mesure" + str(a) + ".csv", "x")
    except Exception as e:
        a = a + 1

### write the  header
file.write("pin1; pin2;difference de tension; time;")
file.flush()

pin_adc_pos = machine.Pin("S23", machine.Pin.IN)
pin_adc_min = machine.Pin("S19", machine.Pin.IN)
adc_min = machine.ADC(pin_adc_min)
adc_max = machine.ADC(pin_adc_pos)


### def a func to be clal on button press to close file and warn people
### that the usb can be removed without losing data

for led in pyb_leds:
    led.on()

t = time.time()
t2 = time.time()
while not sw():
    pyb_leds[0].on()
    pyb_leds[1].on()
    ### read value on two different pin
    value_min = adc_min.read_u16() * 3.3 / 65536
    value_max = adc_max.read_u16() * 3.3 / 65536

    ### maj of csv


    second_pasted = time.time() - t
    hours = second_pasted / 3600
    minutes = (second_pasted - (hours * 3600)) / 60
    secondes = second_pasted - (second_pasted / 60)

    if (time.time() - t2 > 300):
        file.write("\n")
        file.write(str(value_max) + ';' + str(value_min) + ';' + str(value_max - value_min)+";" + str(time.time() - t))
        t2 = time.time()

    ### écrit en secondes

    ### écrit en xxhxxmxxhsecondes
    #file.write(str(value_max) + ';' + str(value_min) + ';' + str(value_max - value_min) + ";" + str(hours) + "H " + str(
    #    minutes) + "min " + str(secondes) + "sec")


    ###Stop ! wait a minute

    time.sleep(4)
    pyb_leds[0].off()
    pyb_leds[1].off()
    time.sleep(1)


file.close()
for led in pyb_leds:
    led.off()

