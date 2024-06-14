from typing import Any
from datetime import datetime
from random import randrange
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib import messages

from user.authentication import *

from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializers import WeatherSerializer
from .forms import WeatherForm
from .exceptions import WeatherException

class WeatherView(View):

    authentication_classes = [JWTAuthentication]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        try:
            user, _ = self.authentication_classes[0].authenticate(request=request)
            request.user = user
        except Exception as e:
            pass
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.getAll())
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                # print('Data: ')
                # print(serializer.data)
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                # print('Error: ')
                # print(serializer.errors)
                objectReturn = {"error":serializer.errors}
        except WeatherException as e:
            objectReturn = {"error":e.message}

        if not request.user:
            objectReturn["errorAuth"] = "Usuário Não Autenticado"

        return render(request, "home.html", objectReturn)
    

class WeatherGenerate(View):

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now(),
            city='Sorocaba'
        )
        serializer = WeatherSerializer(data=weather.__dict__)
        if (serializer.is_valid()):
            repository.insert(serializer.data)
        else:
            print(serializer.errors)

        return redirect('Weather View')
    
class WeatherReset(View):

    def get(self, request): 
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()

        return redirect('Weather View')
    
class WeatherInsert(View):

    def get(self, request):
        weatherForm = WeatherForm()
        return render(request, "form.html", {"form": weatherForm})
    
    def post(self, request):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            repository = WeatherRepository(collectionName='weathers')
            weather_data = {
                'temperature': weatherForm.cleaned_data['temperature'],
                'date': weatherForm.cleaned_data['date'].strftime('%Y-%m-%d %H:%M:%S'),
                'city': weatherForm.cleaned_data['city'],
                'atmosphericPressure': weatherForm.cleaned_data['atmosphericPressure'],
                'humidity': weatherForm.cleaned_data['humidity'],
                'weather': weatherForm.cleaned_data['weather'],
            }
            serializer = WeatherSerializer(data=weather_data)
            if serializer.is_valid():
                repository.insert(serializer.validated_data)
                messages.success(request, "Weather data inserted successfully!")
                return redirect('Weather View')
            else:
                errors = serializer.errors
                messages.error(request, f"Validation errors: {errors}")
                return render(request, "form.html", {"form": weatherForm})

        errors = weatherForm.errors
        messages.error(request, f"Form errors: {errors}")
        return render(request, "form.html", {"form": weatherForm})
    

class WeatherEdit(View):

    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getByID(id)
        weatherForm = WeatherForm(initial=weather)

        return render(request, "form_edit.html", {"form":weatherForm, "id":id})
    
    def post(self, request, id):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            serializer.id = id
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.update(serializer.data, id)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')


class WeatherDelete(View):
    
    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteByID(id)

        return redirect('Weather View')
    

class WeatherFilter(View):
    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.get(data))
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                objectReturn = {"error":serializer.errors}
        except WeatherException as e:
            objectReturn = {"error":e.message}
  
        return render(request, "home.html", objectReturn)