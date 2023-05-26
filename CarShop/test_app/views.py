from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Test hello world!!!")

# Create your views here.
