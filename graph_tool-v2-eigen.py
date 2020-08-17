"""
DO NOT USE - ONLY FOR DOCUMENTATION

# Script to calculate centrality of patent citation
# August 17th, 2020
This script was created to test the script graph_tool-v2.py with a different network centrality measure (eigen)
However, before I effectively ran the tests, I verified that the error in the original script was the missing edge creation (in this script there is no correction to that issue, so it would not work).


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
"""


import matplotlib
import graph_tool.all as gt
from random import randint
import csv


#src='data/uspatclean_selfcit.csv'
#dst='data/centralit_noselfcit.csv'

src='data/patcitonly2.csv'
dst='data/centrality_eigen.csv'



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

print "Numero de vertices " + str(g.num_vertices()) + "\n"
print "Numero de edges " + str(g.num_edges()) + "\n"

        
eigen=g.new_vertex_property('float')
g.vertex_properties["eigen"]=eigen
max_eigenvalue, eigen_matrix = gt.graph_tool.centrality.eigenvector(g, vprop=g.vp.eigen)


with open(dst, 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, lineterminator='\n')
    data=zip(vertices.keys(), g.vp.eigen)
    wr.writerow(['id', 'eigen'])
    for vertice in data:
        wr.writerow(vertice)




