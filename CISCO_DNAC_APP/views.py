from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from CISCO_DNAC_APP.models import *
from CISCO_DNAC_APP.forms import *
import time, threading, requests, json
from requests.auth import HTTPBasicAuth


def index(request):
    return render(request, "DNAC/index.html")


def manage_controllers(request):
    if request.method == 'POST':
        form = AddControllerForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            pass
    else:
        pass
    form = AddControllerForm()
    controllers = DnacControllers.objects.all().order_by('name')
    return render(request, "DNAC/manage_controllers.html", {'controllers': controllers, 'form': form})


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


def collect_statistics(request):
    if request.method == 'POST':
        request_controller_stats()
    else:
        pass
    return render(request, "DNAC/index.html")


def request_controller_stats():
    # Get controller list
    controllers = DnacControllers.objects.all()
    for controller in controllers:
        print(controller.name)
        token = generate_auth_token(controller.url, controller.username, controller.password)
        headers = {"content-type": "application/json", "X-Auth-Token": token}
        ## Make a generic get function for this!
        # Get DNA Center information
        # https://developer.cisco.com/site/dna-center-rest-api/
        url = controller.url.rstrip('/')+"/dna/intent/api/v1/network-health"
        print("\nExecuting GET '%s'\n" % url)
        resp = requests.get(url, headers=headers, verify=False)
        response_json = resp.json()
        print(json.dumps(response_json, indent=4), '\n')
        result = json.dumps(response_json, indent=4)
    # authenticate
    # get data
    # save to models
    # send some result of starting the collection via a flash message
    print(time.ctime())
    threading.Timer(60, request_controller_stats).start()  # Collect information with a 60 second interval
    return


def generate_auth_token(url, username, password):
    # The url for the post token API request
    post_url = url.rstrip('/')+"/api/system/v1/auth/token"
    # All DNAC REST API query and response content type is JSON
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, auth=HTTPBasicAuth(username=username, password=password), headers=headers, verify=False)
        # Remove '#' if need to print out response
        print (r.text)
        r.raise_for_status()
        # return service token
        return r.json()["Token"]
    except requests.exceptions.ConnectionError as e:
        # Something wrong, cannot get service token
        print ("Error: %s" % e)
        sys.exit ()