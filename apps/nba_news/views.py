from __future__ import unicode_literals
import json
import bcrypt
import requests
import re
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Comment, Article

espn_rss__nba_url='http://www.espn.com/espn/rss/nba/news'
news_apikey='46bd8a2eb02c485ba51cea891e1f0b1b'
espnurl='https://newsapi.org/v2/top-headlines?sources=espn&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
bleacherreporturl='https://newsapi.org/v2/everything?sources=bleacher-report&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
foxsportsurl='https://newsapi.org/v2/everything?sources=fox-sports&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
nbaPlayerStats='http://data.nba.net/10s/prod/v1/2016/players.json'

keywords={'Basketball', 'basketball', 'NBA', 'Kobe' 'Curry', 'Jordan', 'LeBron', 'LaVar'}

maxtries=1000

def index(request):
    return render (request, 'nba_news/index.html')

def login(request):
    email = request.POST["email"]
    password = request.POST["password"]
    check = User.objects.login(email, password)
    if check == True:
        user = User.objects.get(email = email)
        request.session["current_user"] = user.id
        return redirect('/nba_news')
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
        return redirect("/nba_news")
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

def nba_news(request):
    current_user = User.objects.get(id = request.session['current_user'])
    espn_rss_nba(espn_rss__nba_url)
    count = 0
    newsapi(espnurl)
    newsapi(bleacherreporturl)
    newsapi(foxsportsurl)
    espn = []
    bleacher = []
    foxsports =[]
    for i in Article.objects.raw("SELECT * FROM nba_news_article order by created_at DESC"):
        if i.source == 'Bleacher Report':
            bleacher.append(i)
        if i.source == 'ESPN':
            espn.append(i)
        if i.source == 'Fox Sports':
            foxsports.append(i)
    context = {
                'current_user': current_user,
                'espn': espn,
                'bleacher':bleacher,
                'foxsports': foxsports
                }

    return render(request, 'nba_news/nbanews.html', context)


# newapi.org only allows 1000 hits a day.
def newsapi(url):
    getapi = requests.get(url).text
    converttojson = json.loads(getapi)['articles']
    for i in range(len(converttojson)):
        description = converttojson[i]['description']
        if any(x in description for x in keywords):
            url = converttojson[i]['url']
            url_image = converttojson[i]['urlToImage']
            author = converttojson[i]['author']
            source = converttojson[i]['source']['name']
            title = converttojson[i]['title']
            published_on = converttojson[i]['publishedAt']
            Article.objects.new_article(url, url_image, author, source, description, title, published_on)
        i+=1

def espn_rss_nba(url):
        espn_call = requests.get(url).text
        match_collection = re.findall(r'<item>.+?</item>', espn_call)
        for i in match_collection:
            url = parse_definition("<link><!\[CDATA\[(.+?)\]", i)
            url_image = "null"
            author = "null"
            source = "ESPN"
            description = parse_definition("<description><!\[CDATA\[(.+?)\]", i)
            title = parse_definition("<title><!\[CDATA\[(.+?)\]", i)
            published_on = parse_definition("<pubDate>(.+?)</pubDate>", i)
            Article.objects.new_article(url, url_image, author, source, description, title, published_on)

def parse_definition(regex_pattern, string):
    i = re.compile(regex_pattern)
    return i.search(string).group(1)


