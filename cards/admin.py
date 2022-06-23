from django.contrib import admin
from .models import DayWord, DayWordInLanguages, Learning, Meaning, LearningToMeaning

admin.site.register(DayWord)
admin.site.register(DayWordInLanguages)
admin.site.register(Learning)
admin.site.register(Meaning)
admin.site.register(LearningToMeaning)
