# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:02:20 2022

@author: Xander
"""

import numpy as np

def OptimalDetect(Constellation,Sigma,ReceivedSymbol,TransmissionProbs=None):
    """@brief: Finds the optimal detection of a received symbol.
    @param Constellation: A list of symbols in the constellation mapped from the origin.
    @param Sigma: The standard deviation of the noise.
    @param ReceivedSymbol: The received symbol.
    @param TransmissionProbs: The probabilities of each symbol in the constellation being transmitted.
    @return: A list containing the probability of the received symbol, the probabilities of each symbol in the constellation, and the optimal detected symbol."""
    BestCost=np.Inf
    BestIndex=0
    Constellation=np.array(Constellation)
    if (TransmissionProbs is None):
        TransmissionProbs=np.ones(len(Constellation,))
    else:
        TransmissionProbs=np.array(TransmissionProbs)
    Beta=0
    Probabilities=[]
    for x in range(0,len(Constellation)):
        CurrProb=TransmissionProbs[x]*np.exp(-abs(ReceivedSymbol-Constellation[x])**2/(2*Sigma**2))[0]
        Beta+=CurrProb
        Probabilities.append(CurrProb)
    Probabilities/=Beta
    return [Beta,Probabilities,Constellation[np.argmax(Probabilities)]]

#example
eightpsk=[1,(1+1j)/np.sqrt(2),1j,(-1+1j)/np.sqrt(2),-1,(-1-1j)/np.sqrt(2),-1j,(1-1j)/np.sqrt(2)]
r=[0.1707 + 0.3712j]
sigma=0.4082
print(OptimalDetect(eightpsk,sigma,r))
