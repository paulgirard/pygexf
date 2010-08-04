#!/usr/bin/python

from gexf import Gexf,GexfImport

# test helloworld.gexf
gexf = Gexf("Paul Girard","A hello world! file")
graph=gexf.addGraph("directed","static","a hello world graph")

graph.addNode("0","hello")
graph.addNode("1","World")
graph.addEdge("0","0","1")

output_file=open("hellowrld.gexf","w")
gexf.write(output_file)

# test GexfImport
f = open("exp.gexf")
o = open("exp_bootstrap_bootstrap.gexf", "w+")

gexf_import = GexfImport(f).gexf()
gexf_import.write(o)
