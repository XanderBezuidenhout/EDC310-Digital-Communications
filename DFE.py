# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 21:43:24 2022

@author: Xander
"""

import numpy as np

def DFE(Constellation,CIR,Received,N):
    """@brief: Performs a decision feedback equalizer.
    @param Constellation: A list of the possible symbols.
    @param CIR: The channel impulse response.
    @param Received: The received signal.
    @param N: The number of symbols to decode.
    @return: A list of the decoded symbols."""

    LikelySequence=np.ones((len(CIR)-1,),int).tolist()
    Deltas=[]
    for x in range(0,N):
        CurrSeq=LikelySequence[-(len(CIR)-1):]
        currdelta=[]
        for y in range(0,len(Constellation)):
            CurrSeq.insert(0,Constellation[y])
            cost=abs(Received[x]-np.dot(CIR,CurrSeq))**2
            CurrSeq=CurrSeq[1:]
            currdelta.append(cost)
        Deltas.append(currdelta)
        LikelySequence.append(Constellation[np.argmin(currdelta)])
    LikelySequence=LikelySequence[len(CIR)-1:]
    return LikelySequence

#examples
bpsk=[1,-1]
N=4
C=[ 0.1685 ,  -0.3112,   -0.6987 ]
r = [ -0.7442 ,  -1.0812,   -0.4788 ,   1.2556 ]
print(DFE(bpsk,C,r,N))
qpsk=[1,1j,-1,-1j]
N=5
C = [0.69 - 0.27j,   0.54 + 0.30j]
r = [ 0.1749 + 0.7460j,  -0.1165 + 1.6443j,  -0.7804 + 0.5543j,  -0.3117 - 0.2266j, 0.0061 - 0.9386j ]
print(DFE(qpsk,C,r,N))