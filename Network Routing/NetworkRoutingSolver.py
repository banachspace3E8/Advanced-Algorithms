#!/usr/bin/python3


from CS4412Graph import *
from Priorityqueue import *
import time
import sys

class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS4412Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while destIndex != node.node_id:
            #edge = node.neighbors[2]
            
            path_edges.append( (self.network.nodes[self.prev[destIndex]].loc, self.network.nodes[destIndex].loc, '{:.0f}'.format(self.distance[destIndex])) )
            total_length += self.distance[destIndex]
            destIndex = self.prev[destIndex]
            # node = edge.dest
            # edges_left -= 1
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        if use_heap == False:
            self.dijkstra(self.network, srcIndex, priorityqueuearray(self.network.nodes))
            
        elif use_heap == True:
            self.dijkstra(self.network, srcIndex, priorityqueuebinaryheap(self.network.nodes))
        t2 = time.time()
        return (t2-t1)


    def dijkstra(self, Graph, source, PQ):
        self.Nodes = Graph.getNodes();
        self.prev = {}
        self.distance = {}
        self.pointdistance = {}
        
        for node in self.Nodes:
            self.distance[node.node_id] = sys.maxsize
            self.prev[node.node_id] = None
            print(node.node_id)
            
        self.distance[source] = 0  
        PQ.decrease_key(source,0)

        while PQ.getsize() != 0:
            
            u = PQ.delete_min()
            for edge in u.neighbors:
                if self.distance[edge.dest.node_id] > self.distance[u.node_id] + edge.length:
                    self.distance[edge.dest.node_id] = self.distance[u.node_id] + edge.length
                    self.prev[edge.dest.node_id] = u.node_id
                    PQ.decrease_key(edge.dest.node_id, self.distance[edge.dest.node_id])
                    self.pointdistance[edge.dest.node_id] = edge.length