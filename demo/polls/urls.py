from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote', views.vote, name='vote'),
    path('new_question/', views.NewQuestionView.as_view(), name='new_question'),
    #path('new_choice/', views.NewChoiceView.as_view(), name='new_choice')
]