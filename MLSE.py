# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 15:25:47 2022

@author: Xander
"""

# This mimicks the Viterbi algorithm, but with a different cost function.
# The cost function is the sum of the squared errors of the received signal
# and the convolution of the channel impulse response and the current state.
# The state is a list of the last L-1 symbols, where L is the length of the
# channel impulse response. The state is updated by adding the current symbol
# to the front of the list, and removing the last symbol from the list.
# The state is a list of the last L-1 symbols, where L is the length of the
# channel impulse response. The state is updated by adding the current symbol
# to the front of the list, and removing the last symbol from the list.
# A trellis is generated with the possible states as the nodes, and the
# possible symbols as the edges. The cost of each edge is the sum of the
# squared errors of the received signal and the convolution of the channel.
# Transitions are printed out, and invalid transitions are marked with 99. Each state is numbered according to how "high" it is relative to other states (like 11 in binary being 3 vs 10 being 2).



import numpy as np
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

def MLSE(CIR,received,N,Constellation):
    """@brief: Performs MLSE decoding on a received signal.
    @param CIR: The channel impulse response.
    @param received: The received signal.
    @param N: The number of symbols to decode, without any prefix or suffix.
    @param Constellation: A list of the possible symbols.
    @return: A list of the decoded symbols."""
    global possiblesymbols
    L=len(CIR)
    NumVerticals=N+L
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
            if(x>N):
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
                cost=np.array(received[x-1])-np.dot(state,CIR)
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
        
            
            
BPSK=[1,-1]
QPSK=[1,1j,-1,-1j]
c1=[0.5824,-0.7065,0.3645]
r1=[-0.1967,-0.4586,0.7886,1.2101,-0.1460]
N1=3
print(MLSE(c1,r1,N1,BPSK));
c = [-0.82, 0.37]
r = [1.2963 - 0.1303j  ,-0.3537- 1.1293j  , 0.3058 + 1.3510j  ,-0.9276 - 0.2167j]
N=3
print(MLSE(c,r,N,QPSK))                
                
    
    
