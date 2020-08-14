# Script to calculate centrality of patent citation
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



import matplotlib
import graph_tool.all as gt
from random import randint
import csv


dst='data/centralit_noselfcit.csv'
src='data/uspatclean_joinselfcit.csv'



g=gt.Graph()



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

        
pagerank=g.new_vertex_property('float')
g.vertex_properties["pagerank"]=pagerank
pagerank=gt.graph_tool.centrality.pagerank(g, prop=g.vp.pagerank)


with open(dst, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, lineterminator='\n')
    data=zip(vertices.keys(), g.vp.pagerank)
    wr.writerow(['id', 'pagerank'])
    for vertice in data:
        wr.writerow(vertice)




