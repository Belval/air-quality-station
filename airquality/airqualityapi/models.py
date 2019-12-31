from django.db import models


class Measurement(models.Model):
    # Timestamp, when the measurement was taken
    timestamp = models.DateTimeField(auto_now=True)
    # PM25 concentration in micro grams per cubic meter
    pm25 = models.DecimalField(decimal_places=4, max_digits=16)
    # PM10 concentration in micro grams per cubic meter
    pm10 = models.DecimalField(decimal_places=4, max_digits=16)
    # Temperature in celsius
    temperature = models.DecimalField(decimal_places=2, max_digits=8)
    # Relative humidity in %
    humidity = models.DecimalField(decimal_places=2, max_digits=8)
