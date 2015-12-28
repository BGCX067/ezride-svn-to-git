from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='/home/gabriel/DEV/Python/Eclipse_workspace/EZRide/EZRide/web-content/media/')
fu = 'uploads'

class Graph(models.Model):
    name = models.CharField(max_length=200)        
    dot_file = models.FileField(upload_to=fu, storage=fs)
    def __unicode__(self):
        return self.name
    
class Node(models.Model):
    name = models.CharField(max_length=200)    
    label = models.CharField(max_length=200)    
    graph = models.ForeignKey(Graph)    
    def __unicode__(self):
        return self.label
    
class Edge(models.Model):
    name = models.CharField(max_length=200)   
    graph = models.ForeignKey(Graph)
    def __unicode__(self):
        return self.name
    
class SubGraph(models.Model):    
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(User)
    graph = models.ForeignKey(Graph)
    nodes = models.ManyToManyField(Node, blank=True)
    edges = models.ManyToManyField(Edge, blank=True)
    def __unicode__(self):
        return self.name