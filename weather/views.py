from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import WeatherForm
from .repositories import WeatherRepository
from .serializers import WeatherSerializer

class WeatherView(View):
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getAll() 
        serializer = WeatherSerializer(weather, many=True) 
        return render(request, "home.html", {"weathers": serializer.data}) 

class WeatherGenerate(View):
    def get(self, request):
        form = WeatherForm()
        return render(request, "generate.html", {'form': form})

    def post(self, request):
        form = WeatherForm(request.POST)
        if form.is_valid():
            repository = WeatherRepository(collectionName='weathers')
            weather = {
                'temperature': form.cleaned_data['temperature'],
                'date': form.cleaned_data['date'],
                'city': form.cleaned_data['city'],
                'atmosphericPressure': form.cleaned_data['atmosphericPressure'],
                'humidity': form.cleaned_data['humidity'],
                'weather': form.cleaned_data['weather'],
            }
            serializer = WeatherSerializer(data=weather)
            if serializer.is_valid():
                repository.insert(serializer.validated_data)
                return redirect('Weather View')
            else:
                errors = serializer.errors
                return HttpResponse(f"Erros de validação: {errors}", status=400)
        return render(request, "generate.html", {'form': form})
    
class WeatherReset(View):
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()
        return redirect('Weather View')