from django.template import loader
from .models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.utils import timezone
from django.core.context_processors import csrf
from django.utils.crypto import get_random_string
from django.shortcuts import render_to_response
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.core import serializers
from django.http import JsonResponse


def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render(request))
  #200 Returned here automatically


def signup(request):

  c = {}
  c.update(csrf(request))

  username = request.POST.get("username")
  password = request.POST.get("password")

  if User.objects.filter(username__exact = username).exists():
      response = JsonResponse({'status':'false','message': 'Username in use'}, status=200)
      return response

  u = User(username = username, password = password)
  u.save()

  response = JsonResponse({'status':'false','message': 'Signup Success'}, status=200)
  return response
   
  


def signin(request):
  c = {}
  c.update(csrf(request))

  username = request.POST.get("username")
  password = request.POST.get("password")


  if User.objects.filter(username__exact = username).exists():
    u = User.objects.get(username__exact = username)

    if(u.password != password):
      response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
      return response


    token = get_random_string(length=50)
    u.token = token

    #template = loader.get_template('main.html')

    request.session['token'] = token

    #return redirect(template.render(request))

    location = 'main.html'
    response = HttpResponse(location, status=200)
    response['Location'] = location
    return response
   #return redirect('main.html')

  else:
    response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
    return response




def main(request):
  token = request.session.pop('token', None)
