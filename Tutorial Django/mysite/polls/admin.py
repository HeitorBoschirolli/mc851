from django.contrib import admin
# . significa este diretorio (polls -> polls.models)
from .models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
