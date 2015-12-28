#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple example for rendering a graph with the Django web framework.
See
http://www.djangoproject.com/
and
http://www.djangobook.com/en/beta/chapter11/

"""
#    Copyright (C) 2007 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Manos Renieris, http://www.cs.brown.edu/~er/
#    Distributed with BSD license.     
#    All rights reserved, see LICENSE for details.
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib import admin

from django.core.context_processors import csrf
from models import Graph, Node, Edge, SubGraph
from forms import SubGraphCreateForm, SubGraphDetailForm
from django.forms.models import modelformset_factory
from django.template.context import RequestContext

try:
    from django.http import HttpResponse
except ImportError: # this won't run without Django, print message 
    print "Django not found."
    
def persist_graph(request, graph_id):
    import pygraphviz as P
    import networkx as N
    
    graph = Graph.objects.get(pk=graph_id)
    dot_path = graph.dot_file.storage.location + '/' + graph.dot_file.name
    G = P.AGraph() # init empty graph
    try:
         
        G.read(dot_path) #read file      
        nodes = G.nodes()
        edges = G.edges() 
        Node.objects.filter(graph__id=graph_id).delete()
        Edge.objects.filter(graph__id=graph_id).delete()               
        for node in nodes:            
            new_node = Node()
            new_node.graph = graph
            new_node.name = node
            new_node.label = node.attr['label']
            new_node.save()
        for edge in edges:
            new_edge = Edge()
            new_edge.graph = graph
            new_edge.name = edge
            new_edge.save()
    except:
        return False
    return HttpResponse(pygraphviz_graph(request, G)) #response

def pygraphviz_graph(request, graph):
    import pygraphviz as P
    import networkx as N
  
    G = graph
    G.layout(prog='dot') #dot language
    img = G.draw(format='svg') # draw png    
    return HttpResponse(img, mimetype='image/svg+xml') #response



def shortest_path_rec(G, lista, i):
    import networkx as N
    L = N.Graph()
    J = N.Graph()  
      
    try:
        edgelist = N.shortest_path(G, source=lista[i],target=lista[(i+1)])
        L = G.subgraph(edgelist)
        J.add_edges_from(L.edges())
        edgelist = shortest_path_rec(G, lista, (i+1))
        L.add_edges_from(edgelist)
        J.add_edges_from(L.edges())
        J.node[lista[i]]= G.node[lista[i]]
        J.graph['color']='red'
        return J.edges()
    except (IndexError, RuntimeError):
        J.node[lista[i]]= G.node[lista[i]]
        J.graph['color']='red'
        return J.edges() 

def render_graph(request, graph_id, subgraph_id):
    import pygraphviz as P
    import networkx as N
    
    graph = Graph.objects.get(pk=graph_id)   
    dot_path = graph.dot_file.storage.location + '/' + graph.dot_file.name          
    G = P.AGraph() # init empty graph   
    try:
        G.read(dot_path) #read file                
        NG = N.Graph(G) #pyGraphViz to networkX; full graph
    except:
        pass
    if subgraph_id <> '0': #render subgraph svg      
        SG = N.Graph() #subgraph networkX 
        nodes = Node.objects.filter(subgraph__id=subgraph_id) #nodes in db
        for node in nodes:
            new_node = NG.node['name']=node.name
            SG.add_node(new_node)                      
        nodes = SG.nodes()
        edges = shortest_path_rec(NG, nodes,0)
        SG.add_edges_from(edges)        
        NSG = N.Graph()
        nodes = Node.objects.filter(graph__id=graph_id)
        for node in nodes:
            if SG.has_node(node.name):
                NSG.add_node(node.name, label=node.label, color='red')            
        NSG.add_edges_from(edges, color='red')
        
        
        NG = N.Graph(G)
        FG = N.compose(NSG, NG)
        FG.name = 'test'
        FG = N.to_agraph(FG)        
        #NEW_GRAPH = funcao de colorir(AGraph(), AGraph.edges()):retorna AGraph()        
        #SG = N.to_agraph(NSG)             
        #NG.graph.update(NSG.graph)
        #NG.name = 'test'
        #FG = N.to_agraph(NG)          
     
        FG.layout(prog='dot') #dot language
        graphView = FG.draw(format='svg') # draw svg
    else:
        G.layout(prog='dot') #dot language
        graphView = G.draw(format='svg') # draw svg       
    return HttpResponse(graphView, mimetype='image/svg+xml') #response

def subgraph_index(request, pk):
    subgraphs = SubGraph.objects.filter(graph__id=pk).exclude(user__id=request.user.id)
    graph_id = pk
    return render_to_response('graphs/subgraph_index.html', {'user': request.user, 'subgraphs': subgraphs, 'graph_id': graph_id }, mimetype='text/html')

def subgraph_create(request, pk):
    if request.method == 'POST': # If the form has been submitted...
        form = SubGraphCreateForm(pk, request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...                        
            subgraph = form.save(commit=False)
            subgraph.name = form.cleaned_data['name']            
            subgraph.graph = Graph.objects.get(pk=pk)
            subgraph.user = request.user
            subgraph.save()
            subgraph.nodes = form.cleaned_data['nodes']   
            subgraph.save()
            subgraph_id = subgraph.id    
            graph_id = subgraph.graph.id      
            return subgraph_detail(request, graph_id, subgraph_id)
        else:      
            return HttpResponseRedirect('/profiles/') # Redirect after POST
    else:
        form = SubGraphCreateForm(pk)   # An unbound form      
    return render_to_response('graphs/subgraph_create.html', {                                                     
        'user': request.user,
        'form': form,
        'graph_id': pk       
    }, context_instance=RequestContext(request))
    
def subgraph_edit(request, graph_id, subgraph_id):
    if request.method == 'POST': # If the form has been submitted...
        form = SubGraphDetailForm(request.POST, instance=SubGraph.objects.get(pk=subgraph_id)) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...                        
            subgraph = form.save(commit=False)
            subgraph.name = form.cleaned_data['name']            
            subgraph.graph = Graph.objects.get(pk=graph_id)
            subgraph.user = request.user
            subgraph.save()
            subgraph.nodes = form.cleaned_data['nodes']   
            subgraph.save()            
            return subgraph_detail(request, graph_id, subgraph_id)
        else:      
            return HttpResponseRedirect('/profiles/') # Redirect after POST
    else:
        form = SubGraphDetailForm(instance=SubGraph.objects.get(pk=subgraph_id))   # An unbound form      
    return render_to_response('graphs/subgraph_edit.html', {                                                     
        'user': request.user,
        'form': form,
        'graph_id': graph_id,
        'subgraph_id': subgraph_id       
    }, context_instance=RequestContext(request))
    
def subgraph_detail(request, graph_id, subgraph_id):
    subgraph = SubGraph.objects.get(pk=subgraph_id)        
    nodes = Node.objects.filter(subgraph__id=subgraph_id)  
    return render_to_response('graphs/subgraph_detail.html', {                                                     
        'user': request.user,
        'subgraph': subgraph,        
        'nodes': nodes       
    }, context_instance=RequestContext(request))
    
