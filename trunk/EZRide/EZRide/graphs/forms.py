from django import forms
from django.forms import ModelForm, Form
from django.forms.models import modelformset_factory
from django.forms.models import BaseModelFormSet
from models import SubGraph, Graph, Node, Edge


attrs_dict = { 'class': 'required' }

class SubGraphCreateForm(forms.ModelForm):  
    def __init__(self, graph_id, *args, **kwargs):
        super(SubGraphCreateForm, self).__init__(*args, **kwargs)
        self.fields['nodes'] = forms.ModelMultipleChoiceField(queryset=Node.objects.filter(graph__id=graph_id).order_by('id'), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = SubGraph
        fields = ('name', 'nodes')
        
class SubGraphDetailForm(forms.ModelForm):
    class Meta:
        model = SubGraph
        fields = ('name', 'nodes')