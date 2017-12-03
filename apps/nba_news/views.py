from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
import requests
from .models import User, UserManager, Comment

espnreq = requests.get('http://api.espn.com/v1/sports/basketball/nba/news?dates=20100219')

def index(request):
    return render (request, 'nba_news/index.html')

def login(request):
    email = request.POST["email"]
    password = request.POST["password"]
    check = User.objects.login(email, password)
    if check == True:
        user = User.objects.get(email = email)
        request.session["current_user"] = user.id
        return redirect('/nbanews')
    else:
        messages.warning(request, check[0])
        return redirect('/')

def logout(request):
    request.session['current_user'] = 0
    return redirect('/')

def registration(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    check = User.objects.register(first_name, last_name, email, password, confirm_password)
    if check == True:
        pwhashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(first_name = first_name, last_name = last_name, email = email, password = pwhashed)
        request.session["current_user"] = user.id
        return redirect("/nbanews")
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect("/")

def create_comment(request):
    check = Comment.objects.create_comment(request.POST['create_comment'])
    if check:
        Comment.objects.create_comment(create_comment = request.POST['create_comment'])
        return redirect('/')
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect('/')

def nbanews(request):
    current_user = User.objects.get(id = request.session['current_user'])
    context = {
                'current_user':current_user
                }
    return render(request, 'nba_news/nbanews.html', context)
