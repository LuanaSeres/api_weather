from django.urls import path
from weather.views import WeatherView, WeatherGenerate

urlpatterns = [
    path('', WeatherView.as_view(), name='Weather View'),
    path('', WeatherGenerate.as_view(), name='Weather Generate'),
]
