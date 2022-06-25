from django.contrib import admin
from .models import DayWord, DayWordInLanguages, Words, LearningToMeaning

admin.site.register(DayWord)
admin.site.register(DayWordInLanguages)
admin.site.register(Words)
admin.site.register(LearningToMeaning)
