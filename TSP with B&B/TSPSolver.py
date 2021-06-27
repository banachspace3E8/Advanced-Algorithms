#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
        
            
class TSPSolver:
    def __init__( self, gui_view ):
        self._scenario = None

    def setupWithScenario( self, scenario ):
        self._scenario = scenario


    ''' <summary>
        This is the entry point for the default solver
        which just finds a valid random tour.  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of solution, 
        time spent to find solution, number of permutations tried during search, the 
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''
    def fillcost(self, costmatrix, cities):
        #Fill the cost to reach nodes from one another
        #in the costmatrix
        for i in range(len(cities)): 
            for j in range(len(cities)):
                costmatrix[i][j] = cities[i].costTo(cities[j])
        return costmatrix

    def reduceRow(self,costmatrix, rowind):
        #subtract the columns of the current row index
        #by the min value
        row = []
        for i in range(len(costmatrix)):
            row.append(costmatrix[rowind][i])
        minval = min(row)
        if minval == float('inf'):
            return 0
        for i in range(len(costmatrix[rowind])):
            costmatrix[rowind][i] -= minval
        return minval

    def reduceColumn(self,costmatrix, colind):
        #subtract the rows of the current col index
        #by the min value
        column = []
        for i in range(len(costmatrix)):
            column.append(costmatrix[i][colind])
        minval = min(column)
        if minval == float('inf'):
            return 0
        for i in range(len(costmatrix)):
            costmatrix[i][colind] -= minval
        return minval

    def reduceCostMatrix(self,costmatrix):
        #iterate through the costmatrix to produce
        #reduced cost matrix and initial lower bound
        lowbound = 0
        for i in range(len(costmatrix)):
            lowbound += self.reduceRow(costmatrix, i)
        for i in range(len(costmatrix)):
            lowbound += self.reduceColumn(costmatrix, i)
        return lowbound
              
    def setColumninf(self,costmatrix, column, value):
        #set the particular column to a desired value
        for i in range(len(costmatrix)):
            costmatrix[i][column] = value
    
    def setRowinf(self,costmatrix, row, value):
        #set the particular row to a desired value
        for i in range(len(costmatrix)):
            costmatrix[row][i] = value   
    
    def lastnode(self,bssf,lowerbound,cities,visited):
        #update the information to the best solution so far 
        #when the last node is reached
        if lowerbound < bssf['cost']:
                    bssf['soln'] = []
                    for i in visited:
                        bssf['soln'].append(cities[i])
                    bssf['soln'] = TSPSolution(bssf['soln'])
                    bssf['cost'] = bssf['soln']._costOfRoute()
                    bssf['count'] += 1
        return bssf
        
    def defaultRandomTour( self, time_allowance=60.0 ):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time()-start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation( ncities )
            route = []
            # Now build the route using the random permutation
            for i in range( ncities ):
                route.append( cities[ perm[i] ] )
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count
        results['soln'] = bssf
        results['max'] = None
        results['total'] = None
        results['pruned'] = None
        return results


    ''' <summary>
        This is the entry point for the greedy solver, which you must implement for 
        the group project (but it is probably a good idea to just do it for the branch-and
        bound project as a way to get your feet wet).  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number of solutions found, the best
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    def greedy( self,time_allowance=60.0 ):
        pass
    
    
    
    ''' <summary>
        This is the entry point for the branch-and-bound algorithm that you will implement
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number solutions found during search (does
        not include the initial BSSF), the best solution found, and three more ints: 
        max queue size, total number of states created, and number of pruned states.</returns> 
    '''
        

    def branchAndBound( self, time_allowance=60.0 ):
    
        ''' <summary>
        This is the entry point for the algorithm you'll write for your group project.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number of solutions found during search, the 
        best solution found.  You may use the other three field however you like.
        algorithm</returns> 
        '''    
        #initialize variables
        totalstates = 1
        prunnedstates = 0
        maximumstates = 0
        starttimer = time.time()
        cities = self._scenario.getCities()
        costmatrix = np.zeros([len(cities),len(cities)])
        #fill the matrix with cost values and generate reduced cost matrix
        costmatrix = self.fillcost(costmatrix, cities)      
        lowerbound = self.reduceCostMatrix(costmatrix)
        
        #store the costmatrix and lowerbound in the priority queue 
        priorityqueue = []
        heapq.heappush(priorityqueue, (len(cities) - 1, lowerbound, [0], costmatrix))
        #generate the initial bssf using a random tour function
        initialbssf = self.defaultRandomTour(time.time())
        bssf = {}
        bssf['cost'] = initialbssf['cost']
        bssf['soln'] = initialbssf['soln']
        bssf['count'] = 1
        
        while len(priorityqueue) != 0 and (time.time() - starttimer) < 60:
            #prune the branches based on the min value of the pq
            state = heapq.heappop(priorityqueue)
            depth = len(cities) - state[0]
            lowerbound = state[1]
            visited = state[2]
            costmatrix = state[3]
            if depth == len(cities):
                bssf = self.lastnode(bssf,lowerbound,cities,visited)
                continue
            
            #create state for every possible path
            for i in range(1, len(cities)):
                newlowerbound = lowerbound
                #if the location is not invalid
                if costmatrix[visited[len(visited) - 1]][i] != float('inf'):
                    #copy the cost matrix
                    newcostmatrix = np.array(costmatrix)
                    newlowerbound += newcostmatrix[visited[len(visited) - 1]][i]
                    #set the current row & col index to inf
                    self.setRowinf(newcostmatrix, visited[len(visited) - 1], float('inf'))
                    self.setColumninf(newcostmatrix, i, float('inf'))
                    newcostmatrix[i][visited[len(visited) - 1]] = float('inf')
                    #evalaute the lower bound
                    newlowerbound += self.reduceCostMatrix(newcostmatrix)
                    totalstates += 1
                    #if the lowerbound is less than the bssf, push the info in the heap
                    if newlowerbound < bssf['cost']:
                        newvisited = list(visited)
                        newvisited.append(i)
                        heapq.heappush(priorityqueue, (len(cities) - depth - 1, newlowerbound, newvisited, newcostmatrix))
                        #maxstates is the maximum of the value of maxstate till now or the priority queue
                        maximumstates = max(maximumstates, len(priorityqueue))
                        continue
                    prunnedstates += 1
                    
                    
        bssf['time'] = time.time() - starttimer
        bssf['max'] = maximumstates
        bssf['total'] = totalstates
        bssf['pruned'] = prunnedstates
        return bssf

        
    def fancy( self,time_allowance=60.0 ):
        pass
        



