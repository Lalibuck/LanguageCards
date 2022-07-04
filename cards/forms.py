from .models import Words
from django import forms

def is_not_empty(form): # form validation
    if form:
        return True
    else:
        return False

class LearningForm(forms.Form):  # adding learn word form
    lword = forms.CharField(max_length=250)
    mword = forms.CharField(max_length=250)

    def clean_learn(self):
        lword = self.cleaned_data['lword']
        if not is_not_empty(lword):
            raise forms.ValidationError(
                u'Некорректные данные'
            )
        return lword

    def clean_mean(self):
        mword = self.cleaned_data['mword']
        if not is_not_empty(mword):
            raise forms.ValidationError(
                u'Некорректные данные'
            )
        return mword

    def save(self):
        word = Words(**self.cleaned_data)
        word.save()
        return word
