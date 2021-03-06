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
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

def index(request):
  #template = loader.get_template('traptalk/index.html')
  #return HttpResponse(template.render(request), RequestContext(request))
  return render_to_response('traptalk/index.html',context_instance=RequestContext(request))


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
  
@csrf_exempt
def main(request):
  c = {}
  c.update(csrf(request))



  logged = False

  if request.POST.get('username') and request.POST.get('password'):
        logged = True

  if logged == False:
    response = JsonResponse({'status':'false','message': 'You must Log in to access this'}, status=403)
    return response


  username = request.POST['username']
  password = request.POST['password']

  if User.objects.filter(username__exact = username).exists():
    u = User.objects.get(username__exact = username)

    if(u.password != password):
      response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
      return response

    token = updateToken(u)

    friends = Friend.objects.filter(friend_one=u) | Friend.objects.filter(friend_two=u)
    messages = Message.objects.filter(message_from=u).order_by('sent') | Message.objects.filter(message_to=u).order_by('sent')

    context = {
        'token': token,
        'friends': friends,
        'messages': messages,
        'username': username,
    }

    template = loader.get_template('traptalk/main.html')
    return HttpResponse(template.render(context, request))

  else:
    response = JsonResponse({'status':'false','message': 'Username or Password incorrect'}, status=403)
    return response





def signout(request):
  logged = False

  if request.POST.get('token'):
        logged = True

  if logged == False:
    response = JsonResponse({'status':'false','message': 'You must Log in to access this'}, status=403)
    return response

  token = request.POST.get("token")

  ValidToken.objects.filter(token = token).delete()

  response = JsonResponse({'status':'false','message': 'Signout Succesful'}, status=200)
  return response


def addFriend(request):
  logged = False

  if request.POST.get('token'):
        logged = True

  if logged == False:
    response = JsonResponse({'status':'false','message': 'You must Log in to access this'}, status=403)
    return response


  username = request.POST.get("username")
  friendName = request.POST.get("friendName")
  token = request.POST.get("token")
  if(authorised(username,token) != True):
    response = JsonResponse({'status':'false','message': 'Session time out, please log in again'}, status=403)
    return response

  if User.objects.filter(username__exact = friendName).exists():
    friend = User.objects.get(username__exact = friendName)
    user = User.objects.get(username__exact = username)
    friendship = Friend(friend_one = user, friend_two = friend)
    friendship.save()
    response = JsonResponse({'status':'false','message': 'Friend Added Succesfully'}, status=200)
    return response

  response = JsonResponse({'status':'false','message': 'User with that I.D does not exist'}, status=200)
  return response


def send(request):
  logged = False

  if request.POST.get('token'):
        logged = True

  if logged == False:
    response = JsonResponse({'status':'false','message': 'You must Log in to access this'}, status=403)
    return response



  senderName = request.POST.get("senderName")
  receiverName = request.POST.get("receiverName")
  messageText = request.POST.get("messageText")
  token = request.POST.get("token")
  username = request.POST.get("username")

  if(authorised(username,token) == False):
    response = JsonResponse({'status':'false','message': 'Session time out, please log in again.'}, status=403)
    return response

  sender = User.objects.get(username__exact = senderName)
  receiver = User.objects.get(username__exact = receiverName)

  m = Message(message_from = sender, message_to = receiver, message_contents = messageText)
  m.save()
  response = JsonResponse({'status':'false','message': 'Sent Succesfully'}, status=200)
  return response


def getParticularMessages(request):
  logged = False

  if request.POST.get('token'):
    logged = True

  if logged == False:
    response = JsonResponse({'status':'false','message': 'You must Log in to access this'}, status=403)
    return response

  token = request.POST.get("token")
  username = request.POST.get("username")
  selected = request.POST.get("selected")

  if(authorised(username,token) == False):
    response = JsonResponse({'status':'false','message': 'Session time out, please log in again.'}, status=403)
    return response 

  if User.objects.filter(username__exact = username).exists():
    u = User.objects.get(username__exact = username)

  if User.objects.filter(username__exact = selected).exists():
    s = User.objects.get(username__exact = selected)

  messagesQuery = (Message.objects.filter(message_from=u).order_by('sent') & Message.objects.filter(message_to=s).order_by('sent'))| (Message.objects.filter(message_to=u).order_by('sent') & Message.objects.filter(message_from=s).order_by('sent'))

  messages = []
  messagesUser = []
  count = 0

  for msg in messagesQuery:
    messages.append(msg.message_contents)
    if msg.message_from == u:
      messagesUser.append(count)
    count = count + 1 


  
  response_data = {}
  response_data['messages'] = messages
  response_data['messagesUser'] = messagesUser

  #response = serializers.serialize("json", response_data)
  

  #return HttpResponse(response, content_type='application/json')
  response = JsonResponse(response_data, status=200)
  return response




#IF TOKEN VALID, UPDATES TOKEN IN VALID TOKENS
#FALSE RETURN MEANS TOKEN INVALID OR TIMED OUT
def authorised(username,token):
  return True

  u = User.objects.get(username = username)

  if ValidToken.objects.filter(validFor__exact = u).exists():
    t = ValidToken.objects.get(validFor__exact = u)

    if(t.token != token):
      return False

    issued = t.issued
    now = datetime.datetime.now(timezone.utc)
    difference = now - issued
    secondsDifference = difference.total_seconds()

    if secondsDifference < 3600:

      updateToken(u)
      return True

    else:
      return False

  else:
    return False

  return False

def updateToken(u):
  if ValidToken.objects.filter(validFor = u).exists():
    ValidToken.objects.filter(validFor = u).delete()

  token = get_random_string(length=50)
  t = ValidToken(token = token, validFor = u)
  t.save()

  return token