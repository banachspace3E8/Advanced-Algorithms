# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 16:02:44 2021

@author: Shishir
"""
import sys

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


class priorityqueuearray:
    def __init__( self, graph_nodes):
        self.pq_array = [[node, sys.maxsize] for node in graph_nodes]
        self.size = len(graph_nodes)
        self.index = [0]*self.size
        self. insert(graph_nodes, self.index)
 
    def insert(self, graph_nodes, index):  
        for ind, node in enumerate(graph_nodes):
            self.index[node.node_id] = ind
            
    def getsize(self):
            return len(self.pq_array)
    
    def distanceweight(self, i):
        return self.pq_array[i][1]
    
    def swap(self, index1, index2):
        self.pq_array[index1], self.pq_array[index2] = self.pq_array[index2], self.pq_array[index1]
        temp1 = self.pq_array[index1][0].node_id
        temp2 = self.pq_array[index2][0].node_id
        self.index[temp1], self.index[temp2] = self.index[temp2], self.index[temp1]
        

    def decrease_key(self, ind, distance):
        temp = self.index[ind]
        if temp >= self.size:
            return "unity index"
        self.pq_array[temp][1] = distance
            
    def delete_min(self):
        if self.size ==0:
            return "no array"
        i = min(range(self.size), key = self.distanceweight)
        self.swap(i, self.size-1)
        minimum, pos = self.pq_array.pop()
        self.size -= 1
        return minimum
            
    
#
#
#
#  
    
    
class priorityqueuebinaryheap:
    def __init__(self, graph_nodes):
        self.pq_array = [[node, sys.maxsize] for node in graph_nodes]
        self.size = len(graph_nodes)
        self.index = [0]*self.size
        self.insert(graph_nodes, self.index)
        self.heapify()
      
    def getsize(self):
        return len(self.pq_array) 
        
    def insert(self, graph_nodes, index):  
        for ind, node in enumerate(graph_nodes):
            self.index[node.node_id] = ind
            
    def distanceweight(self, ind):
        return self.pq_array[ind][1]
    
    
    def getparentindex(self, ind):
        return (ind-1)//2
    
        #l_r =>  1 or 2 for left child or right child
    def getchildindex(self, ind, l_r):
        return 2*ind + l_r
    
    def isChild(self, ind):
        return 0 <= ind  and ind < self.size
    
    def isleafnode(self, ind):
        return self.isChild(ind) and not self.isChild(self.getchildindex(ind, 1))

  
    def heapify(self):
        for i in reversed(range(self.size)):
            if self.distanceweight(i) < self.distanceweight(self.getparentindex(i)):
                self.swap(self, i, self.getparentindex(i))
        
    def swap(self, index1, index2):
        self.pq_array[index1], self.pq_array[index2] = self.pq_array[index2], self.pq_array[index1]
        temp1 = self.pq_array[index1][0].node_id
        temp2 = self.pq_array[index2][0].node_id
        self.index[temp1], self.index[temp2] = self.index[temp2], self.index[temp1]
        
    def bubbleup(self, ind):
        while ind != 0 :
            if self.distanceweight(ind) >= self.distanceweight(self.getparentindex(ind)):
                break
            self.swap(ind, self.getparentindex(ind))
            ind = self.getparentindex(ind)
        
    def delete_min(self):
        if self.size == 0:
            return "Empty heap"
        self.swap(0, self.size-1)
        minimum, pos = self.pq_array.pop()
        self.size -= 1
        self.bubbledown(0)
        return minimum
    
    def bubbledown(self, ind):

        while self.isChild(ind) and not self.isleafnode(ind):
            lowestindex = ind
            if self.distanceweight(self.getchildindex(ind, 1)) < self.distanceweight(lowestindex):
                lowestindex = self.getchildindex(ind, 1)
                

            if self.isChild(self.getchildindex(ind, 2)) and self.distanceweight(self.getchildindex(ind, 2)) < self.distanceweight(lowestindex):
                lowestindex = self.getchildindex(ind,2)
            if lowestindex == ind:
                return
            self.swap(ind, lowestindex)
            ind = lowestindex

    
    def decrease_key(self, ind, distance):
        ii = self.index[ind]
        if ii >= self.size:
            return "unity index"
        self.pq_array[ii][1] = distance
        self.bubbleup(ii)
    
    