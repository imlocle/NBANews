from __future__ import unicode_literals
# from splinter import Browser
from bs4 import BeautifulSoup as soup
# import json
import requests
import re
# import ssl
# import urllib2
# import HTMLParser
# from datetime import datetime
# from .models import Article, Comment
# import views

#browser = Browser("chrome", headless=True)

espn_rss__nba_url='http://www.espn.com/espn/rss/nba/news'
espn_newsapi_url='https://newsapi.org/v2/top-headlines?sources=espn&apiKey=46bd8a2eb02c485ba51cea891e1f0b1b'
espn_nba_url="http://www.espn.com/nba/"

# def espn_rss_nba(url):
#     espn_call = requests.get(url).text
#     match_collection = re.findall(r'<item>.+?</item>', espn_call)
#     for i in match_collection:
#         url = parse_definition("<link><!\[CDATA\[(.+?)\]", i)
#         url_image = "null"
#         author = "null"
#         author_url = 'null'
#         source = "ESPN"
#         description = parse_definition("<description><!\[CDATA\[(.+?)\]", i)
#         title = parse_definition("<title><!\[CDATA\[(.+?)\]", i)
#         published_on = parse_definition("<pubDate>(.+?)</pubDate>", i)
#         Article.objects.new_article(url, url_image, author, author_url, source, description, title, published_on)

def espn_nba(espn_nba_url):
    espn_html = soup(requests.get(espn_nba_url).text, 'html.parser')
    espn_html.find_all("div", "contentItem__contentWrapper")

