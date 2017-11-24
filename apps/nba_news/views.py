from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, UserManager
from django.contrib import messages
import bcrypt
from nba_data import Client, CurrentSeasonOnly, Season

def index(request):
    return render(request, 'nba_news/index.html')

def registration(request):
    check = User.objects.register(
        request.POST["first_name"]
        , request.POST["last_name"]
        , request.POST["email"]
        , request.POST["password"]
        , request.POST["confirm_password"])

    if check == True:
        passwordinput = request.POST["password"].encode('utf-8')
        hashed = bcrypt.hashpw(passwordinput, bcrypt.gensalt())
        user = User.objects.create(
            first_name = request.POST["first_name"]
            , last_name = request.POST["last_name"]
            , email = request.POST["email"]
            , password = hashed)
        request.session["current_user"] = user.id
        return redirect("/nba_news")
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect("/")

def login(request):
    check = User.objects.login(
        request.POST["email"]
        , request.POST["password"])

    if check == True:
        user = User.objects.get(email = request.POST['email'])
        request.session["current_user"] = user.id
        return redirect('/nba_news')
    else:
        messages.warning(request, check[0])
        return redirect('/')

def logoutr(request):
    request.session['current_user'] = 0
    return redirect('/')

def get_players_for_2015_season():
    return Client.get_players_for_season(season = Season.season_2015)