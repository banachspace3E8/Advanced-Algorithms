#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 20:47:40 2021

@author: khanshis
"""

#Shishir Khanal
#Class to implement Autoregressive Model
#This class doesn't work if y[0...n] =0 where n = number of desired eigenvalues
    #This is because the np.linalg.inv() in the batch least squates evaluation results in singluarity
import numpy as np
import random as random
from matplotlib import pyplot

class AR_RLS:
    def __init__(self, data, numberofeigenvalues, rowlength):
        self.data = data
        self.rowlength = rowlength
        #the notes start indexing from 1 we start from 0, test for consistency
        self.numberofeigenvalues = numberofeigenvalues
        #self.modelparameters = np.matrix()
        self.previousP = np.matrix(np.zeros((self.numberofeigenvalues, self.numberofeigenvalues)))
        self.P = np.matrix(np.zeros((self.numberofeigenvalues, self.numberofeigenvalues)))
        self.previoustheta = np.matrix(np.zeros((self.numberofeigenvalues, 1)))
        self.theta = np.matrix(np.zeros((self.numberofeigenvalues, 1)))
        self.phi = np.matrix(np.zeros((1, self.numberofeigenvalues)))

#------------Functions to evaluate BLS----------------------------------------
    def slicearray(self,array, start,end):
        capitalphi_i = array[start:end]
        return capitalphi_i[::-1]
    
    def evaluateY(self, capitalphi, finalindex):
        Y = capitalphi[:,0]
        Y = Y[1:]
        Y = np.append(Y,self.data[finalindex])
        return Y[:,None]

    def populatematrix(self):
        capitalphi = np.zeros((self.rowlength-1, self.numberofeigenvalues))
        # -1 to correct matrix indexing
        #capitalphi matrix only needs 'matrixsize - 1' elements
            #This is taken care by range function 'stop' index is not included
        for i in range(self.numberofeigenvalues, self.rowlength):
            index = (i - self.numberofeigenvalues)
            capitalphi[index,:] = self.slicearray(self.data,index,i)
        return capitalphi
    
    def batchleastsquares(self, initialdata):
        capitalphi = self.populatematrix()
        product = np.matmul(capitalphi.transpose(), capitalphi)
        self.previousP = np.linalg.inv(product) 
        Y = self.evaluateY(capitalphi,self.rowlength - 1)
        self.previoustheta = np.matmul(self.previousP, np.matmul(capitalphi.transpose(), Y))
        return
#--------------end Functions to evaluate BLS----------------------------------

#--------------Functions to aid RLS-------------------------------------------  
    def buildphi(self, index):
        return self.slicearray(self.data,(index - self.numberofeigenvalues),index)
        
    def evaluateP(self):
        phi = np.asmatrix(self.phi)
        num = np.matmul(phi,self.previousP)
        den = 1 + np.matmul(phi, np.matmul(self.previousP,phi.transpose()))
        #den is a scalar matrix this could cause some problems
        dividend = np.divide(num, den)
        
        #[None,:] is to get the appropriate matrix product
        #Otherwise, matmul evaluates dot product for 1D arrays by default
        secondterm = np.matmul(self.previousP, np.matmul(phi.transpose(), dividend))
        
        P = np.subtract(self.previousP,secondterm)
        return P
    
    def evaluatetheta(self, currentdata):
        parenthesisterm = currentdata - np.matmul(self.phi,self.previoustheta)
        num = np.matmul(self.P, self.phi[:,None])
        den = 1 + np.matmul(self.phi, np.matmul(self.P, self.phi[:,None]))
        dividend = np.divide(num, den)
        secondterm = dividend*parenthesisterm     
        theta = np.add(self.previoustheta, secondterm)
        return theta
#------------end Functions to aid RLS-----------------------------------------

#------------RLS implementation-----------------------------------------------
    def evaluatemodel(self):
        modelparameters = np.matrix(np.zeros((self.numberofeigenvalues, (len(self.data)-self.rowlength+1))))
        self.batchleastsquares(self.data[:self.rowlength])
        modelparameters[:,0] = self.previoustheta
        for i in range(self.rowlength, len(self.data)):
            self.phi = self.buildphi(i)
            self.P = self.evaluateP()
            self.theta = self.evaluatetheta(self.data[i])
            modelparameters[:,i - self.rowlength +1] = self.theta
            self.previousP = self.P
            self.previoustheta = self.theta
        return modelparameters 
#------------end RLS implementation-------------------------------------------

def main():
    y = np.array(np.zeros(1000))
    yp = np.array(np.zeros(1000))
    #e = random.uniform(0,0.025)
    y[0] = 10
    y[1] = 15
    rowlength = 100#rowlength should be >># of eigenvalues
    for i in range(2, len(y)):
        #s^2 + 2*s*(1/2) + (1/2)^2
        y[i] = -0.15*y[i-1]-0.92*y[i-2]+random.uniform(0,0.025)
    pyplot.plot(y[0:50])
    classar = AR_RLS(y,5,rowlength)
    modelparams = classar.evaluatemodel()
    yp[0] = 10   
    yp[1] = 15
    param = modelparams[:,900]
    for i in range(2, len(yp)):
        #s^2 + 2*s*(1/2) + (1/2)^2
        yp[i] = param[0]*yp[i-1]+param[1]*yp[i-2]+param[2]*yp[i-3]+param[3]*yp[i-4]+param[4]*yp[i-5]+random.uniform(0,0.025)
    pyplot.plot(yp[0:50])
    #pyplot.plot(modelparams)
    #print(modelparams[:,994])
    
if __name__ == "__main__":
    main();  