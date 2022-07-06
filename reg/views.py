from .forms import RegisterForm
from django.shortcuts import render, redirect


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('')
    else:
        form =RegisterForm()
    return render(response, 'signup.html', {"form": form})