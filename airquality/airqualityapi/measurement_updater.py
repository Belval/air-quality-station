import array
import serial
import struct
import time
from apscheduler.schedulers.background import BackgroundScheduler
from airqualityapi.models import Measurement

def update_air_quality():
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 9600

    ser.open()
    ser.flushInput()

    byte, lastByte = "\x00", "\x00"
    cnt = 0
    while True:
        lastByte = byte
        byte = ser.read(size=1)
        if lastByte == b"\xAA" and byte == b"\xC0":
            sentence = ser.read(size=8)
            readings = struct.unpack('<hhxxcc', sentence)
            pm_25 = readings[0] / 10.0
            pm_10 = readings[1] / 10.0
            Measurement.objects.create(pm25 = pm_25, pm10 = pm_10)
            return

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_air_quality, 'interval', minutes=1)
    scheduler.start()