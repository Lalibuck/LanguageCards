import datetime
from django.shortcuts import render
from .models import DayWord, DayWordInLanguages
from .api_relations import random_word, words_of_a_day, definition


def make_day_word():
    languages =("ru", "de", "fr", "es", "it")
    word = random_word()
    defin = definition(word)
    dayword = DayWord.objects.create(word=word, definition=defin)
    for lang in languages:
        DayWordInLanguages.objects.create(language=lang, text=words_of_a_day(lang, word))



def main(request):
    if len(DayWord.objects.filter(added_date__gte=datetime.date.today())):
        word = DayWord.objects.filter(added_date__gte=datetime.date.today())
    else:
        make_day_word()
        word = DayWord.objects.filter(added_date__gte=datetime.date.today())
    return render(request, 'main.html', {'words': word})

def word(request, date):

    if len(DayWord.objects.filter(added_date__gte=datetime.date.today())):
        make_day_word()
        word = DayWord.objects.filter(added_date__gte=datetime.date.today())
    else:
        word = DayWord.objects.filter(added_date__gte=datetime.date.today())
    return render(request, 'main.html', {'words': word})


