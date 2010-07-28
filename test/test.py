#!/usr/bin/python

import gexf

f = open("exp.gexf")
o = open("exp_bootstrap_bootstrap.gexf", "w+")

gexf_import = gexf.GexfImport(f).gexf()
gexf_import.write(o)
