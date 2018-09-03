from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Question
from .BancoDeDados import *
from .models import *
from django.template import loader

# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def soma(resquest, n1, n2):
    return HttpResponse("Soma = {}".format(n1 + n2))

def buscapagamentos(request, id):

    try:
        pedido = Pedido.objects.get(id=id).status_pagamento

        if(pedido == True):
            resposta = 'Pago'
        else:
            resposta = 'Não Pago'

    except Pedido.DoesNotExist:
        resposta = 'Pedido Não Existe'


    return HttpResponse("Status do Pagamento: {}".format(resposta))

