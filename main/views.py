from django.shortcuts import render

# Create your views here.

def index(response):
    return render(response, "main/index.html")

def login(response):
    return render(response, "main/login.html")


