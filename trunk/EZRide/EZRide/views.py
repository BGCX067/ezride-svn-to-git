# Developed by Intento Web
from django.shortcuts import render_to_response

def home(request): 
        return render_to_response('site/home.html', {'user' : request.user,})