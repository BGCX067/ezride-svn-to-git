from models import Graph
from django import forms
from django.db.models import get_model
from django.contrib import admin
from models import Graph, Node, Edge
from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from EZRide.graphs.views import persist_graph
from django.core.context_processors import request

class GraphAdminForm(forms.ModelForm):
    # Step 1: Add the extra form fields to the ModelForm
    class Meta:
        model = Graph
 
    # Step 2: Override the constructor to manually set the form's latitude and
    # longitude fields if a Graph instance is passed into the form
    def __init__(self, *args, **kwargs):
        super(GraphAdminForm, self).__init__(*args, **kwargs)
 
        # Set the form fields based on the model object
        if kwargs.has_key('name'):
            instance = kwargs['name']
            self.initial['name'] = instance.name
            self.initial['dot_file'] = instance.dot_file
 
    # Step 3: Override the save method to manually set the model's latitude and
    # longitude properties based on what was submitted from the form
    def save(self, commit=True):
        model = super(GraphAdminForm, self).save(commit=False)
 
        # Save the latitude and longitude based on the form fields
        model.name = self.cleaned_data['name']
        model.dot_file = self.cleaned_data['dot_file']
 
        if commit:
            model.save()    
                        
        return model
        #persist_graph(self, model.pk)
             
        
 
# Custom admin definition
# I'm using admin.GeoModelAdmin because I'm using GeoDjango. Usually
# you would be subclassing admin.ModelAdmin.
class GraphAdmin(admin.ModelAdmin):
    form = GraphAdminForm

    def change_view(self, request, object_id, extra_context=None):
        result = super(GraphAdmin, self).change_view(request, object_id, extra_context)
        graph = Graph.objects.get(id__exact=object_id)
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
            #result['Location'] = graph
            return persist_graph(request, object_id)
        
     
# Register admin
admin.site.register(Graph, GraphAdmin)
