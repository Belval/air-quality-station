# air-quality-station
Combining the SNS011 sensor with an OrangePI to displays:

- PM2.5 and PM10 air quality measurements
- Temperature and Humidity measurements

## UI

The basic chart UI allows for easy reading of the air quality data for a given interval.

![ui](images/ui.png)

## Hardware

- [SNS011 air quality sensor](https://www.aliexpress.com/item/Laser-PM2-5-sensor-SDS011-particle-sensor-dust-sensor/32724933436.html)
- [DHT22 temperature and humidity sensor](https://www.amazon.ca/gp/product/B06Y63YMSS/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1) (Bought from Amazon for the fast shipping, is much cheaper on AliExpress)
- [MH-Z19 CO2 sensor](https://www.aliexpress.com/item/32708354059.html)
- [Orange Pi Zero H2](https://www.aliexpress.com/item/New-Orange-Pi-Zero-H2-Quad-Core-Open-source-512MB-development-board-beyond-Raspberry-Pi/32761500374.html)
    - Any RasPi-like system would do
- Power adapter
- 4GB+ microSD card

## Case

There is a 3D printable case model for the SNS011 available in the `case/` directory.

![case](images/case.png)

## Future enhancement

- Better CO2 monitoring, while the CCS811 seems to be working, using a MOx sensor as a way to estimate CO2 concentration is highly controversial.
- Better dashboard
