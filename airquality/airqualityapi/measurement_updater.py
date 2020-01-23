import array
import serial
import struct
import time
import os
from datetime import datetime
from threading import Thread
from airqualityapi.dht22 import DHT22
from pyA20.gpio import gpio
from pyA20.gpio import port

from airqualityapi.models import Measurement


def update_measurement():
    # Setup air quality sensor
    aiq_ser = serial.Serial()
    aiq_ser.port = "/dev/ttyUSB0"
    aiq_ser.baudrate = 9600

    aiq_ser.open()
    aiq_ser.flushInput()

    byte, lastByte = "\x00", "\x00"
    cnt = 0

    # Setup CO2 concentration sensor
    co2_ser = serial.Serial(timeout=5)
    co2_ser.port = "/dev/ttyS1"
    co2_ser.baudrate = 9600

    co2_ser.open()

    # Setup Temperature and Humidity sensor
    PIN = port.PA10
    gpio.init()

    instance = DHT22(pin=PIN)

    time.sleep(5)

    # Main loop, save every minute
    last_save = time.time()
    accumulator = []
    aiq_quality_read_once = False
    co2_concentration_read_once = False
    temp_hum_read_once = False
    last_pm25_reading = -1
    last_pm10_reading = -1
    last_co2_reading = -1
    last_temperature_reading = -1
    last_humidity_reading = -1
    while True:
        try:
            lastByte = byte
            byte = aiq_ser.read(size=1)
            if lastByte == b"\xAA" and byte == b"\xC0":
                sentence = aiq_ser.read(size=8)
                readings = struct.unpack("<hhxxcc", sentence)
                last_pm25_reading = readings[0] / 10.0
                last_pm10_reading = readings[1] / 10.0
                air_quality_read_once = True
            co2_ser.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            co2_res = co2_ser.read(9)
            if co2_res != None:
                last_co2_reading = co2_res[2] * 256 + co2_res[3]
                co2_concentration_read_once = True
            result = instance.read()
            if result.is_valid():
                last_temperature_reading = result.temperature
                last_humidity_reading = result.humidity
                temp_hum_read_once = True
            if air_quality_read_once and temp_hum_read_once and last_pm10_reading >= 0:
                accumulator.append(
                    (
                        last_pm25_reading,
                        last_pm10_reading,
                        last_co2_reading,
                        last_temperature_reading,
                        last_humidity_reading,
                    )
                )
            # We save every minute
            if time.time() - last_save >= 30:
                avg_pm25, avg_pm10, avg_co2, avg_temp, avg_hum = [
                    sum(ml) / len(ml) for ml in list(zip(*accumulator))
                ]
                Measurement.objects.create(
                    pm25=avg_pm25,
                    pm10=avg_pm10,
                    co2=avg_co2,
                    temperature=avg_temp,
                    humidity=avg_hum,
                )
                data = [sum(ml) / len(ml) for ml in list(zip(*accumulator))]
                print(
                    f"[{datetime.now()}] - PM25: {data[0]:.1f} | PM10: {data[1]:.1f} | CO2: {data[2]:.1f} | Temp: {data[3]:.1f} | Hum.: {data[4]:.1f}"
                )
                last_save = time.time()
                accumulator = []
        except Exception as ex:
            pass
        time.sleep(1)


def start():
    thread = Thread(target=update_measurement)
    thread.start()

