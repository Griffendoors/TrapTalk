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

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.template import RequestContext

def index(request):
  #template = loader.get_template('traptalk/index.html')
 #return HttpResponse(template.render(request))
  #return render_to_response('traptalk/index.html');
  #return render_to_response('traptalk/index.html', context_instance=RequestContext(request))
  #200 Returned here automatically
  template = loader.get_template('traptalk/index.html')
  return HttpResponse(template.render(request))


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


    token = updateToken(u)

    friends = Friend.objects.filter(friend_one=u)
    sentMessages = Message.objects.filter(message_from=u).order_by('sent')
    recvMessages = Message.objects.filter(message_to=u).order_by('sent')

    context = {
        'token': token,
        'friends': friends,
        'sentMessages': sentMessages,
        'recvMessages': recvMessages,
        'username': username,
    }

    template = loader.get_template('traptalk/main.html')

    return HttpResponse(template.render(context, request))


  else:
    response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
    return response


def updateToken(u):

    if ValidToken.objects.filter(validFor = u).exists():
      ValidToken.objects.filter(validFor = u).delete()

    token = get_random_string(length=50)
    t = ValidToken(token = token, validFor = u)
    t.save()

    return token


def signout(request):

    token = request.POST.get("token")
    username = request.POST.get("username")

    u = User.objects.get(username__exact = username)

    ValidToken.objects.filter(token = token, validFor = u).delete()

    response = JsonResponse({'status':'false','message': 'Sign Out Succesful'}, status=200)
    return response


def addFriend(request):
 # pprint(vars(request))




  username = request.POST.get("username")
  friendName = request.POST.get("friendName")

  print(username)
  print(friendName)
  
  if User.objects.filter(username__exact = friendName).exists():
    friend = User.objects.get(username__exact = friendName)
    user = User.objects.get(username__exact = username)
    friendship = Friend(friend_one = user, friend_two = friend)
    friendship.save()
    response = JsonResponse({'status':'false','message': 'Friend Added Succesfully'}, status=200)
    return response


  response = JsonResponse({'status':'false','message': 'User with that I.D does not exist'}, status=200)
  return response








def main(request):
  #pprint(vars(request))






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