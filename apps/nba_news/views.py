from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, UserManager, Comment
from django.contrib import messages
import requests
import bcrypt

espnreq = requests.get('http://api.espn.com/v1/sports/basketball/nba/news?dates=20100219')

def index(request):
    return render(request, 'nba_news/index.html')
def login_reg(request):
    return render (request, "nba_news/login_reg.html")

def registration(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]
    check = User.objects.register(first_name, last_name, email, password, confirm_password)
    if check:
        pwhashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(
            first_name = request.POST["first_name"]
            , last_name = request.POST["last_name"]
            , email = request.POST["email"]
            , password = pwhashed)
        request.session["current_user"] = user.id
        return redirect("/")
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect("/")

def login(request):
    check = User.objects.login(
        request.POST["email"]
        , request.POST["password"])

    if check:
        user = User.objects.get(email = request.POST['email'])
        request.session["current_user"] = user.id
        return redirect('/')
    else:
        messages.warning(request, check[0])
        return redirect('/')

def logout(request):
    request.session['current_user'] = 0
    return redirect('/')

def create_comment(request):
    check = Comment.objects.create_comment(request.POST['create_comment'])
    if check:
        Comment.objects.create_comment(create_comment = request.POST['create_comment'])
        return redirect('/')
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect('/')
