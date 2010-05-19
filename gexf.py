# -*- coding: utf-8 -*-

from lxml  import etree
from datetime import  *
 
 
 # missing features : 
 # load, validate, modify existing gexf file
 # slices / phylogeny / ...
 
 # evolution ideas :
 # add display stats on graph composition when exportingto xml
 # add anti-paralell edges test
 # add a test based on existing example from gexf.net
 # add modification accessors like setStart ...
 # factorize attribute managment by creating an attribute class
 # add a test code utility to check that code will not use _variable outside objects
 
class Gexf :

	def __init__(self,creator,description):
		self.creator=creator
		self.description=description
		self.graphs=[]
		self.xmlns="http://www.gephi.org/gexf/1.1draft"
		self.xsi="http://www.w3.org/2001/XMLSchema-instance"
		self.schemaLocation="http://www.gephi.org/gexf/1.1draft http://gephi.org/gexf/1.1draft.xsd"
		self.viz="http://www.gexf.net/1.1draft/viz"
		self.version="1.1"
	
	def addGraph(self,type,mode,label):
		g = Graph(type,mode,label)
		self.graphs.append(g)
		return g
 	
 	def getXML(self):
 		gexfXML = etree.Element("{"+self.xmlns+"}gexf",version=self.version,nsmap={None:self.xmlns,'viz':self.viz,'xsi':self.xsi})
# 		gexfXML.set("xmlnsxsi",)
 		gexfXML.set("{xsi}schemaLocation",self.schemaLocation)
		meta = etree.SubElement(gexfXML, "meta")
		meta.set("lastmodified",datetime.now().isoformat())
		etree.SubElement(meta, "creator").text=self.creator		
		etree.SubElement(meta, "description").text=self.description
		for graph in self.graphs :
			gexfXML.append(graph.getXML())
			
		return gexfXML
 		
 	def write(self,file):
 		file.write(etree.tostring(self.getXML(),pretty_print=True,encoding='utf-8'))
 		self.print_stat()
 	
 	def print_stat(self) :
 		for graph in self.graphs :
 			graph.print_stat()

 	
 
class Graph :

	
	
	
	def __init__(self,type,mode,label,start="",end="") :
		
		# control variable
		self.authorizedType=("directed","undirected")
		self.authorizedMode=("dynamic","static")
		self.defaultType="directed"
		self.defaultMode="static"
		self.label=label
		
		
		if type in self.authorizedType :
			self.type=type
		else :
			self.type=self.defaultType
		if mode in self.authorizedMode :
			self.mode=mode
		else :
			self.mode=self.defaultMode
		
	
		self.start=start
		
		self.end = end
		
		
		self._nodesAttributes={}
		self._edgesAttributes={}
		self._nodes={}
		self._edges={}
		
	def addNode(self,id,label,start="",end="",pid="") :
		self._nodes[id]=Node(self,id,label,start,end,pid)
		return self._nodes[id]
	
	def nodeExists(self,id) :
		if id in self._nodes.keys():
			return 1
		else :
			return 0
		
	def addEdge(self,id,source,target,weight="",start="",end="",label="") :
		self._edges[id]=Edge(self,id,source,target,weight,start,end,label)
		return self._edges[id]
	
	def addNodeAttribute(self,title,defaultValue,type="integer",mode="static") :
		# add to NodeAttributes
		# generate id
		id=len(self._nodesAttributes)
		self._nodesAttributes[id]={"title":title , "default":defaultValue, "mode":mode, "type":type}		# modify Nodes with default
		#: bad idea and unecessary
		#for node in self._nodes.values():
		#	node.addAttribute(id,defaultValue)

		return id
	
	def addDefaultAttributesToNode(self,node) :
		# add existing nodesattributes default values
		for id,values in self._nodesAttributes.iteritems() :
			node.addAttribute(id,values["default"])
			
	def checkNodeAttribute(self,id,value,start,end):
		# check conformity with type is missing
		if id in self._nodesAttributes.keys() :
			if self._nodesAttributes[id]["mode"]=="static" and ( not start=="" or not end=="") : 
				raise Exception("attribute "+str(id)+" is static you can't specify start or end dates. Declare Attribute as dynamic")
			return 1		
		else :
			raise Exception("attribute id unknown. Add Attribute to graph first")

		
	def addEdgeAttribute(self,title,defaultValue,type="integer",mode="static"):
		# add to NodeAttributes
		# generate id
		id=len(self._edgesAttributes)
		self._edgesAttributes[id]={"title":title, "default":defaultValue, "mode":mode, "type":type } 		# modify Nodes with default
		#for edge in self._edges.values():
		#	edge.addAttribute(id,defaultValue)
			
			
	def addDefaultAttributesToEdge(self,edge) :
		# add existing nodesattributes default values
		for id,values in self._edgesAttributes.iteritems() :
			edge.addAttribute(id,values["default"])
			
	def checkEdgeAttribute(self,id,value,start,end):
		# check conformity with type is missing
		if id in self._edgesAttributes.keys() :
			if self._edgesAttributes[id]["mode"]=="static" and ( not start=="" or not end=="") : 
				raise Exception("attribute "+str(id)+" is static you can't specify start or end dates. Declare Attribute as dynamic")
			return 1		
		else :
			raise Exception("attribute id unknown. Add Attribute to graph first")

	
	def getXML(self) :
		# return lxml etree element
		graphXML = etree.Element("graph",defaultedgetype=self.type,mode=self.mode,label=self.label)
		attributesXMLNodeDynamic = etree.SubElement(graphXML, "attributes")
		attributesXMLNodeDynamic.set("class","node")
		attributesXMLNodeDynamic.set("mode","dynamic")
		attributesXMLNodeStatic = etree.SubElement(graphXML, "attributes")
		attributesXMLNodeStatic.set("class","node")
		attributesXMLNodeStatic.set("mode","static")
		
		for id,value in self._nodesAttributes.iteritems() :
			if value["mode"]=="static" :
				attxml=attributesXMLNodeStatic
			else :
				attxml=attributesXMLNodeDynamic
			
			attributeXML=etree.SubElement(attxml, "attribute")
			attributeXML.set("id",str(id))
			attributeXML.set("title",value["title"])
			attributeXML.set("type",value["type"])
			etree.SubElement(attributeXML, "default").text=value["default"]
		
		attributesXMLEdgeDynamic = etree.SubElement(graphXML, "attributes")
		attributesXMLEdgeDynamic.set("class","edge")
		attributesXMLEdgeDynamic.set("mode","dynamic")
		attributesXMLEdgeStatic = etree.SubElement(graphXML, "attributes")
		attributesXMLEdgeStatic.set("class","edge")
		attributesXMLEdgeStatic.set("mode","static")
		
		for id,value in self._edgesAttributes.iteritems() :
			if value["mode"]=="static" :
				attxml=attributesXMLEdgeStatic
			else :
				attxml=attributesXMLEdgeDynamic
			
			attributeXML=etree.SubElement(attxml, "attribute")
			attributeXML.set("id",str(id))
			attributeXML.set("title",value["title"])
			attributeXML.set("type",value["type"])
			etree.SubElement(attributeXML, "default").text=value["default"]
		
		
		
		nodesXML = etree.SubElement(graphXML, "nodes")
		for node in self._nodes.values() :
			nodesXML.append(node.getXML())
			
		edgesXML = etree.SubElement(graphXML, "edges")
		for edge in self._edges.values() :
			edgesXML.append(edge.getXML())
			
		return graphXML
		
	def print_stat(self):
		print self.label+" "+self.type+" "+self.mode+" "+self.start+" "+self.end
 		print "number of nodes : "+str(len(self._nodes))
 		print "number of edges : "+str(len(self._edges))
		
		
class Node :

	def __init__(self,graph,id,label,start="",end="",pid="",r="",g="",b="") :
		self.id =id 
		self.label=label
		self.start=start
		self.end=end
		self.pid=pid
		self._graph=graph
		self.setColor(r,g,b)
		if not self.pid=="" :
			if not self._graph.nodeExists(self.pid) :
				raise Exception("pid "+self.pid+" node unknown, add nodes to graph first")

		self._attributes=[]
		
		# add existing nodesattributes default values : bad idea and unecessary
		#self._graph.addDefaultAttributesToNode(self)
		
	def addAttribute(self,id,value,start="",end="") :
		if self._graph.checkNodeAttribute(id,value,start,end) :
			self._attributes.append({"id":id,"value":value,"start":start,"end":end})
			
			
	def getXML(self) :
		# return lxml etree element
		try :
			nodeXML = etree.Element("node",id=self.id,label=str(self.label))
			if not self.start == "":
				nodeXML.set("start",self.start)
			if not self.end == "":
				nodeXML.set("end",self.end)
			if not self.pid == "":
				nodeXML.set("pid",self.pid)
			
			attributesXML = etree.SubElement(nodeXML, "attvalues")
			for atts in self._attributes :
				attributeXML=etree.SubElement(attributesXML, "attvalue")
				attributeXML.set("for",str(atts["id"]))
				
				attributeXML.set("value",atts["value"])
				
				if not atts["start"]=="" :
					attributeXML.set("start",atts["start"])
				if not atts["end"]=="" :
					attributeXML.set("end",atts["end"])
			
			if not self.r=="" and not self.g=="" and not self.b=="" :
				#color : <viz:color r="239" g="173" b="66"/>
				colorXML = etree.SubElement(nodeXML, "{http://www.gexf.net/1.1draft/viz}color")
				colorXML.set("r",self.r)
				colorXML.set("g",self.g)
				colorXML.set("b",self.b)
			
			return nodeXML
		except Exception as e:
			print self.label
			print self._attributes	
			print e
			exit()	
	
	def setColor(self,r,g,b) :
		self.r=r
		self.g=g
		self.b=b
	
class Edge :

	def __init__(self,graph,id,source,target,weight="",start="",end="",label="",r="",g="",b="") :
		self.id =id
		self._graph=graph
		
		
		if self._graph.nodeExists(source) :
			self._source=source
		else :
			raise Exception("source "+source+" node unknown, add nodes to graph first")
			
		if self._graph.nodeExists(target) :
			self._target=target
		else:
			raise Exception("target "+target+" node unknown, add nodes to graph first")	
					
		self.start=start
		self.end=end
		self.weight=weight
		self.label=label
		self._attributes=[]
		
		# add existing nodesattributes default values : bad idea and unecessary
		#self._graph.addDefaultAttributesToEdge(self)
		
		
	def addAttribute(self,id,value,start="",end="") :
		if self._graph.checkEdgeAttribute(id,value,start,end) :
			self._attributes.append({"id":id,"value":value,"start":start,"end":end})
		
	
	def getXML(self) :
		# return lxml etree element
		try :
			edgeXML = etree.Element("edge",id=str(self.id),source=str(self._source),target=str(self._target))
			if not self.start == "":
				edgeXML.set("start",self.start)
			if not self.end == "":
				edgeXML.set("end",self.end)
			if not self.weight == "":
				edgeXML.set("weight",str(self.weight))
			if not self.label == "":
				edgeXML.set("label",str(self.label))
				
			if not self.r=="" and not self.g=="" and not self.b=="" :
				#color : <viz:color r="239" g="173" b="66"/>
				colorXML = etree.SubElement(nodeXML, "{http://www.gexf.net/1.1draft/viz}color")
				colorXML.set("r",self.r)
				colorXML.set("g",self.g)
				colorXML.set("b",self.b)

			
			attributesXML = etree.SubElement(edgeXML, "attvalues")
			for atts in self._attributes :
				attributeXML=etree.SubElement(attributesXML, "attvalue")
				attributeXML.set("for",str(atts["id"]))
				attributeXML.set("value",atts["value"])
				if not atts["start"]=="" :
					attributeXML.set("start",atts["start"])
				if not atts["end"]=="" :
					attributeXML.set("end",atts["end"])
			return edgeXML
		except Exception as e:
			print self._source+" "+self._target	
			print e
			exit()	
			
	def setColor(self,r,g,b) :
		self.r=r
		self.g=g
		self.b=b
			