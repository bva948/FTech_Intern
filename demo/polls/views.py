#from django import template
from django.utils import timezone
from django.http import response
from django.http.request import QueryDict
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import ChoiceForm, Question, Choice, QuestionForm, Subject
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.views import generic, View

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['subject'] = Subject.objects.all()
        return context

    def get_queryset(self):
        subject_id = self.request.GET.get('subject_id', None)
        if (subject_id):
            return Question.objects.filter(subject = subject_id)
        return Question.objects.all()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class NewQuestionView(View):
    def get(self, request):
        form = QuestionForm
        return render(request, 'polls/new_question.html', {'form': form})

    def post(self, request):
        new_question_text = request.POST['question_text']
        subject = request.POST['subject']
        question = Question.objects.filter(question_text = new_question_text, subject = subject)
        if question is None:
            new_question = Question(question_text = new_question_text, pub_date = timezone.now(), subject = subject)
            new_question.save()
            return HttpResponse("Question saved")
        else:
            
            return HttpResponse("Question exists")

# class NewChoiceView(View):
#     def get(self, request):
#         form = ChoiceForm
#         return render(request, "polls/new_choice.html", {'form': form})

#     def post(self, request):
#         question = request.POST['question']
#         new_choice_text = request.POST['choice_text']
#         try:
#             c = Choice.objects.get(question = question, choice_text = new_choice_text)
#         except 
#         new_choice = Choice(question = question, choice_text = new_choice_text)
#         new_choice.save()
#         return HttpResponse("Saved")

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')
#     #template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     #output = ', '.join([q.question_text for q in latest_question_list])
#     #return HttpResponse(template.render(context, request)
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exists")
#     # return render(request, "polls/detail.html", {'question': question.question_text})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
#     #return HttpResponse("Result of question %s." %question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        seleted_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Select a choice"
        })
    else:
        seleted_choice.vote += 1
        seleted_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))
    #return HttpResponse("Vote for question %s." %question_id)
