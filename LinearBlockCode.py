# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:30:01 2022

@author: Xander
"""

import numpy as np
import scipy as sp
import random as random



def LinearBlockEncode(s,n,G=None,P=None):
    """@brief: Encodes a binary string using the Linear Block Code algorithm.
    @param s: The binary string to be encoded.
    @param n: The length of the codeword.
    @param G: The generator matrix.
    @param P: The parity check matrix.
    @return: The encoded binary string.
    """
    if (G is None):
        G=np.identity(len(s))
        G=np.hstack((G,P))
    #print(G)
    return np.matmul(s,G)%2

def LinearBlockDecode(c,k,n,G=None,P=None,num_iterations=10000):
    """@brief: Decodes a binary string using the Linear Block Code algorithm.
    @param c: The binary string to be decoded.
    @param k: The length of the original message.
    @param n: The length of the codeword.
    @param G: The generator matrix.
    @param P: The parity check matrix.
    @param num_iterations: The number of iterations to run the decoding algorithm, trying to find errors.
    @return: The decoded binary string."""
    if (G is None):
        G=np.identity(k)
        G=np.hstack((G,P))
    P=np.array(G)[:,k:]
    PT=np.transpose(P)
    ID=np.identity(len(PT))
    H=(np.hstack((PT,ID))).astype(int)
    #print(H)
    HT=(np.transpose(H)).astype(int)
    z=np.matmul(c,HT)%2
    #print(z)
    if sum(z)==0:#no errors found
        return c[:k]
    
    indices=[]
    for count in range(0,num_iterations):
        num_elements=np.random.randint(0,len(HT))
        possible=[x for x in range(0,len(HT))]
        sample_indices=random.sample(possible,num_elements)
        combination=HT[sample_indices]
        res=np.bitwise_xor.reduce(combination)
        if (sum(np.bitwise_xor(z,res))==0):#same
            sample_indices.sort()
            indices.append(sample_indices)
    if (len(indices)>0):
        indices=np.unique(indices)
        mini=0
        for x in range(0,len(indices)):
            if (len(indices[x])<len(indices[mini])):
                mini=x
        indices=indices[mini]
        for d in indices:
            c[d]^=1
    return c[:k]
    
#CLASS EXAMPLE
P=[[1,1,0,1,0,0],
[0,0,1,0,1,0],
[1,1,0,0,1,1],
[1,0,1,1,0,1],
[0,1,0,0,1,0],
[0,0,1,1,1,0],
[1,0,0,0,0,1],
[0,1,1,1,0,1 ]]
s = [ 1,0,0,1,0,1,1,1 ]
c=(LinearBlockEncode(s, len(s)+len(P[0]),None,P))
print(c)
decoded=LinearBlockDecode(c, len(s),len(s)+len(P[0]),None,P)
print(decoded)#should have no errors thus syndrom zero
c=[ 1,0,0,0,0,1,1,1,1,0,1,0,1,0 ] 
decoded=LinearBlockDecode(c, len(s),len(s)+len(P[0]),None,P)
print(decoded)#should have no errors thus syndrom zero
k=10
n=20
G = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1],
  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0],
  [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1]]
c_est = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1]
decoded=LinearBlockDecode(c_est, k, n,G)
print(decoded)
#ST2 2022
Q3_c_est = [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0] #uncoded bit sequence
Q3_P = \
[[0,0,1,0,0,0,1,1], #parity matrix
 [1,1,1,1,1,1,0,1],
 [1,0,1,0,1,1,1,1],
 [1,0,1,0,1,1,1,0],
 [1,0,1,0,1,1,0,0],
 [1,1,1,1,0,1,0,1],
 [1,0,1,0,1,0,0,0],
 [0,1,0,0,0,0,0,1]]
k=int(1.0/2.5)*len(Q3_P[0])
decoded=LinearBlockDecode(Q3_c_est, len(s),k+len(Q3_P[0]),None,Q3_P)
#print(decoded)


