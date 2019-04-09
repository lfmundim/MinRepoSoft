import networkx as nx

class GraphLib:
	def __init__(self):
		self.graph = nx.Graph()

	def addEdge(self, fileA, fileB):
		try:
			edge = self.graph[fileA][fileB]
			newEdgeWeight = edge['weight'] + 1
			self.graph.add_edge(fileA, fileB, weight=newEdgeWeight)
		except KeyError as e:
			self.graph.add_edge(fileA, fileB, weight=1)
		
	def testFunc(self):
		self.addEdge('B', 'D')
		self.addEdge('B', 'D')
		self.addEdge('A', 'C')
		self.addEdge('C', 'D')
		self.addEdge('A', 'B')
		self.addEdge('C', 'B')
		print(self.getHeaviestEdge())
		print(self.getMostRelatedNode())

	def getHeaviestEdge(self):
		maxWeight = 0

		for edge in self.graph.edges:
			actualEdge = self.graph[edge[0]][edge[1]]
			if(actualEdge['weight'] > maxWeight):
				heaviestEdge = edge[0],edge[1]
				maxWeight = actualEdge['weight']
		return heaviestEdge, maxWeight

	def getMostRelatedNode(self):
		maxRelated = 0

		for node in self.graph.nodes:
			neighborCount = sum(1 for neighbor in nx.neighbors(self.graph, node))
			if(neighborCount > maxRelated):
				maxRelated = neighborCount
				mostRelatedNode = node
		return mostRelatedNode, maxRelated
