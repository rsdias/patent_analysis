#!/usr/bin/env python
# coding: utf-8

# In[1]:


# calculate centrality of patent citation
# February 25th, 2020
# Networkx proved too slow
# Graph-tool is much faster
# The steps to calculate centrality in graph-tools are
# 1-create a graph
# 2-read data and convert into a list of edges and a list of vertices


# February 6th, 2020
# Type: Graph
# Number of nodes: 8527465
# Number of edges: 91336922
# Average degree:  21.4218


# In[2]:


import matplotlib
import graph_tool.all as gt
from random import randint
import csv
import gzip 

# import pandas as pd


# In[3]:



dst='data/centralit_noselfcit.csv'
src='data/uspatclean_joinselfcit.csv'
#src=gzip.open('data/patcitonly2.csv.gz','rt')
#src=zipsrc.open()

# src='data/sample.csv'


# In[4]:


g=gt.Graph()


# In[5]:


#get_ipython().magic(u'time')

with open(src, 'rt') as csvfile:
    
    list_of_edges = csv.reader(csvfile, delimiter=',')

    vertices = {}

    for e in list_of_edges:
        if e[0] not in vertices:
            vertices[e[0]] = True
        if e[1] not in vertices:
            vertices[e[1]] = True

    for d in vertices:
        vertices[d] = g.add_vertex()
#         g.add_vertex(vertices[d])

#    for edge in list_of_edges:
#        print(vertices[edge[0]], vertices[edge[1]])
#         g.add_edge(vertices[edge[0]], vertices[edge[1]])


# In[ ]:


#get_ipython().magic(u'time')
#with open(src, 'r') as csvfile:
    
#    list_of_edges = csv.reader(csvfile, delimiter=',')

#    for edge in list_of_edges:
#         print(vertices[edge[0]], vertices[edge[1]])
#        g.add_edge(vertices[edge[0]], vertices[edge[1]])


# In[ ]:


g.num_vertices()


# In[ ]:


g.num_edges()


# In[ ]:


# Initialize attribute
# eigen=g.new_vertex_property('float')


# In[ ]:


# Internalize attribute into the graph
# g.vertex_properties["eigen"]=eigen


# In[ ]:


#get_ipython().magic(u'time')
# Calculate centrality 
# max_eigenvalue, eigen = gt.graph_tool.centrality.eigenvector(g, vprop=g.vp.eigen)
# max_eigenvalue, eigen_matrix = gt.graph_tool.centrality.eigenvector(g, vprop=g.vp.eigen)


# In[ ]:


#get_ipython().magic(u'time')
pagerank=g.new_vertex_property('float')
g.vertex_properties["pagerank"]=pagerank
pagerank=gt.graph_tool.centrality.pagerank(g, prop=g.vp.pagerank)


# In[ ]:


#get_ipython().magic(u'time')
#katz=g.new_vertex_property('float')
#g.vertex_properties["katz"]=katz
#katz=gt.graph_tool.centrality.katz(g, vprop=g.vp.katz)


# In[ ]:


# %time
#betweenness=g.new_vertex_property('float')
#g.vertex_properties["betweenness"]=betweenness
#betweenness=gt.graph_tool.centrality.betweenness(g, vprop=g.vp.betweenness)


# In[ ]:


# g.vertex_properties["eigen"]=eigenvector_property_map


# In[ ]:


# g.get_vertices(vprops='eigen')


# In[ ]:


#get_ipython().magic(u'time')
with open(dst, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, lineterminator='\n')
    data=zip(vertices.keys(), g.vp.pagerank)
    wr.writerow(['id', 'pagerank'])
    for vertice in data:
        wr.writerow(vertice)


# In[ ]:


#g.list_properties()



# In[ ]:


# for i in range(0,len(vertices), 10000):
#     print(eigenvector_property_map[i])


# In[ ]:


# for i in range(0,len(vertices), 10):
#     print(g.get_vertices())


# In[ ]:


# g.vertex_properties['eigen']


# In[ ]:


# with open("data/centrality.csv", "a") as myfile:

#     for i in range(1,len(vertices)):
        
#         output=[]
#         output.append([i, eigenvector_property_map[i]]) 
#         myfile.write(str(output[0]))


# In[ ]:


# output[0]

