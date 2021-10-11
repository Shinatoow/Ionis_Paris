import pyb
import time
import machine

pin_adc_pos = machine.Pin("S23", machine.Pin.IN)
pin_adc_min = machine.Pin("S19", machine.Pin.IN)
adc_pos = machine.ADC(pin_adc_pos)
adc_min = machine.ADC(pin_adc_min)
resistance = 22
while True:
    print(((adc_min.read_u16() - adc_pos.read_u16()) * 0.00488) / resistance)
