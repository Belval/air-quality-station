from django.apps import AppConfig


class AirqualityapiConfig(AppConfig):
    name = 'airqualityapi'

    def ready(self):
        from airqualityapi import measurement_updater
        measurement_updater.start()
