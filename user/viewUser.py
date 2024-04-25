from django.shortcuts import render, redirect
from django.views import View
from weather.forms import UserForm, LoginForm
from user.modelUser import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.repositoryUser import UserRepository
from django.http import JsonResponse

    
class UserGenerate(View):
    def get(self, request):
        form = UserForm()
        return render(request, "userGenerate.html", {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            # Criar um objeto User com os dados do formulário
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            repository = UserRepository(collectionName='users')
            repository.insert(user)
            return redirect('User List')
        
        return render(request, "userGenerate.html", {'form': form})

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuário não encontrado. Por favor, registre-se.')
                return redirect('register')  # Redireciona para a página de registro
        return render(request, 'login.html', {'form': form})

class UserList(View):
    def get(self, request):
        repository = UserRepository(collectionName='users')
        users = repository.getAll()
        return render(request, "userList.html", {'users': users})

class UserEdit(View):
    def get(self, request, id):
        repository = UserRepository(collectionName='users')
        user = repository.getByID(id)
        userForm = UserForm(initial=user)
        return render(request, "userEdit.html", {"form": userForm, "id": id})

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
        return render(request, "userList.html", {'users': users})

class UserDelete(View):
    def get(self, request, id):
        repository = UserRepository(collectionName='users')
        repository.deleteByID(id)
        users = repository.getAll()
        return render(request, "userList.html", {'users': users})
    

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Autenticar o usuário manualmente
                request.user = user
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'message': 'Invalid password'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid username'}, status=400)