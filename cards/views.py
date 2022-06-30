import datetime
import random
from django.shortcuts import render, redirect
from .models import DayWord, DayWordInLanguages, LearningToMeaning, Words
from .api_relations import random_word, words_of_a_day, definition, translate_word
from .forms import LearningForm
from django.contrib.auth.decorators import login_required


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

def update_word(query, answer):
    rate = {1: datetime.timedelta(days=1),
            2: datetime.timedelta(days=3),
            3: datetime.timedelta(days=5),
            4: datetime.timedelta(days=10),
            5: datetime.timedelta(days=30),
            6: datetime.timedelta(days=90),
            7: datetime.timedelta(days=180),
            }
    word = query
    if answer:
        if word.learning_rate < 7:
            word.learning_rate += 1
        word.learning_time = datetime.datetime.now() + rate[word.learning_rate]
        word.save()
    else:
        if word.learning_rate > 1:
            word.learning_rate -= 1
        word.learning_time = datetime.datetime.now() + rate[word.learning_rate]
        word.save()



def four_var(query):
    vars = []
    true_word = Words.objects.get(id=query)
    vars.append(true_word.mword)
    some_words = Words.objects.exclude(id=query).order_by('?')[:3]
    for word in some_words:
        vars.append(word.mword)
    random.shuffle(vars)
    return vars

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


@login_required(login_url='/login/')
def add(request):
    if request.method == "POST":
        ad_word = 'The word is succesfully added'
        form = LearningForm(request.POST)
        if form.is_valid():
            form = form.save()
            LearningToMeaning.objects.create(user=request.user,
                                            words=Words.objects.get(id=form.pk),
                                             learning_rate=1,
                                             learning_time=datetime.datetime.now() + datetime.timedelta(days=1),
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

def translate(request):
    if request.method == 'POST':
        mword = words_of_a_day('en', request.POST.get('lword'))
        lword = request.POST.get('lword')
        return render(request, 'add.html', {
            'lword': lword, 'mword': mword
        })


@login_required(login_url='/login/')
def learn(request):
    if request.method == "POST":
        if request.POST.get('game') == 'type':
            request.session['language'] = request.POST.get('language')
            return redirect('type/')
        elif request.POST.get('game') == 'one':
            request.session['language'] = request.POST.get('language')
            return redirect('one/', request.POST.get('language'))
    else:
        return render(request, 'learn.html')


def one(request):

    if request.method == 'POST' and 'check' in request.POST:
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now()).order_by('learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        query = query[:1]
        word = LearningToMeaning.objects.get(words=query)
        revise = Words.objects.get(id=query)
        if request.POST.get('mean').lower() == revise.mword.lower():
            update_word(word, True)
            message = 'Correct'
        else:
            update_word(word, False)
            message = 'Incorrect. The right answer is {}'.format(revise.mword)

        return render(request, 'one.html', {'words': query, 'message': message})
    else:
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now(), ).order_by('learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        query = query[:1]

        if query.exists():
            vars = four_var(query)
            return render(request, 'one.html', {'words': query, 'vars': vars})
        else:
            message = 'No words to rehearse'
            return render(request, 'one.html', {'words': query, 'message': message})


def type(request):
    if request.method == 'POST' and 'check' in request.POST:
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now()).order_by('learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        query = query[:1]
        word = LearningToMeaning.objects.get(words=query)
        revise = Words.objects.get(id=query)
        if request.POST.get('mean').lower() == revise.mword.lower():
            update_word(word, True)
            message = 'Correct'
        else:
            update_word(word, False)
            message = 'Incorrect. The right answer is {}'.format(revise.mword)

        return render(request, 'type.html', {'words': query, 'message': message})
    else:
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now(), ).order_by('learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        query = query[:1]
        if query.exists():
          return render(request, 'type.html', {'words': query})
        else:
            message = 'No words to rehearse'
            return render(request, 'type.html', {'words': query, 'message': message})


def vocab(request):
    if request.method == 'POST':
          query = Words.objects.filter(learningtomeaning__learning_lang=request.POST.get('language')).filter(learningtomeaning__user=request.user)
          if query.exists():
              return render(request, 'vocab.html', {'query': query})
          else:
              error = "No added words"
              return render(request, 'vocab.html', {'error': error})
    else:
        return render(request, 'vocab.html')
