from django.db import models
from EZRide.graphs.models import SubGraph
from django.contrib.auth.models import User

class UserRide(models.Model): 
    subgraph = models.OneToOneField(SubGraph, blank=True)
    users = models.ManyToManyField(User, blank=True)    
    def __unicode__(self):
        return self.subgraph.name
    
class RideDateTime(models.Model):
    ride = models.ForeignKey(UserRide)
    date_time = models.DateTimeField(unique=True)


    