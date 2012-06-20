#!/usr/bin/python

import sys,pprint

sys.path.append('../gexf')
from _gexf import Gexf, GexfImport

# test helloworld.gexf
gexf = Gexf("Paul Girard","A hello world! file")
graph=gexf.addGraph("directed","static","a hello world graph")

graph.addNode("0","hello")
graph.addNode("1","World")
graph.addEdge("0","0","1")

output_file=open("helloworld.gexf","w")
gexf.write(output_file)

# test GexfImport
f = open("gexf.net.dynamics_openintervals.gexf")
gexf_import = Gexf.importXML(f)
f.close()
f = open("gexf.net.dynamics_openintervals.gexf")
gexf_import2 = Gexf.importXML(f)
f.close()
print "test gexf comparision "+str(gexf_import==gexf_import2)



graph=gexf_import.graphs[0]
# display nodes list 
for node_id,node in graph.nodes.iteritems() : 
    print node.label
    pprint.pprint(node.getAttributes(),indent=1,width=1)

# display edges list 
for edgeid,edge in graph.edges.iteritems() : 
    print str(graph.nodes[edge.source])+" -> "+str(graph.nodes[edge.target])
    pprint.pprint(edge.getAttributes(),indent=1,width=1)


o = open("gexf.net.dynamics_openintervals_copied.gexf", "w")

gexf_import.write(o)
