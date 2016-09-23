from django.template import loader
from .models import User, ValidToken, Friend, Message
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
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import utc
import datetime
from pprint import pprint

def index(request):
  #template = loader.get_template('traptalk/index.html')
 #return HttpResponse(template.render(request))
  return render_to_response('traptalk/index.html');
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
  return redirect('/main')
  c = {}
  c.update(csrf(request))

  username = request.POST.get("username")
  password = request.POST.get("password")


  if User.objects.filter(username__exact = username).exists():
    u = User.objects.get(username__exact = username)

    if(u.password != password):
      response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
      return response



    if ValidToken.objects.filter(validFor__exact = u).exists():
      ValidToken.objects.filter(validFor = u).delete()


    token = get_random_string(length=50)
    t = ValidToken(token = token, validFor = u)
    t.save()

    request.session['username'] = username
    request.session['token'] = token
    return HttpResponseRedirect('main')




  else:
    response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
    return response


def signout(request):

    token = request.POST.get("token")
    username = request.POST.get("username")

    u = User.objects.get(username__exact = username)

    ValidToken.objects.filter(token = token, validFor = u).delete()


    response = JsonResponse({'status':'false','message': 'Sign Out Succesful'}, status=200)
    return response



def main(request):

  
  pprint (vars(request))


  token = request.session.get('token')
  username = request.session.get('username')


  print('token: ' , token)
  print('username: ' , username)


  u = User.objects.get(username = username)


  if ValidToken.objects.filter(validFor__exact = u).exists():
    t = ValidToken.objects.get(validFor__exact = u)

    if(t.token != token):
      print('1')
      raise Http404

    issued = t.issued
    now = datetime.datetime.now(timezone.utc)
    difference = now - issued
    secondsDifference = difference.total_seconds()
    print('token from client: ', token)
    print('token from DB: ' , t.token)
    print('timediff:' , secondsDifference)

    if secondsDifference < 3600:
      template = loader.get_template('traptalk/main.html')
      return HttpResponse(template.render(request))

    else:
      print('2')
      raise Http404

  else:
    print('3')
    raise Http404


def authenticated(username, token):
  u = User.objects.get(username = username)

  if ValidToken.objects.filter(validFor__exact = u).exists():
    t = ValidToken.objects.get(validFor__exact = u)

  if(t.token != token):
    print('1')
    raise Http404

  issued = t.issued
  now = datetime.datetime.now(timezone.utc)
  difference = now - issued
  secondsDifference = difference.total_seconds()
  print('token from client: ', token)
  print('token from DB: ' , t.token)
  print('timediff:' , secondsDifference)

  if secondsDifference < 3600:
    print('test')