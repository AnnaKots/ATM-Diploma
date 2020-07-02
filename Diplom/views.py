# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
import json
import os

from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.models import User

from Diplom.forms import EnterForm, RegistrationForm

from django.shortcuts import render


def start(request):
    error_message = request.GET.get("error_message", "")
    success_message = request.GET.get("success_message", "")
    username = None
    return render(request, "introduction.html",
                  {"success_message": success_message, "error_message": error_message,
                   "user_name": username})


def index(request):
    names = ['Главная_улица', 'Парк', 'Аэропорт', 'Центр', 'Университет']
    error_message = request.GET.get("error_message", "")
    success_message = request.GET.get("success_message", "")
    username = None
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    return render(request, "index.html",
                  {"names": names, "success_message": success_message, "error_message": error_message,
                   "user_name": username})


def index_for_all(request):
    error_message = request.GET.get("error_message", "")
    success_message = request.GET.get("success_message", "")
    username = None
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    return render(request, "for_all_index.html",
                  {"success_message": success_message, "error_message": error_message,
                   "user_name": username})


def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def registration(request):
    errors = []
    success = ''
    if request.method == 'POST':
        if 'signIn' in request.POST:
            return HttpResponseRedirect('/login/')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']

            users = User.objects.all()
            usernames = []
            for x in users:
                usernames.append(x.username)

            if form.cleaned_data['password'] != form.cleaned_data['password2']:
                errors.append('Пароли должны совпадать')
            elif usernames.count(username) != 0:
                errors.append('Такой логин уже занят')
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                user.save()
                return HttpResponseRedirect('/login/')

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form, 'errors': errors, 'success': success})


def login(request):
    errors = []
    names_dict = {}
    if request.method == 'POST':
        if 'reg' in request.POST:
            return HttpResponseRedirect('/registration/')
        form = EnterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            names_dict = {x: request.POST.get(x, "") for x in ["username", "password"]}
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                errors.append('Неверно введён логин или пароль')
    else:
        form = EnterForm()
    return render(request, 'login.html', {'form': form, 'errors': errors, 'names_dict': names_dict})


def calculate(request):
    error_message = request.GET.get("error_message", "")
    success_message = request.GET.get("success_message", "")
    if request.method == 'POST':
        ret = request.POST
        atm_name = str(ret["atm_name"])
        date = str(ret["date"])
        festival = int(ret["festival"].replace('"', ''))
        working_day = int(ret["working_day"].replace('"', ''))

        print('ВРЕМЯ ДО')
        a = os.popen(
            'python script.py ' + '"' + atm_name + '"' + ' ' + '"' + date + '"' + ' ' + str(festival) + ' ' + str(
                working_day)).read()
        print('ВРЕМЯ ПОСЛЕ')
        print(a)
        return HttpResponse(a)
    username = None
    if not request.user.is_authenticated:
        return redirect(reverse('login'))


def calculate_for_all(request):
    error_message = request.GET.get("error_message", "")
    success_message = request.GET.get("success_message", "")
    if request.method == 'POST':
        ret = request.POST
        date = "'" + (ret["date"]) + "'"
        festival = int(ret["festival"].replace('"', ''))
        working_day = int(ret["working_day"].replace('"', ''))

        a = os.popen(
            'python script_for_all.py ' + '"' + str(date) + '"' + ' ' + str(festival) + ' ' + str(
                working_day)).read()
        print(a)
        return HttpResponse(a)
    username = None
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
