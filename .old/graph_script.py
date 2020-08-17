import matplotlib
import graph_tool.all as gt
from random import randint
import csv

src='data/patcitonly.csv'
g=gt.Graph()

with open(src, 'r') as csvfile:
    
    list_of_edges = csv.reader(csvfile, delimiter=',')

    vertices = {}

    for e in list_of_edges:
        if e[0] not in vertices:
            vertices[e[0]] = True
        if e[1] not in vertices:
            vertices[e[1]] = True

    for d in vertices:
        vertices[d] = g.add_vertex()

    for edge in list_of_edges:
        print(vertices[edge[0]], vertices[edge[1]])

with open(src, 'r') as csvfile:
    
    list_of_edges = csv.reader(csvfile, delimiter=',')

    for edge in list_of_edges:
        g.add_edge(vertices[edge[0]], vertices[edge[1]])

eigen=g.new_vertex_property('float')
g.vertex_properties["eigen"]=eigen
max_eigenvalue, eigenvector_property_map = gt.graph_tool.centrality.eigenvector(g, vprop=g.vp.eigen)

pagerank=g.new_vertex_property('float')
g.vertex_properties["pagerank"]=pagerank
pagerank=gt.graph_tool.centrality.pagerank(g)

with open('data/eigen.csv', 'w') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(zip(vertices.keys(), g.vp.eigen, g.vp.pagerank))
g.num_edges()