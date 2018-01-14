from __future__ import unicode_literals
import json
import bcrypt
import requests
import re
import ssl
import urllib2
import HTMLParser
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Comment, Article

realgm_url='https://basketball.realgm.com/rss/wiretap/0/0.xml'
the_players_tribune_url='https://www.theplayerstribune.com/sports/basketball/'
espn_rss__nba_url='http://www.espn.com/espn/rss/nba/news'
news_apikey='46bd8a2eb02c485ba51cea891e1f0b1b'
espnurl='https://newsapi.org/v2/top-headlines?sources=espn&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
bleacherreporturl='https://newsapi.org/v2/everything?sources=bleacher-report&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
foxsportsurl='https://newsapi.org/v2/everything?sources=fox-sports&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
nba_player_stats='http://data.nba.net/10s/prod/v1/2016/players.json'

#keywords for filtering basketball related articles for newsapi
keywords={'Basketball', 'basketball', 'NBA', 'Kobe Bryant' 'Curry', 'double-double', 'LeBron', 'LaVar'}


#parser.unescape
parser = HTMLParser.HTMLParser()
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
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwhashed)
        request.session["current_user"] = user.id
        return redirect("/nba_news")
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect("/")

def create_comment(request):
    check = Comment.objects.create_comment(request.POST['create_comment'])
    if check:
        Comment.objects.create_comment(create_comment=request.POST['create_comment'])
        return redirect('/')
    else:
        for i in range(0, len(check)):
            messages.warning(request, check[i])
        return redirect('/')

def nba_news(request):
    current_user = User.objects.get(id=request.session['current_user'])
    the_players_tribune(the_players_tribune_url)
    realgm(realgm_url)
    espn_rss_nba(espn_rss__nba_url)
    newsapi(espnurl)
    newsapi(bleacherreporturl)
    newsapi(foxsportsurl)
    newsfeed = []
    for i in Article.objects.raw("SELECT * FROM nba_news_article order by created_at DESC"):       
        newsfeed.append(i)         
    context = {
                'current_user': current_user,
                'newsfeed': newsfeed,
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
            author_url = 'null'
            source = converttojson[i]['source']['name']
            title = converttojson[i]['title']
            published_on = converttojson[i]['publishedAt']
            Article.objects.new_article(url, url_image, author, author_url, source, description, title, published_on)
        else:
            continue
        i+=1

def the_players_tribune(url):
    tribune_call = requests.get(url).text
    tribune_call = parser.unescape(tribune_call)
    match_collection = re.findall(r'<div class=\"article-snippet\">.+?/h3><p>.+?</p>', tribune_call)
    for i in match_collection:
        url = parse_definition("<div class=\"article-snippet\">\\s*<a href=\"([^\"]+)\">", i)
        url_image = parse_definition("<div class=\"cover\">\\s*<img src=\"(https.+?(jpg|gif))\"", i)
        author = parse_definition("<div\\s*class=\"byline dark\"><span><a href=\".+?\">(.+?)<", i)
        author_url = parse_definition("<div\\s*class=\"byline dark\"><span><a href=\"(https.+?author[^\"]+)\">", i)
        source = "The Players' Tribune"
        description = parse_definition("<p>(.+?)</p>", i)
        title = parse_definition("<h3\\s*class=\"entry-title\">\\s*<a href=\".+?\">(.+?)</a>", i)
        published_on = "null"
        if re.compile(r'.+?Empire.+?Season.+?Episodes.+?').match(title):
            continue
        Article.objects.new_article(url, url_image, author, author_url, source, description, title, published_on)

def espn_rss_nba(url):
    espn_call = requests.get(url).text
    match_collection = re.findall(r'<item>.+?</item>', espn_call)
    for i in match_collection:
        url = parse_definition("<link><!\[CDATA\[(.+?)\]", i)
        url_image = "null"
        author = "null"
        author_url = 'null'
        source = "ESPN"
        description = parse_definition("<description><!\[CDATA\[(.+?)\]", i)
        title = parse_definition("<title><!\[CDATA\[(.+?)\]", i)
        published_on = parse_definition("<pubDate>(.+?)</pubDate>", i)
        Article.objects.new_article(url, url_image, author, author_url, source, description, title, published_on)

def realgm(url):
    realgm_call = requests.get(url).text
    realgm_call = parser.unescape(realgm_call)
    match_collection = re.findall(r'<item>.+?</item>', realgm_call, flags=re.MULTILINE|re.DOTALL)
    for i in match_collection:
        url = parse_definition("<link>(.+?)</link>", i)
        url_image = "null"
        description = parse_definition("<description>(.+?)</description", i).replace('<p>', '').replace('</p>', '').replace('<span>', '').replace('</span>', '')
        author = "null"
        author_url = 'null'
        source = "RealGM"
        title = parse_definition("<title>(.+?)<", i)
        published_on = parse_definition("<pubDate>(.+?)</pubDate>", i)
        #published_on = datetime.strptime(published_on, '%a, %d %b %Y %H:%M:%S %Z')
        if re.compile(r'.+?Duncd-On.+?').match(url):
            continue
        if re.compile(r'Get all the latest news.+?').match(description):
            continue
        Article.objects.new_article(url, url_image, author, author_url, source, description, title, published_on)

def parse_definition(regex_pattern, string):
    i = re.compile(regex_pattern, flags=re.MULTILINE|re.DOTALL)
    return i.search(string).group(1)