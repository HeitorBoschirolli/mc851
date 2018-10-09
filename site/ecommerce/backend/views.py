from django.shortcuts import render
from datetime import *
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import urllib2
import json
import base64

# Create your views here.
def teste(request):

    url = 'http://ec2-18-231-28-232.sa-east-1.compute.amazonaws.com:3002/register'

    # data = json.dumps(status)
    data = json.loads(request.body)


    data = json.dumps(data)

    # base64string = base64.b64encode('%s:%s' % ('test', 'senhatest'))

    request2 = urllib2.Request(url=url, data=data, headers={'Content-Type': 'application/json'})
    # request2.add_header("Authorization", "Basic %s" % base64string)

    # request2.add_header('Content-Type': 'application/json')

    # import pdb
    # pdb.set_trace()

    try:
        # serializade_data = urllib2.urlopen(request2, data=json.dumps(data))
        serializade_data = urllib2.urlopen(request2).read()
        resposta = json.loads(serializade_data)

        return JsonResponse(resposta)

    except urllib2.URLError as e:
        print(e)


    return JsonResponse({'error': 502})

