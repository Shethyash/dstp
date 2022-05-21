from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        fName = request.user.first_name
        return render(request, 'index.html', {'fName': fName})
    else:
        return redirect('/')


def sign_up(request):
    if request.method == "POST":
        user_name = request.POST.get('uName')
        first_name = request.POST.get('fName')
        last_name = request.POST.get('lName')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        myUser = User.objects.create_user(user_name, email, password1)
        myUser.first_name = first_name
        myUser.last_name = last_name
        myUser.save()

        messages.success(request, 'User created successfully')
        return redirect('sign_in')
    return render(request, 'auth/sign_up.html')


def sign_in(request):
    if request.method == "POST":
        user_name = request.POST.get('uName')
        password = request.POST.get('password')

        user = authenticate(username=user_name,    password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('/')
    return render(request, 'auth/sign_in.html')


def sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('/home')


def nodes(request):
    return render(request, 'nodes.html')


def node(request, node_id):
    return render(request, 'node.html')


def add_node(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

    return render(request, 'add_node.html')
