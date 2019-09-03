import array
import serial
import struct
import time
from datetime import datetime
from threading import Thread
from Adafruit_CCS811 import Adafruit_CCS811
from airqualityapi.dht22 import DHT22
from pyA20.gpio import gpio
from pyA20.gpio import port

from airqualityapi.models import Measurement


def update_measurement():
    # Setup air quality sensor
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 9600

    ser.open()
    ser.flushInput()

    byte, lastByte = "\x00", "\x00"
    cnt = 0
    
    # Setup Temperature and Humidity sensor
    PIN = port.PA10
    gpio.init()
    
    # Setup eCO2 / TVOC sensor
    ccs = Adafruit_CCS811(busnum=0)
    instance = DHT22(pin=PIN)

    while not ccs.available():
        pass

    time.sleep(5)

    # Main loop, save every minute
    last_save = time.time()
    accumulator = []
    air_quality_read_once = False
    ccs_read_once = False
    temp_hum_read_once = False
    last_pm25_reading = -1
    last_pm10_reading = -1
    last_co2_reading = -1
    last_tvoc_reading = -1
    last_temperature_reading = -1
    last_humidity_reading = -1
    while True:
        try:
            lastByte = byte
            byte = ser.read(size=1)
            if lastByte == b"\xAA" and byte == b"\xC0":
                sentence = ser.read(size=8)
                readings = struct.unpack('<hhxxcc', sentence)
                last_pm25_reading = readings[0] / 10.0
                last_pm10_reading = readings[1] / 10.0
                air_quality_read_once = True
            result = instance.read()
            if result.is_valid():
                last_temperature_reading = result.temperature
                last_humidity_reading = result.humidity
                temp_hum_read_once = True
            if ccs.available():
                if not ccs.readData():
                    last_co2_reading = ccs.geteCO2()
                    last_tvoc_reading = ccs.getTVOC()
                    ccs_read_once = True
            if air_quality_read_once and ccs_read_once and temp_hum_read_once:
                accumulator.append((
                    last_pm25_reading,
                    last_pm10_reading,
                    last_co2_reading,
                    last_tvoc_reading,
                    last_temperature_reading,
                    last_humidity_reading
                ))
            # We save every minute
            if time.time() - last_save >= 30:
                avg_pm25, avg_pm10, avg_co2, avg_tvoc, avg_temp, avg_hum = [
                    sum(ml) / len(ml)
                    for ml in list(zip(*accumulator))
                ]
                Measurement.objects.create(
                    pm25 = avg_pm25,
                    pm10 = avg_pm10,
                    co2 = avg_co2,
                    tvoc = avg_tvoc,
                    temperature = avg_temp,
                    humidity = avg_hum
                )
                data = [sum(ml) / len(ml) for ml in list(zip(*accumulator))]
                print(f"[{datetime.now()}] - PM25: {data[0]:.1f} | PM10: {data[1]:.1f} | CO2: {data[2]:.1f} | TVOC: {data[3]:.1f} | Temp: {data[4]:.1f} | Hum.: {data[5]:.1f}")
                last_save = time.time()
                accumulator = []
        except Exception as ex:
            print(ex)
        time.sleep(1)

def start():
    thread = Thread(target = update_measurement)
    thread.start()

