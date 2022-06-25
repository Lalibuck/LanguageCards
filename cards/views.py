import datetime
from django.shortcuts import render
from .models import DayWord, DayWordInLanguages, LearningToMeaning, Words
from .api_relations import random_word, words_of_a_day, definition
from .forms import LearningForm

def make_day_word():
    languages = ("ru", "de", "fr", "es", "it")
    word = random_word()
    defin = definition(word)
    dayword = DayWord.objects.create(word=word, definition=defin)
    dayword_id = dayword.get_index()
    for lang in languages:
        DayWordInLanguages.objects.create(word=DayWord.objects.get(id=dayword_id),
                                          language=lang,
                                          text=words_of_a_day(lang, word)
                                          )



def main(request):
    if DayWord.objects.filter(added_date=datetime.date.today()).exists():
        word = DayWord.objects.filter(added_date=datetime.date.today())
    else:
        make_day_word()
        word = DayWord.objects.filter(added_date=datetime.date.today())
    return render(request, 'main.html', {'words': word})

def word(request, date):

    if DayWord.objects.filter(added_date=datetime.date.today()).exists():
        word = DayWord.objects.filter(added_date=datetime.date.today())
    else:
        make_day_word()
        word = DayWord.objects.filter(added_date=datetime.date.today())
    return render(request, 'word.html', {'words': word})


def add(request):
    if request.method == "POST":
        ad_word = 'The word is succesfully added'
        form = LearningForm(request.POST)
        if form.is_valid():
            form = form.save()
            LearningToMeaning.objects.create(user=request.user,
                                            words=Words.objects.get(id=form.pk),
                                             learning_rate=1,
                                             learning_time=datetime.date.today() + datetime.timedelta(days=1),
                                             learning_lang=request.POST.get('language'),
                                             meaning_lang='en'
                                              )
            form = LearningForm()
            return render(request, 'add.html', {
                            'form': form,
                            'ad_word': ad_word,
                            })
        else:
            ad_word = 'The word is not added'
            return render(request, 'add.html', {
                            'form': form,
                            'ad_word': ad_word,
                            })
    else:
        form = LearningForm()
    return render(request, 'add.html', {
                    'form': form,
                })