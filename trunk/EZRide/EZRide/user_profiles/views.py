# Developed by Intento Web
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib import admin

from django.core.context_processors import csrf
from models import UserProfile, User
from forms import UserProfileEditForm
from EZRide.graphs.models import SubGraph
from django.forms.models import modelformset_factory
from django.template.context import RequestContext

def profile_index(request):
    subgraphs = SubGraph.objects.filter(user__id=request.user.id)
    return render_to_response('profiles/profile_index.html', {'user': request.user, 'subgraphs': subgraphs}, mimetype='text/html')