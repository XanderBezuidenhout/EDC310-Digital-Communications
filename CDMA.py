# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 13:58:56 2022

@author: Xander
"""

import numpy as np
import scipy as sp

def CDMADecode(P,N,G,Transmission,Constellation,Spreads=None):
    """@brief: Decodes a transmission to extract a specific user's data using CDMA.
    @param P: The number of users.
    @param N: The number of symbols per user.
    @param G: The number of chips per symbol (coding rate).
    @param Transmission: The superimposed transmission.
    @param Constellation: The constellation used to encode the data.
    @param Spreads: The spreading sequences used to encode the data, if none are given then a hadamard matrix is used."""
    if (Spreads is None):
        Spreads=sp.linalg.hadamard(G)[:P]
    Chips=np.tile(Spreads,N)
    Decode=np.multiply(Chips,Transmission)
    Transmission=np.reshape(Decode, (P,N,G))
    AllUsersDecoded=[]
    for x in range(0,P):
        CurrUserDecoded=[]
        for y in range(0,N):
            index=np.argmin(abs(sum(Transmission[x][y])-Constellation))
            CurrUserDecoded.append(Constellation[index])
        AllUsersDecoded.append(CurrUserDecoded)
    return AllUsersDecoded
def CDMAEncode(P,N,G,EachUserData,Spreads=None):
    """@brief: Encodes data for each user using CDMA.
    @param P: The number of users.
    @param N: The number of symbols per user.
    @param G: The number of chips per symbol (coding rate).
    @param EachUserData: The data to be encoded for each user.
    @param Spreads: The spreading sequences used to encode the data, if none are given then a hadamard matrix is used.
    @return: The superimposed transmission."""
    if (Spreads is None):
        Spreads=sp.linalg.hadamard(G)[:P]
    Chips=np.tile(Spreads,N)
    RepeatSym=np.repeat(EachUserData,G,axis=1)
    Encoded=np.multiply(Chips,RepeatSym)
    SuperImposedTransmission=np.sum(Encoded,axis=0)/np.sqrt(P*G)
    return SuperImposedTransmission.tolist()
#CLASS EXAMPLE
P=2
N=2
G=4
Transmit=[[1,-1],[-1,1]]
spread=[[1,-1,1,-1],[1,-1,-1,1]]
received=CDMAEncode(P, N, G, Transmit,spread)
#print(received)
bpsk=[1,-1]
qpsk=[1,1j,-1,-1j]
decoded=CDMADecode(P, N, G, received,bpsk,spread)
print(decoded)
        
    