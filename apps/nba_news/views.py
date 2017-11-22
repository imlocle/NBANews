# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'nba_news/index.html')

def registration(request):
    