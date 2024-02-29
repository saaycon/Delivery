class Graph(object): # class for the creation of the Graph
    def __init__(self, nodes, init_graph): #constructor of the graph
        self.nodes = nodes
        self.graph = self.construct_the_graph(nodes, init_graph)

    def construct_the_graph(self, nodes, init_graph): #creates the graph
        graph = {} #empty dictionary used to represent the graph
        for node in nodes: # For loop that loops through each node in the list and creates a dicitonary to store the node's neighbours and the values of the edges(distances)
            graph[node] = {}

        graph.update(init_graph) #Updates the graph with the initial graph that is provided

        for node, edges in graph.items(): #for loop that loops through the nodes and edges inside the graph
            for adjacent_node, value in edges.items(): # loops throught the edges and each of the edge's values
                if graph[adjacent_node].get(node, False) == False: # if the reverse edge is not present, this adds it to the graph with the same value
                    graph[adjacent_node][node] = value

        return graph #returns the constructed graph

    def get_nodes(self): #this returns the nodes from the graph
        return self.nodes

    def get_outgoing_edges(self, node): # this function gets the neighbours of a node
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        return connections

    def value(self, node1, node2): # this function returns the value between two nodes
        return self.graph[node1][node2]
