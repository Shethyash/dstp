import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from home.models import Feeds
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
        # f_data = Feeds(
        #     c_id=body['c_id'],
        #     entry_id=body['entry_id'],
        #     field1=body['field1'],
        #     field2=body['field2'],
        #     field3=body['field3'],
        #     field4=body['field4'],
        #     field5=body['field5'],
        #     field6=body['field6'],
        #     created_at=body['created_at'],
        #     updated_at=body['updated_at'])
        # f_data.save()
        return HttpResponse(json.dumps(body))
    return HttpResponse()


def get_feeds(request):
    data = Feeds.objects.all()
    return render(request, 'get_fees.html', {'data': data})


def node(request):
    if request.method == "POST":
        name = request.POST.get('name')
        user_id = request.POST.get('user_id')
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
    return render(request, 'nodes/add_node.html')
