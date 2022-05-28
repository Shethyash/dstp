import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Feeds
from django.views.decorators.csrf import csrf_exempt
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
        if User.objects.filter(username=user_name):
            messages.error(request, 'Username already exists')
            return redirect('/')
        if User.objects.filter(email=email):
            messages.error(request, 'Email already exists')
            return redirect('/')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('/')
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

def add_node(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
        status = request.POST.get('status')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

    return render(request, 'add_node.html')

@csrf_exempt
def store_feeds(request):

    if request.method == "POST":
        # store data to db
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(json.dumps(body))
        f_data = Feeds(
            node_id=body['node_id'],
            entry_id=body['entry_id'],
            temprature=body['temprature'],
            humidity=body['humidity'],
            LWS=body['LWS'],
            soil_temprature=body['soil_temprature'],
            soil_moisture=body['soil_moisture'],
            battery_status=body['battery_status'],
            created_at=body['created_at'])
        
        f_data.save()
        return HttpResponse(json.dumps(body))
    
    return HttpResponse()

def get_feeds(request):
    data = Feeds.objects.all()
    return render(request, 'get_feeds.html', {'data': data})

def node(request):
    
    return render(request, 'nodes/add_node.html')

def nodereg(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('uid')
        status = request.POST.get('status')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
    if request.method == "PUT":
        name = request.PUT.get('name')
        user_id = request.PUT.get('user_id')
        status = request.PUT.get('status')
        description = request.PUT.get('description')
        latitude = request.PUT.get('latitude')
        longitude = request.PUT.get('longitude')
    return render(request,'nodes/reg_node.html')