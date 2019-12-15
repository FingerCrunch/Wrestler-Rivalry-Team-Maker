# Tite: Wresteler Rivalries Team Maker
# Author: Eric Riemer
# Last Modified: 11/10/2019
# OSU email address: riemere@oregonstate.edu
# Course number/section: CS325 - 400
# Assignment Number: 5                Due Date: 11/11/2019
# Description: This program creates a graph (represented by an adjacency list) where each vertex represents a wrestler and each edge represents a rivalry.
#It then performs Breadth First Search to determine the distance of each vertex from the first wrestler given. 
#The wrestlers will be assigned teams based on distance from the starting vertex. If the distance from #the starting distance is even, then that vertex is on the same team as the starting #vertex (Babyfaces); whereas, if that vertex is odd, then that vertex is on the opposing team (Heels).

#Reference: https://github.com/joeyajames/Python/blob/master/graph_adjacency-list.py)
    #The implementation of the Vertex Class (Functions: init and add_neighbor) and Graph Class (Functions: add_vertex, add_edge)
#Implementation of an undirected graph using Adjacency Lists
#The Vertex class initializes a vertex when given a name
#Each vertex holds the following variables: 
#its name, a list of its neighbors, color, distance from starting vertex, and parent node
import queue

class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()
        self.color = "WHITE"
        self.distance = 0
        self.parent = self
    #this function adds a new vertex (v) to the neighbors list if it isn't already in it
    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            
class Graph:
    vertices = {}
    babyfaces = {}
    heels = {}

    #Reference: https://github.com/joeyajames/Python/blob/master/graph_adjacency-list.py)
    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    #Reference: https://github.com/joeyajames/Python/blob/master/graph_adjacency-list.py)
    def add_edge(self, u, v):
        if u in self.vertices and v in self.vertices:
            self.vertices[u].add_neighbor(v)
            self.vertices[v].add_neighbor(u)
            return True
        else:
            return False
    #This function checks if the problem is possible, then prints "Impossible" if it isn't.
    #If it is possible, it prints the members of each team.
    def print_teams(self):
        if self.check_impossible() == True:
            print("Impossible")
        else:
            print("Yes, Possible!")
            print("Babyfaces: ", end="")
            for key in self.babyfaces:
                print(key, end=" ")
            print("\n")
            print("Heels: ", end="")
            for key in self.heels:
                print(key, end=" ")
            print("\n")
    
    #This function returns true if the set is impossible and false if it is not impossible.
    #Checks each edge to verify that it doesn't share edges with member of same team.
    #If 2 members of the same team share an edge, the poblem is impossible.
    #Time-Complexity: O(VE), where V is number of vertices and E is number of edges
    def check_impossible(self):
        for babyface in self.babyfaces:
            for neighbor in self.vertices[babyface].neighbors:
                if neighbor in self.babyfaces:
                    return True
        for heel in self.heels:
            for neighbor in self.vertices[heel].neighbors:
                if neighbor in self.heels:
                    return True
        return False

    #This function runs breadth first search (BFS) on a graph. It accepts a starting node as an
    #argument and updates the distance of all other nodes to be the distance from the starting node.
    #Reference: Oregon State University - CS325 - Week5 - Graph Algorithms: Part I BFS & DFS(.pdf)
        #https://oregonstate.instructure.com/courses/1772237/pages/graph-algorithm-videos-and-lecture-notes?module_item_id=18984114
    #Time Complexity: O(V + E), where V is number of vertices and E is number of edges
    def BFS(self, start):
        #Create a queue
        queue = [] 

        #Append the starting vertex to the queue
        queue.append(start) 

        # While all the vertices haven't been explored
        while queue:
            #Dequeue and store a visited vertex
            node = queue.pop(0)
            #Add this visited vertex's neighbors to the queue
            for key in self.vertices[node].neighbors:
                #If a neighbor is unvisited (ie. WHITE), explore it
                if self.vertices[key].color == "WHITE":
                    #Change its color to GREY, indicating has been explored
                    self.vertices[key].color = "GREY"
                    #set its parent to the visited vertex
                    self.vertices[key].parent = self.vertices[node]
                    #update its distance to be 1 greater than its parent's distance from the starting node
                    self.vertices[key].distance = self.vertices[key].parent.distance + 1
                    #append the vertex
                    queue.append(self.vertices[key].name)
            #set the visited vertex's color to BLACK, indicating it has been visited
            self.vertices[node].color = "BLACK"
        #After performing BFS on the starting vertex, check each vertex's color in the graph
        #If a vertex's color is WHITE (ie. unexplored), perform call BFS on that node
        #This will call BFS until all disconected components of the graph are explored. 
        for key in self.vertices:
            if self.vertices[key].color == "WHITE":
                self.BFS(self.vertices[key].name)

    #This function assigns wrestlers to teams by sorting by even an odd distance from the starting node.
    #If a vertex's distance from the starting vertex is even, then it is assigned to the Babyfaces team.
    #If a vertex's distance from the starting vertex is odd, then it is assigned to the Heels team.
    #Time-Complexity: O(V), where V is number of vertices
    def make_teams(self):
        for key in sorted(list(self.vertices.keys())):
            #if the distance to the vertex is even, add the vertex to babyfaces dictionary
            if self.vertices[key].distance % 2 == 0:
                self.babyfaces[key] = key
            #if the distance to the vertex is odd, add the vertex to heels dictionary
            else:
                self.heels[key] = key

#This function accepts a filename as a string and runs the program
def run(filename):
    #Create a graph with each wrestler and rivalry, where the wrestlers are represented by vertices
    #and the rivalries are represented by the edges in the graph.  This is an undirected graph without weights.
    graph = Graph()
    #Open the file and add the wrestlers as vertices and rivalries as edges to the graph (adjacency list)
    with open(filename) as inFile:
        number_of_wrestlers = inFile.readline()
        first = True
        for wrestler in range(int(number_of_wrestlers)):
            if first == True:
                first_wrestler = inFile.readline().rstrip()
                graph.add_vertex(Vertex(first_wrestler))
                first = False
            else:
                wrestler_name = inFile.readline().rstrip()
                graph.add_vertex(Vertex(wrestler_name))

        number_of_rivalries = inFile.readline()
        for rivalry in range(int(number_of_rivalries)):
            competitors = inFile.readline().rstrip()
            competitors = competitors.split(" ")
            graph.add_edge(competitors[0], competitors[1])
    inFile.close()

    #Run BFS, using the first wrestler as the starting vertex
    graph.BFS(first_wrestler)
    #Assign wrestlers to teams (Babyfaces or Heels)
    graph.make_teams()
    #Print the teams to the console
    graph.print_teams()

#Enter your file name into the run() function to run the program
run("wrestler.txt")
