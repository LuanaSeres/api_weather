from django import forms

class WeatherForm(forms.Form):
    temperature = forms.FloatField(label='Temperatura')
    date = forms.DateTimeField(label='Data')
    city = forms.CharField(label='Cidade', required=False)
    atmosphericPressure = forms.CharField(label='Pressão Atmosférica', required=False)
    humidity = forms.CharField(label='Umidade', required=False)
    weather = forms.CharField(label='Clima', required=False)

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)