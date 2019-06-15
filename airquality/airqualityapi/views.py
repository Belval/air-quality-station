import datetime
import json

from dateutil import parser
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from airqualityapi.models import Measurement

def measurements(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    if start is not None:
        start = parser.parse(start)
    if end is not None:
        end = parser.parse(end)

    if start is None:
        start = datetime.datetime(1970, 1, 1)
    if end is None:
        end = datetime.datetime.now()

    serialized = serializers.serialize(
        "python",
        Measurement.objects.filter(Q(timestamp__gte=start, timestamp__lte=end)),
        fields=['timestamp', 'pm25', 'pm10'],
    )
    return JsonResponse([m['fields'] for m in serialized], safe=False)

def ping(request):
    return JsonResponse({"ping": "pong"})
