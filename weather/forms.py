from django import forms

class WeatherForm(forms.Form):
    temperature = forms.FloatField(label='Temperatura')
    date = forms.DateTimeField(label='Data')
    city = forms.CharField(label='Cidade', required=False)
    atmosphericPressure = forms.CharField(label='Pressão Atmosférica', required=False)
    humidity = forms.CharField(label='Umidade', required=False)
    weather = forms.CharField(label='Clima', required=False)