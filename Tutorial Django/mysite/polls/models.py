import datetime

from django.db import models
from django.utils import timezone

# Temos 2 tabelas, onde a tabela question tem os atributos de texto e data de publicacao
# e a classe Choice que tem uma referencia a uma pergunta e os campos textos e quantidade
# de votos

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # O argumento em texto é opcional e serve como um nome para se usar em vez de pub_date
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # cada Choice está relacionada a uma única Question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
