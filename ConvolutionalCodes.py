# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:25:47 2022

@author: Xander
"""

import numpy as np


def GetTransitionOutput(PrevState,NextState,g):
    """@brief: Gets the output of a transition between two states in a convolutional code.
    @param PrevState: The previous state of the convolutional code.
    @param NextState: The next state of the convolutional code.
    @param g: The generator matrix of the convolutional code.
    @return: The output of the transition between the two states.
    """
    FullState=[NextState[0]]+PrevState
    for x in range(len(FullState)):
        if (FullState[x]==-1):
            FullState[x]=0
    Output=[np.dot(g[x],FullState)%2 for x in range(len(g))]
    return Output

possiblesymbols=[]
def CreateAllPossibleStates(Constellation,Combination,k):
    global possiblesymbols;
    if (k<=0):
        possiblesymbols.append(Combination)
        return
    for i in range(len(Constellation)):
        newcombination=Combination+[Constellation[i]]
        CreateAllPossibleStates(Constellation,newcombination,k-1)
bpsk=[1,-1]

def MLSE(g,received,N,Constellation):
    """@brief: Performs convolutional decoding on a received signal.
    @param g: The generator matrix of the convolutional code.
    @param received: The received signal.
    @param N: The number of symbols to decode, without any prefix or suffix.
    @param Constellation: The constellation used to transmit the signal.
    @return: A list of the decoded symbols.
    """
    global possiblesymbols
    L=len(g[0])
    NumVerticals=N+1
    NumHorizontals=int((len(Constellation)))**(L-1)
    Alphas=np.full((NumVerticals,NumHorizontals),99,float)
    HasParents=np.full((NumVerticals,NumHorizontals),False,bool)
    HasParents[0][0]=True#first index is the vertical layer, second is the node within layer
    HasParents[-1][0]=True
    Alphas[0][0]=0
    Deltas=[]
    possiblesymbols=[]
    CreateAllPossibleStates(Constellation,[],L-1)
    
    for x in range(1,NumVerticals):
        LayerDeltas=[]
        for y in range(0,NumHorizontals):
            CurrNode=possiblesymbols[y]
            CurrNodeDeltas=np.full((NumHorizontals,),99,float)
            if(x>N+1):
                if(not np.array_equal(np.full((x-N,),Constellation[0]), CurrNode[:x-N])):# at the end of trellis, needs to shift 1s in
                    LayerDeltas.append(CurrNodeDeltas)
                    continue
            if(x<L-1):#at start of trellis,last few symbols must be 1s
                ehem=np.full((L-x-1,),Constellation[0])
                ooh=CurrNode[(x):]
                if (not np.array_equal(ehem, ooh)):
                    LayerDeltas.append(CurrNodeDeltas)
                    continue
            for z in range(0,NumHorizontals):
                PrevNode=possiblesymbols[z]
                if (not np.array_equal(CurrNode[1:],PrevNode[:-1])):
                    continue
                if (not HasParents[x-1][z]): #check if prevnode has parents
                    continue
                HasParents[x][y]=True
                state=np.concatenate(([CurrNode[0]],PrevNode))
                cost=sum(np.bitwise_xor(np.array(GetTransitionOutput(PrevNode, CurrNode, g)).astype(int),np.array(received[x-1]).astype(int)))
                cost*=2
                delta=abs(cost)**2
                CurrNodeDeltas[z]=delta
            LayerDeltas.append(CurrNodeDeltas)
            MinCostBackPathIndex=np.argmin(CurrNodeDeltas)
            Alphas[x][y]=Alphas[x-1][MinCostBackPathIndex]+CurrNodeDeltas[MinCostBackPathIndex]
        Deltas.append(LayerDeltas)
    for x in range(0,len(possiblesymbols)):
        for y in range(len(possiblesymbols)):
            print(str(len(possiblesymbols)-x-1)+"->"+str(len(possiblesymbols)-y-1)+str((np.array(Deltas)[:,y,x]).tolist()))
    CurrNodeIndex=0
    Path=[]
    for x in reversed(range(1,NumVerticals)):
        CurrNode=possiblesymbols[CurrNodeIndex]
        for y in range(0,(NumHorizontals)):
            CurrAlpha=Deltas[x-1][CurrNodeIndex][y]+Alphas[x-1][y]
            if (CurrAlpha==Alphas[x][CurrNodeIndex]):
                CurrNodeIndex=y
                Path.insert(0,CurrNode[0])
                continue
    Path.insert(0,CurrNode[0])
    Path=Path[L-2:-(L-1)]
    return Path

def ConvolutionalEncode(k,SourceBits,g):
    """@brief: Encodes a sequence of bits using a convolutional code.
    @param k: The number of bits per symbol.
    @param SourceBits: The sequence of bits to encode.
    @param g: The generator matrix of the convolutional code.
    @return: A list of the encoded bits."""
    state=np.zeros((k-1,)).tolist()
    SourceBits+=state
    code=[]
    for x in range(len(SourceBits)):
        PrevState=state.copy()
        state.insert(0,SourceBits[x])
        state=state[:-1]
        NextState=state.copy()
        code.append(np.array(GetTransitionOutput(PrevState, NextState, g)).flatten().tolist())
    return code
g = [4, 6, 5]  
s= [1, 0, 1, 0, 1]   
k=3
n=9        
for x in range(0,k):
        g[x]=[int(i) for i in list('{0:0b}'.format(g[x]))]
        while (len(g[x])<k):
            g[x].insert(0,0)  
coded=ConvolutionalEncode(k, s, g)
print(coded)
decoded=MLSE(g,coded,len(s)-(k-1),[1,-1])
#print(decoded)
#c_est =[1, 1,-1, 1,-1, 1, 1,-1, 1, 1, 1,-1, 1,-1,-1,-1, 1,-1,-1,-1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1,-1, 1 ] 
#k=4
#n=int(len(c_est)/(k-1))
#g=[[1,0,0,0],[1,0,1,0],[0,1,1,1]]
#decoded=MLSE(g,c_est,n,[1,-1])
 #(g,received,N,Constellation)   
#print(decoded)
