from django.shortcuts import render, redirect
from django.views import View
from user.models import UserEntity
from user.repository import UserRepository
from django.http import JsonResponse
from .authentication import *
from weather.forms import UserForm, LoginForm
from django.utils.deprecation import MiddlewareMixin

class UserTokenizer(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                token = generateToken(user)
                response = JsonResponse({'token': token})
                response.set_cookie('jwt_token', token)
                return response
            else:
                return JsonResponse({'error': 'User and/or password incorrect'}, status=400)
        else:
            return JsonResponse({'error': 'Username and password must be provided'}, status=400)


class UserGenerate(View):
    def get(self, request):
        form = UserForm()
        return render(request, "user_generate.html", {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = UserEntity(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            repository = UserRepository(collectionName='users')
            repository.insert(user)
            return redirect('Weather View')
        
        return render(request, "user_generate.html", {'form': form})

class UserList(View):
    def get(self, request):
        repository = UserRepository(collectionName='users')
        users = repository.getAll()
        return render(request, "user_list.html", {'users': users})


class UserEdit(View):
    def get(self, request, id):
        repository = UserRepository(collectionName='users')
        user = repository.getByID(id)
        userForm = UserForm(initial=user)
        return render(request, "user_edit.html", {"form": userForm, "id": id})

    def post(self, request, id):
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            user_data = {
                'username': userForm.cleaned_data['username'],
                'email': userForm.cleaned_data['email'],
                'password': userForm.cleaned_data['password'],
            }
            repository = UserRepository(collectionName='users')
            repository.update(user_data, id)
        else:
            print(userForm.errors)
        users = repository.getAll()
        return render(request, "user_list.html", {'users': users})


class UserDelete(View):
    def get(self, request, id):
        repository = UserRepository(collectionName='users')
        repository.deleteByID(id)
        users = repository.getAll()
        return render(request, "user_list.html", {'users': users})
    

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
      
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token = generateToken(user)
            response = redirect('Weather View')
            response.set_cookie('jwt_token', token)
            return response
        else:
            form = LoginForm()
            error_message = 'Credenciais inválidas'
            return render(request, 'login.html', {'form': form, 'error_message': error_message})

class UserLogout(View):
    def get(self, request):
        response = redirect('Weather View')  
        response.delete_cookie('jwt_token')
        return response
    
class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt_token')
        if token:
            user = getAuthenticatedUser(token)
            if user:
                request.user = user
            else:
                request.user = None
        else:
            request.user = None