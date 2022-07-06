import datetime
import random
from django.shortcuts import render, redirect
from .models import DayWord, DayWordInLanguages, LearningToMeaning, Words
from .api_relations import random_word, words_of_a_day, definition
from .forms import LearningForm
from django.contrib.auth.decorators import login_required


def make_day_word():
    """add translation by different languages"""
    languages = ("ru", "de", "fr", "es", "it")
    """random word using random word api"""
    word = random_word()
    """definition of the word by ninjas dictionary"""
    defin = definition(word)
    dayword = DayWord.objects.create(word=word, definition=defin)
    dayword_id = dayword.get_index()
    for lang in languages:
        """saving to the db"""
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
        """checking credibility of the answer"""
        if word.learning_rate < 7:
            """right answer"""
            word.learning_rate += 1
            """updating the learning time"""
        word.learning_time = datetime.datetime.now() + rate[word.learning_rate]
        word.save()
    else:
        """wrong answer"""
        if word.learning_rate > 1:
            word.learning_rate -= 1
            """updating the learning rate"""
        word.learning_time = datetime.datetime.now() + rate[word.learning_rate]
        word.save()


def four_var(query):
    """one from four game"""
    vars = []
    true_word = Words.objects.get(id=query)
    """getting the right answer"""
    vars.append(true_word.mword)
    """getting three another random options"""
    some_words = Words.objects.exclude(id=query).order_by('?')[:3]
    for word in some_words:
        vars.append(word.mword)
    """option shuffling"""
    random.shuffle(vars)
    return vars


def main(request):
    """main page"""
    if DayWord.objects.filter(added_date=datetime.date.today()).exists():
        """if the word_of a day exists"""
        word = DayWord.objects.filter(added_date=datetime.date.today())
    else:
        """if the word_of a day not exists"""
        make_day_word()
        word = DayWord.objects.filter(added_date=datetime.date.today())
    return render(request, 'main.html', {'words': word})


def word(request, date):
    """a word of a day page"""
    if DayWord.objects.filter(added_date=datetime.date.today()).exists():
        word = DayWord.objects.filter(added_date=datetime.date.today())
    else:
        make_day_word()
        word = DayWord.objects.filter(added_date=datetime.date.today())
    return render(request, 'word.html', {'words': word})


@login_required(login_url='/login/')
def add(request):
    """adding words"""
    if request.method == "POST":
        ad_word = 'The word is succesfully added'
        form = LearningForm(request.POST)
        if form.is_valid():
            """saving the learning word"""
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
            """unsuccessful adding of the learning word"""
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
    """translation (if necessary) adding words"""
    if request.method == 'POST':
        mword = words_of_a_day('en', request.POST.get('lword'))
        """translation using microsoft translator api"""
        lword = request.POST.get('lword')
        return render(request, 'add.html', {
            'lword': lword, 'mword': mword
        })


@login_required(login_url='/login/')
def learn(request):
    """choosing the learning game page"""
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
    """one-from-four game"""
    if request.method == 'POST' and 'check' in request.POST:  # checking the answer
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now()).order_by(
            'learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        query = query[:1]
        """choosing apt words"""
        word = LearningToMeaning.objects.get(words=query)
        revise = Words.objects.get(id=query)
        if request.POST.get('mean').lower() == revise.mword.lower():
            """checking correctness of the answer"""
            """updating the db"""
            update_word(word, True)
            message = 'Correct'
        else:
            """updating the db"""
            update_word(word, False)
            message = 'Incorrect. The right answer is {}'.format(revise.mword)

        return render(request, 'one.html', {'words': query, 'message': message})
    else:
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now(), ).order_by(
            'learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        """choosing the firs one apt word"""
        query = query[:1]
        if query.exists():
            """have words to learn"""
            """generating four options"""
            vars = four_var(query)
            return render(request, 'one.html', {'words': query, 'vars': vars})
        else:
            """no words match"""
            message = 'No words to rehearse'
            return render(request, 'one.html', {'words': query, 'message': message})


def type(request):
    if request.method == 'POST' and 'check' in request.POST:
        """checking the answer"""
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now()).order_by(
            'learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        """getting apt appropriate options(choosing one of them)"""
        query = query[:1]
        word = LearningToMeaning.objects.get(words=query)
        revise = Words.objects.get(id=query)
        if request.POST.get('mean').lower() == revise.mword.lower():
            """checking the correctness of the answer"""
            update_word(word, True)
            message = 'Correct'
        else:
            update_word(word, False)
            message = 'Incorrect. The right answer is {}'.format(revise.mword)

        return render(request, 'type.html', {'words': query, 'message': message})
    else:
        query = Words.objects.filter(learningtomeaning__learning_lang=request.session['language'],
                                     learningtomeaning__user=request.user,
                                     learningtomeaning__learning_time__lte=datetime.datetime.now(), ).order_by(
            'learningtomeaning__learning_rate', 'learningtomeaning__learning_time')
        query = query[:1]
        if query.exists():
            return render(request, 'type.html', {'words': query})
        else:
            message = 'No words to rehearse'
            return render(request, 'type.html', {'words': query, 'message': message})


@login_required(login_url='/login/')
def vocab(request):
    """generate the list of learning words by language"""
    if request.method == 'POST':
        query = Words.objects.filter(learningtomeaning__learning_lang=request.POST.get('language')).filter(
            learningtomeaning__user=request.user).order_by('learningtomeaning__learning_rate',
                                                           'learningtomeaning__learning_time')
        if query.exists():
            """checking the existence of the list by opting params"""
            return render(request, 'vocab.html', {'query': query})
        else:
            error = "No added words"
            return render(request, 'vocab.html', {'error': error})
    else:
        return render(request, 'vocab.html')
