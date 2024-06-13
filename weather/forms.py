from django import forms

class WeatherForm(forms.Form):
    temperature = forms.FloatField()
    date = forms.DateTimeField()
    city = forms.CharField(max_length=255)
    atmosphericPressure = forms.FloatField(required=False)
    humidity = forms.FloatField(required=False)
    weather = forms.CharField(max_length=255, required=False)

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)