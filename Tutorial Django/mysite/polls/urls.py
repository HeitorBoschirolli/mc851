from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # Dentro do de todas URLS entradas que ocorrem após mysite.com/polls/ qual
    # função da view deve ser executada caso entre naquele path.
    # Caso entre no path raiz ('') devera ser executada a função
    # index de view (views.index)
    # Também criamos um nome para isso, chamando de index, ao qual podemos nos
    # referenciar mais tarde
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

]
