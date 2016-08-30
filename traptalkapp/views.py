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
    content = {'message': 'username already in use'}
    return HttpResponse(content = content, status = 200)


  u = User(username = username, password = password)
  u.save()
  content = {'message': 'success'}
  return HttpResponse(content = content, status = 200)
    
  
def signin(request):
  c = {}
  c.update(csrf(request))

  username = request.POST.get("username")
  password = request.POST.get("password")


  if User.objects.filter(username__exact = username).exists():
    u = User.objects.get(username__exact = username)

    if(u.password != password):
      content = {'message': 'username or password incorrect'}
      return HttpResponse(content = content, status= 403)


    token = get_random_string(length=50)
    u.token = token

    print(token)

    template = loader.get_template('Main.html')

    request.session['token'] = token
    return redirect(template.render(request))

  else:
    content = {'message': 'username or password incorrect'}
    return HttpResponse(content = content, status = 403)



  def main(request):
    token = request.session.pop('token', None)





#t = loader.get_template('myapp/index.html')
#c = {'foo': 'bar'}
#return HttpResponse(t.render(c, request), content_type='application/xhtml+xml')


#return HttpResponse("Username already in use.",c)

#content = {'please move along': 'nothing to see here'}
#return Response(content, status=status.HTTP_404_NOT_FOUND)



#return render_to_response("a_template.html", c)
#return render(request, 'polls/detail.html', {'user': user})


#Quote.objects.filter(author__exact = name) no
#Quote.objects.filter(author__author_name=name) yes
#Quote.objects.filter([model]__[field]__exact = [whatever])
#User.objects.get(User__username__exact = username)


#def index(request):
	#return HttpResponse("Hello world.")


#def detail(request, question_id):
 #   return HttpResponse("You're looking at question %s." % question_id)

#def results(request, question_id):
 #   response = "You're looking at the results of question %s."
  #  return HttpResponse(response % question_id)

#def vote(request, question_id):
 #   return HttpResponse("You're voting on question %s." % question_id)



 #def index(request):
   # latest_question_list = Question.objects.order_by('-pub_date')[:5]
  #  output = ', '.join([q.question_text for q in latest_question_list])
  #  return HttpResponse(output)



  #def index(request):
  #  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  #  template = loader.get_template('polls/index.html')
  #  context = {
  #      'latest_question_list': latest_question_list,
  #  }
  #  return HttpResponse(template.render(context, request))


 # def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
   # context = {'latest_question_list': latest_question_list}
   # return render(request, 'polls/index.html', context)



#def detail(request, question_id):
#    try:
 #       question = Question.objects.get(pk=question_id)
  #  except Question.DoesNotExist:
 #       raise Http404("Question does not exist")
 #   return render(request, 'polls/detail.html', {'question': question})



 #def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
 #   return render(request, 'polls/detail.html', {'question': question})



 #def vote(request, question_id):
  #  question = get_object_or_404(Question, pk=question_id)
  #  try:
  #      selected_choice = question.choice_set.get(pk=request.POST['choice'])
  #  except (KeyError, Choice.DoesNotExist):
   #     # Redisplay the question voting form.
   #     return render(request, 'polls/detail.html', {
   #         'question': question,
   #         'error_message': "You didn't select a choice.",
   #     })
  #  else:
  #     selected_choice.votes += 1
   #     selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
   #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


 # def results(request, question_id):
  #  question = get_object_or_404(Question, pk=question_id)
 #   return render(request, 'polls/results.html', {'question': question})


# class IndexView(generic.ListView):
  #  template_name = 'polls/index.html'
  #  context_object_name = 'latest_question_list'

  #  def get_queryset(self):
    #    """Return the last five published questions."""
   #     return Question.objects.order_by('-pub_date')[:5]


#class DetailView(generic.DetailView):
   # model = Question
   # template_name = 'polls/detail.html'


#class ResultsView(generic.DetailView):
  #  model = Question
 #   template_name = 'polls/results.html'


 #class IndexView(generic.ListView):
    #template_name = 'polls/index.html'
   # context_object_name = 'latest_question_list'

  #  def get_queryset(self):
   #     """Return the last five published questions."""
   #     return Question.objects.order_by('-pub_date')[:5]

   #def get_queryset(self):
   # """
   # Return the last five published questions (not including those set to be
   # published in the future).
   # """
   # return Question.objects.filter(
    #    pub_date__lte=timezone.now()
   # ).order_by('-pub_date')[:5]