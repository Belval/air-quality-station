import datetime
import json

from dateutil import parser
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, F, Q
from django.db.models.functions import TruncDay, TruncHour
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader

from airqualityapi.models import Measurement

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def measurements(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    interval = request.GET.get('interval', 'minute')

    if start is not None:
        start = parser.parse(start)
    if end is not None:
        end = parser.parse(end)

    if start is None:
        start = datetime.datetime(1970, 1, 1)
    if end is None:
        end = datetime.datetime.now()

    measurements = Measurement.objects.filter(Q(timestamp__gte=start, timestamp__lte=end))
    if interval == 'hour':
        measurements = measurements.annotate(datetime=TruncHour('timestamp')
                                   ).values('datetime'
                                   ).annotate(pm25=Avg('pm25')
                                   ).annotate(pm10=Avg('pm10')
                                   ).annotate(co2=Avg('co2')
                                   ).annotate(tvoc=Avg('tvoc')
                                   ).annotate(temperature=Avg('temperature')
                                   ).annotate(humidity=Avg('humidity')
                                   ).values(
                                        'datetime',
                                        'pm25',
                                        'pm10',
                                        'co2',
                                        'tvoc',
                                        'temperature',
                                        'humidity')
    elif interval == 'day':
        measurements = measurements.annotate(datetime=TruncDay('timestamp')
                                   ).values('datetime'
                                   ).annotate(pm25=Avg('pm25')
                                   ).annotate(pm10=Avg('pm10')
                                   ).annotate(co2=Avg('co2')
                                   ).annotate(tvoc=Avg('tvoc')
                                   ).annotate(temperature=Avg('temperature')
                                   ).annotate(humidity=Avg('humidity')
                                   ).values(
                                        'datetime',
                                        'pm25',
                                        'pm10',
                                        'co2',
                                        'tvoc',
                                        'temperature',
                                        'humidity')
    else:
        measurements = measurements.annotate(datetime=F('timestamp')
                ).values('datetime', 'pm25', 'pm10', 'co2', 'tvoc', 'temperature', 'humidity')


    return JsonResponse(list(measurements), encoder=DjangoJSONEncoder, safe=False)

def ping(request):
    return JsonResponse({"ping": "pong"})
