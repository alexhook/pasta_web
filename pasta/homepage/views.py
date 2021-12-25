from django.http.request import HttpRequest
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

def index(request: HttpRequest):
    return render(
        request,
        'index.html',
        context={}
    )
