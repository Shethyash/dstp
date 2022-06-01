import json
from lib2to3.pytree import Node
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Feeds
from home.models import Nodes
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from dstp import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.template.loader import render_to_string
from . tokens import generate_token

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
        if len(user_name) > 10:
            messages.error(request, 'Username must be less than 10 characters')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('/')
        myUser = User.objects.create_user(user_name, email, password1)
        myUser.first_name = first_name
        myUser.last_name = last_name
        myUser.is_active = False
        myUser.save()

        # welcome email
        subject = "Welcome to IOT Dashboard"
        message = "Welcome to IOT Dashboard, " + first_name + " " + \
            last_name + "!" + "Thank you for signing up with us"
        from_email = settings.EMAIL_HOST_USER
        to_list = ['202111046@daiict.ac.in', '202111045@daiict.ac.in']
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # email verification
        current_site = get_current_site(request)
        email_subject = 'Activate your account'
        msg = render_to_string('emails/acc_active_email.html', {
            'name': myUser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token': generate_token.make_token(myUser),
        })

        email = EmailMessage(email_subject, msg,
                             settings.EMAIL_HOST_USER, to=to_list)
        email.fail_silently = True
        email.send()

        messages.success(
            request, 'User created successfully, We have sent you an email to verify your account')
        return redirect('sign_in')
    return render(request, 'auth/sign_up.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verified')
        return redirect('/')
    else:
        messages.error(request, 'The link is invalid')
        return redirect('/')


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


@csrf_exempt
def store_feeds(request):

    if request.method == "POST":
        # store data to db
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(json.dumps(body))
        f_data = Feeds(
            node_id=body['node_id'],
            temprature=body['temprature'],
            humidity=body['humidity'],
            LWS=body['LWS'],
            soil_temprature=body['soil_temprature'],
            soil_moisture=body['soil_moisture'],
            battery_status=body['battery_status'])

        f_data.save()
        return HttpResponse(json.dumps(body))

    return HttpResponse()


def get_feeds(request):
    if request.method == "GET":
        id = request.GET.get("id")
        data = Feeds.objects.filter(node_id=id)
        return render(request, 'get_feeds.html', {'data': data})


def node(request):
    data = Nodes.objects.filter(user_id=request.user.id)
    return render(request, 'nodes/get_node.html', {'data': data})


def nodereg(request):
    if request.method == "POST":
        Name = request.POST.get('name')
        User_id = request.user.id
        Status = request.POST.get('status')
        Description = request.POST.get('desc')
        Latitude = request.POST.get('latitude')
        Longitude = request.POST.get('longitude')

        node_data = Nodes(
            name=Name,
            user_id=User_id,
            status=Status,
            description=Description,
            latitude=Latitude,
            longitude=Longitude
        )
        node_data.save()
        return redirect('/nodes')

    return render(request, 'nodes/reg_node.html')


def edit_node(request):
    id = request.GET.get("id")
    data = Nodes.objects.get(id=id)
    print(data)
    return render(request, 'nodes/reg_node.html', {'data': data})
