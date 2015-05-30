from unittest import TestCase

import os
from filecmp import cmp

from gexf import Gexf


class TestGexf(TestCase):

    @staticmethod
    def filepath(path):
        return os.path.join(os.path.dirname(__file__), path)
    
    def test_create_export_and_import(self):
        """Create a graph with gexf export and then check that
        what we import with gexf looks correct"""
        # create a graph
        AUTHOR = "Dok Uduv"
        DESCRIPTION = "A hello world! file"

        TYPE = 'directed'
        MODE = 'static'
        LABEL = "a hello world graph, with two nodes and one edge."

        gexf = Gexf(AUTHOR, DESCRIPTION)
        graph = gexf.addGraph(
            TYPE,
            MODE,
            LABEL
        )
        graph.addNode("0", "node ONE")
        graph.addNode("1", "node TWO")
        graph.addEdge("0", "0", "1")

        # save it
        filepath = self.filepath("helloworld.gexf")
        with open(filepath, "w") as f:
            gexf.write(f)

        # import the graph with gexf
        with open(filepath) as f:
            gexp = Gexf.importXML(f)

        self.assertEqual(gexp.creator, AUTHOR)
        self.assertEqual(gexp.description, DESCRIPTION)
        self.assertEqual(len(gexp.graphs), 1)
        graph = gexp.graphs[0]
        self.assertEqual(graph.type, TYPE)
        self.assertEqual(graph.mode, MODE)
        self.assertEqual(graph.label, LABEL)
        self.assertEqual(len(graph.nodes.keys()), 2)
        self.assertEqual(len(graph.edges.keys()), 1)
        os.remove(filepath)

    def test_import_export_of_external_file(self):
        original = self.filepath("./gexf.net.dynamics_openintervals.gexf")
        with open(original) as f:
            gexf = Gexf.importXML(f)

        export = self.filepath("./gexf.net.dynamics_openintervals-export.gexf")
        with open(export, "w") as f:
            gexf.write(f)

        self.assertTrue(cmp(
            original,
            export,
            shallow=False
        ))
        os.remove(export)
