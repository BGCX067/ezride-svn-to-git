from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, CreateView
from views import persist_graph, pygraphviz_graph, render_graph, subgraph_index, subgraph_create, subgraph_detail, subgraph_edit
from models import Graph, SubGraph
from EZRide.user_profiles.models import UserProfile
from EZRide.graphs.models import SubGraph
from forms import SubGraphCreateForm

urlpatterns = patterns('',
                       (r'^$',
                        ListView.as_view(
                                         queryset=Graph.objects.all(),
                                         context_object_name='graphs',
                                         template_name='graphs/index.html')),
                       url(r'^(?P<graph_id>\d+)/render/(?P<subgraph_id>\d+)/$', render_graph),
                       url(r'^(?P<pk>\d+)/$', subgraph_index),                            
                       (r'^(?P<pk>\d+)/create/$', subgraph_create),
                       (r'^(?P<graph_id>\d+)/edit/(?P<subgraph_id>\d+)/$', subgraph_edit),
                       (r'^(?P<graph_id>\d+)/detail/(?P<subgraph_id>\d+)/$', subgraph_detail)                                                                    
                       )