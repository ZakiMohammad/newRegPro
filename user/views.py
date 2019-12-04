from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import context

# main / index method
def index(request):
    return render(request, 'user/index.html', {'title':'index'})

# register user method
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            # For mail system
            htmly = get_template('user/Email.html')
            d = { 'username':username }
            subject, from_email, to = 'welcome', 'zeusreus011@gmail.com', email
            html_content = htmly.render(d)
            # store email data
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            # .send method used for sending messages
            messages.success(request, f'Your Acocunt has been created! You can Now Log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'user/register.html', { 'form':form, 'title':'register here'})

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' wecome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'Account do not exit plaese sign in')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form':form, 'title':'Log in'})
