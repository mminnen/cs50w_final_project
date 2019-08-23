from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from CISCO_DNAC_APP.models import *
from CISCO_DNAC_APP.forms import *


def index(request):
    return render(request, "DNAC/index.html")


def manage_controllers(request):
    controllers = DnacControllers.objects.all().order_by('name')
    form = AddControllerForm()
    return render(request, "DNAC/manage_controllers.html", {'controllers': controllers, 'form': form})


def add_controller(request):
    controllers = DnacControllers.objects.all().order_by('name')
    ### If form posted add to database!!!!!!!!!!!
    return render(request, "DNAC/manage_controllers.html", {'controllers': controllers})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
