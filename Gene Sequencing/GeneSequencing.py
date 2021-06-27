#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
    from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

    def __init__( self ):
        pass

    
# This is the method called by the GUI.  _sequences_ is a list of the ten sequences, _table_ is a
# handle to the GUI so it can be updated as you find results, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you 
# how many base pairs to use in computing the alignment

#checks for the match of diagonal elements
    def diagonalscore(self, element1, element2):
        if element1 == element2:
            return MATCH
        else:
            return SUB
        
#computes the cost of the unrestricted algorithm
    def computecost_unrestricted(self,A, B):
        costmatrix = [[0 for i in range(len(B)+1)] for j in range(len(A)+1)]
        backpointer = [[0 for i in range(len(B)+1)] for j in range(len(A)+1)]
        
        for i in range(1,len(A)+1):
            costmatrix[i][0] =INDEL * i
            
        for j in range(1,len(B)+1):
            costmatrix[0][j] = INDEL * j
            
        for  i in range(1, len(A)+1):
            for j in range(1, len(B)+1):
                match = costmatrix[i-1][j-1] + self.diagonalscore(A[i-1], B[j-1])
                delete = costmatrix[i-1][j] + INDEL
                insert = costmatrix[i][j-1] + INDEL
                if min(match, insert, delete) == match:
                    backpointer[i][j] = "match"
                elif min(match, insert, delete) == delete:
                    backpointer[i][j] = "delete"
                elif min(match, insert, delete) == insert:
                    backpointer[i][j] = "insert"
                costmatrix[i][j] = min(match, insert, delete) 
        return costmatrix[len(A)][len(B)], backpointer
    
    #evalautes the indices of the matrices in the banded coordinates
    def evaluateindices(self, costmatrix, i, j):
        #transform in the band range
        jband = j - i + MAXINDELS
        if not 0 <= jband < 2 * MAXINDELS + 1:
            return math.inf
        return costmatrix[i][jband]
    
    #computes the cost of the banded algorithm
    def computecost_banded(self, A, B): 
        costmatrix = [[0 for i in range(2 * MAXINDELS + 1)] for j in range(len(A) + 1)]
        backpointer = [[0 for i in range(2 * MAXINDELS + 1)] for j in range(len(A) + 1)]
        # fill the first row and column
        for i in range(1, MAXINDELS + 1):
            costmatrix[i][0] = INDEL * i
            backpointer[i][0] = "delete"
        for j in range(1, MAXINDELS + 1):
            costmatrix[0][j] = INDEL * j
            backpointer[0][j] = "insert"
            
        for i in range(1, len(A) + 1):
            #loop over the particular band range
            for j in range(max(1, i - MAXINDELS), min(len(B), i + MAXINDELS) + 1):
                match =  self.evaluateindices(costmatrix,i - 1, j - 1) + self.diagonalscore(A[i-1], B[j-1])
                delete = self.evaluateindices(costmatrix,i - 1, j)  + INDEL
                insert = self.evaluateindices(costmatrix,i , j - 1) + INDEL
                #fill the backpointer array
                if min(match, insert, delete) == match:
                    backpointer[i][j - i + MAXINDELS] = "match"
                elif min(match, insert, delete) == delete:
                    backpointer[i][j - i + MAXINDELS] = "delete"
                elif min(match, insert, delete) == insert:
                    backpointer[i][j - i + MAXINDELS] = "insert" 
                costmatrix[i][j - i + MAXINDELS] = min(match, delete, insert)
        return self.evaluateindices(costmatrix, len(A), len(B)),backpointer

    #compute the text alignment
    def alignment(self, backpointer, i,j, A,B):
        i = len(A)
        j = len(B)
        newA = []
        newB = []
        while i > 0 or j > 0:
            if backpointer[i][j] == "match":
                newA.append(A[i-1])
                newB.append(B[j-1])
                i = i-1
                j = j-1
            elif backpointer[i][j] == "insert":
                newA.append("-")
                newB.append(B[j-1])
                j = j-1
            elif backpointer[i][j] == "delete":
                newA.append(A[i-1])
                newB.append("-")
                i = i-1
            return newA, newB
                
    def align( self, sequences, table, banded, align_length):
        self.banded = banded
        self.MaxCharactersToAlign = align_length
        sequencei = [0 for i in range(self.MaxCharactersToAlign)]
        sequencej = [0 for j in range(self.MaxCharactersToAlign)]
        results = []
        backpointer = []
        for i in range(len(sequences)):
            jresults = []
            for j in range(len(sequences)):

                if(j < i):
                    s = {}
                else:
                    if self.MaxCharactersToAlign > len(sequences[i]):
                        sequencei = sequences[i]
                    if self.MaxCharactersToAlign > len(sequences[j]):
                        sequencej = sequences[j]
                    else:
                        sequencei = sequences[i][:self.MaxCharactersToAlign]
                        sequencej = sequences[j][:self.MaxCharactersToAlign]
                    if banded:
                        minscore, backpointer = self.computecost_banded(sequencei, sequencej)
                        score = minscore
                        alignment1, alignment2 = self.alignment(backpointer,MAXINDELS,MAXINDELS, sequencei, sequencej)
                    else:
                        minscore, backpointer = self.computecost_unrestricted(sequencei, sequencej)
                        score = minscore
                        alignment1, alignment2 = self.alignment(backpointer, len(sequencei),len(sequencej),sequencei, sequencej)
###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
                    # alignment1 = 'abc-easy  DEBUG:(seq{}, {} chars,align_len={}{})'.format(i+1,
                    #     len(sequences[i]), align_length, ',BANDED' if banded else '')
                    # alignment2 = 'as-123--  DEBUG:(seq{}, {} chars,align_len={}{})'.format(j+1,
                    #     len(sequences[j]), align_length, ',BANDED' if banded else '')
###################################################################################################                    
                    s = {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
                    table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
                    table.update()    
                jresults.append(s)
            results.append(jresults)
        return results


