from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Learning(models.Model):
    word = models.CharField(unique=True, max_length=250)


class Meaning(models.Model):
    word = models.CharField(unique=True, max_length=250)


class LearningToMeaning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    learning = models.ForeignKey(Learning, on_delete=models.CASCADE)
    meaning = models.ForeignKey(Meaning, on_delete=models.CASCADE)
    learning_rate = models.IntegerField()
    added_time = models.DateField(auto_now_add=True)
    learning_time = models.DateField()
    learning_lang = models.CharField(max_length=250)
    meaning_lang = models.CharField(max_length=250)


class DayWord(models.Model):
    word = models.CharField(max_length=250)
    definition = models.TextField()
    added_date = models.DateField(auto_now_add=True)

    def get_index(self):
        return self.pk

    def get_url(self):
        return reverse('word', kwargs={'date': str(self.added_date)})

    def __str__(self):
        return self.word


class DayWordInLanguages(models.Model):
    word = models.ForeignKey(DayWord, on_delete=models.CASCADE)
    language = models.CharField(max_length=250)
    text = models.CharField(max_length=250)

    def __str__(self):
        return self.text

