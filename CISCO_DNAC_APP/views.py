from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from CISCO_DNAC_APP.models import *
from CISCO_DNAC_APP.forms import *
from CISCO_DNAC_APP.simulate_webhook_events import simulate_event
import time, threading, requests, json
from requests.auth import HTTPBasicAuth
import urllib3


from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def index(request):
    return render(request, "DNAC/index.html")


def health(request):
    controllers = DnacControllers.objects.all().order_by('name')
    return render(request, "DNAC/health.html", {'controllers': controllers})


def events(request):
    # Make this one searchable
    return render(request, "DNAC/events.html")


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


def controller_health(request, controller_id):
    controllers = DnacControllers.objects.all().order_by('name')
    controller = DnacControllers.objects.get(pk=controller_id)

    health = json.loads(get_network_health(controller=controller))

    controller_health = {'overall': 0, 'access': 0, 'distribution': 0, 'core': 0, 'wlc': 0, 'ap': 0}
    controller_count = {}

    if 'error' in health:
        print(health['error'])
        messages.add_message(request, messages.ERROR, 'An error ocurred: '+health['error'])
    else:
        for item in health['response']:
            controller_health.update({'overall': item['healthScore']})
        for item in health['healthDistirubution']:  # Yes, Cisco really has a typo like this in their API :-(
            print(item)
            controller_health.update({item['category'].lower(): item['healthScore']})
        for item in health['healthDistirubution']:
            controller_count.update({item['category']: {'total': item['totalCount'], 'good': item['goodCount'], 'fair': item['fairCount'], 'bad': item['badCount'], 'unmonitored': item['unmonCount'] }})
        print(controller_count)

    return render(request, "DNAC/health.html", {'controllers': controllers, 'controller': controller,
                                                'controller_health': controller_health, 'controller_count': controller_count})

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
    messages.add_message(request, messages.SUCCESS, 'Simulating webhook events...')
    return render(request, "DNAC/index.html")


def request_controller_stats():
    simulate_event()
    print(time.ctime())
    threading.Timer(10, request_controller_stats).start()  # Restart function every 10 second interval
    return


def network_device_list(controller):
    """
    Get a list of network devices
    """
    url = controller.url.rstrip('/')+"/api/v1/network-device"
    get_intent_api(url, controller)
    return


def get_network_health(controller):
    """
    Returns Overall Network Health information by Device category (Access, Distribution, Core, Router, Wireless)
    for any given point of time.
    """
    url = controller.url.rstrip('/')+"/dna/intent/api/v1/network-health"
    params = "timestamp=" + str(int((time.time()) * 1000))
    result = get_intent_api(url, controller, params)
    return result


def get_site_count(controller):
    """
    API to get site count
    https://developer.cisco.com/site/dna-center-rest-api/
    """
    url = controller.url.rstrip('/')+"/dna/intent/api/v1/site/count"
    get_intent_api(url, controller)
    return


def get_intent_api(url, controller, params=None):
    """
    Generic fuction to GET information via the Intent API
    """
    print(params)
    print("\nExecuting GET '%s'\n" % url)
    token = generate_auth_token(controller.url, controller.username, controller.password)
    headers = {
        'content-type': "application/json",
        '__runsync': "true",
        '__timeout': "30",
        '__persistbapioutput': "true",
        'X-Auth-Token': token
    }
    resp = requests.get(url, headers=headers, params=params, verify=False)
    print(resp.status_code)
    response_json = resp.json()
    print(json.dumps(response_json, indent=4), '\n')
    result = json.dumps(response_json, indent=4)
    return result


def generate_auth_token(url, username, password):
    # The url for the post token API request
    post_url = url.rstrip('/')+"/api/system/v1/auth/token"
    # All DNAC REST API query and response content type is JSON
    headers = {'content-type': 'application/json'}
    # POST request and response
    try:
        r = requests.post(post_url, auth=HTTPBasicAuth(username=username, password=password), headers=headers, verify=False)
        # Remove '#' if need to print out response
        token = r.json()["Token"]  # Extract token from json response {"Token":"...."}
        r.raise_for_status()
        # return service token
        return token
    except requests.exceptions.ConnectionError as e:
        # Something wrong, cannot get service token
        print ("Error: %s" % e)
        sys.exit ()


def listen_web_hooks(request):
    # Currently this function does not require authentication
    if request.method == 'POST':
        # print(dir(request))
        # print(request.user)
        # print(request.META)
        # print(request.headers)
        print(request.META['REMOTE_ADDR'])
        print(request.body)
        # save event to models
        """
        instance_id <== instanceId
        source_ip <== request.META['REMOTE_ADDR']
        title <== title
        category <== Category
        domain <== domain
        severity <== severity
        timestamp <== timestamp (integer)
        actual_service_id <== actualServiceId
        issue_description <== ["enrichmentInfo"]["issueDetails"]["issue"][0]["issueSummary"]
        """
        try:
            post = json.loads(request.body)
            print(post["enrichmentInfo"]["issueDetails"]["issue"][0]["issueSummary"])

            event = WebhookEvents()
            event.instance_id = post["instanceId"]
            event.source_ip = request.META['REMOTE_ADDR']
            event.title = post["title"]
            event.category = post["category"]
            event.domain = post["domain"]
            event.severity = post["severity"]
            # https: // stackoverflow.com / questions / 31548132 / python - datetime - fromtimestamp - yielding - valueerror - year - out - of - range
            # Need to divide the provided timestamp by 1000 to convert ms to seconds
            event.timestamp = datetime.fromtimestamp(post["timestamp"]/1000)
            event.actual_service_id = post["actualServiceId"]
            event.issue_description = post["enrichmentInfo"]["issueDetails"]["issue"][0]["issueSummary"]

            event.save()
        except Exception as e:
            print(e)
            return HttpResponse("ERROR", status=500)
    else:
        HttpResponse("Method not allowed", status=403)
    return HttpResponse("OK")
