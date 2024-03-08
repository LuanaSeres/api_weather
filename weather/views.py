from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .models import WeatherEntity

from datetime import datetime
from random import randrange

class WeatherView(View):
    def get(self, request):
        weathers = []
        for i in range(10):
            weathers.append(
                WeatherEntity(
                    temperature=randrange(start=17, stop=40),
                    date=datetime.now()
                )
            )
        #return HttpResponse(weathers)
        
        return render(request, "home.html", {"weathers" : weathers})
