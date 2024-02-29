import sys #provides access to the sys module, helping with accesing to a few functions

from Graph import Graph
from Driver import Driver
from Order import Order


def dijkstras_algorithm(graph, start_node): # function for the implementation of dijkstra's algorithm
    unvisited_nodes = list(graph.get_nodes()) # this will initialize a list with unvisited nodes with all the nodes in the graph
    #this initializes the dictionary called distances and each node in unvisited nodes is set to the maximum possible distance
    distances = {node: sys.maxsize for node in unvisited_nodes}
    distances[start_node] = 0


    previous_nodes = {node: None for node in unvisited_nodes} # this sets previous nodes to none for each node

    # a while loop that runs until the nodes are all visited
    while unvisited_nodes:
        current_smallest_node = None
        for node in unvisited_nodes:
            if current_smallest_node is None or distances[node] < distances[current_smallest_node]:
                current_smallest_node = node
        # gets the neighbours of a node
        neighbours = graph.get_outgoing_edges(current_smallest_node)
        # this for loop updates the distances and the previous nodes for the neighbours
        for neighbour in neighbours:
            new_distance = distances[current_smallest_node] + graph.value(current_smallest_node, neighbour)
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous_nodes[neighbour] = current_smallest_node

        unvisited_nodes.remove(current_smallest_node) #this removes a node that has been visited from the unvisited list

    return previous_nodes, distances



def return_the_closest_driver(drivers, user_location, graph): #function to find the closest driver to the user
    #variables to find the closest driver
    closest_driver = None 
    smallest_distance_to_user = sys.maxsize

    for driver in drivers: # this is a for loop that iterates through every driver in drivers list 
        present_location = driver.present_location.strip() 

        # this calculates the distance from the driver to Coventry City Centre using dijkstra's algorithm
        _, distance_to_coventry = dijkstras_algorithm(graph=graph, start_node=present_location)
        distance_to_coventry = distance_to_coventry["Coventry City Centre"]

        # this is calculating the distance from the driver to the user's location based on the user input using dijkstra's algorihm
        _, distance_to_user = dijkstras_algorithm(graph=graph, start_node=present_location)
        distance_to_user = distance_to_user[user_location]

        total_distance = distance_to_coventry + distance_to_user #calculates the total distance between the driver's distance to coventry city centre and the driver's distance to the user's location 

        if total_distance < smallest_distance_to_user: # this checks if the current driver has a smaller distance to the user's location
            smallest_distance_to_user = total_distance #this updates the minimum distance
            closest_driver = driver # this updates the closest driver

    return closest_driver

nodes = ["Coventry City Centre", "Canley", "Great Heath", "Bedworth", "Bell Green", "Binley", "Finham", "Whitley", "Spon End", "Tile Hill"] #nodes for the graph

init_graph = {}
for node in nodes:
    init_graph[node] = {}

init_graph["Coventry City Centre"]["Canley"] = 3
init_graph["Coventry City Centre"]["Bedworth"] = 6
init_graph["Coventry City Centre"]["Bell Green"] = 3
init_graph["Canley"]["Great Heath"] = 1
init_graph["Canley"]["Tile Hill"] = 2
init_graph["Canley"]["Spon End"] = 6
init_graph["Great Heath"]["Tile Hill"] = 3
init_graph["Tile Hill"]["Whitley"] = 7
init_graph["Spon End"]["Whitley"] = 8
init_graph["Whitley"]["Binley"] = 4
init_graph["Whitley"]["Finham"] = 3
init_graph["Finham"]["Binley"] = 3
init_graph["Binley"]["Bell Green"] = 8 # graph creation

drivers = [
    Driver(name="Adam", present_location="Spon End"),
    Driver(name="Adrian", present_location="Binley"),
    Driver(name="Raul", present_location="Tile Hill"),
    Driver(name="Armand", present_location="Great Heath")
] # drivers list

graph = Graph(nodes, init_graph) # this is using the Graph class to create a graph instance.

def order_menu(): # order menu
    print("Welcome to the Razvan's App for Food Delivery!") #print statement that lets the user know how the app is called.

    user_location = input("Where do you live? ") #takes input for the user's location
    user_location = user_location.title() #helps with smaller case inputs and converts them to Uppercase so that the code can work
    order_for_user = input("What would you like to order? ") # takes input for order for the user

    order = Order(destination=user_location, order=order_for_user)

    closest_driver = return_the_closest_driver(drivers, order.destination, graph)

    # this uses dijkstras algorithm to find the route to Coventry City Centre
    previous_nodes_coventry, _ = dijkstras_algorithm(graph=graph, start_node=closest_driver.present_location)
    route_nodes_coventry = []
    current_node_coventry = "Coventry City Centre"
    while current_node_coventry is not None:
        route_nodes_coventry.append(current_node_coventry)
        current_node_coventry = previous_nodes_coventry[current_node_coventry]

    route_nodes_coventry.reverse() #reverses the route list to get the correft order

    # similar to the one above, this uses dijkstras algorithm this time to find the route to the user's location
    previous_nodes_user, _ = dijkstras_algorithm(graph=graph, start_node="Coventry City Centre")
    route_nodes_user = []
    current_node_user = order.destination
    while current_node_user is not None:
        route_nodes_user.append(current_node_user)
        current_node_user = previous_nodes_user[current_node_user]

    route_nodes_user.reverse()

    # this combines both routes to get the full route that the driver is going to make.
    full_route = route_nodes_coventry + route_nodes_user[1:]  # Exclude the starting node (Coventry City Centre)
    
    #print statement that confirms the order, the driver, the location of the user and the route.
    print(f"Thanks for the order! {closest_driver.name} is on the way to deliver {order.order} to {user_location}.")
    print(f"Route: {' -> '.join(full_route)}")

if __name__ == "__main__":
    order_menu()
