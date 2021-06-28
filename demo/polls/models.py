from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.utils import timezone
import datetime

class Subject(models.Model):
    subject_text = models.CharField(max_length = 50)

    def __str__(self):
        return self.subject_text

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    #subject = models.CharField(max_length = 50)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'subject']

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text']
