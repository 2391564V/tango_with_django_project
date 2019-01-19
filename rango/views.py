from django.shortcuts import render
from django.http import HttpResponse

# Define different views to send a reponse to
def index(request):
    return HttpResponse("Rango says hey there partner!")

def about(request):
    return HttpResponse("This is the about page!")
