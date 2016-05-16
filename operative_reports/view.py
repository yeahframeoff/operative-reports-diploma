import os

from django.http import HttpResponse


def hello(request):
    times = int(os.getenv('TIMES', 3))
    return HttpResponse('Hello! ' * times)
