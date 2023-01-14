# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 23:01:08 2022

@author: Xander
"""

import numpy as np

def ChannelEstimation(PilotStartPosition,PilotLength,CIRLength,Received,Transmitted):
    """@brief: Estimates the channel impulse response using a pilot sequence.
    @param PilotStartPosition: The start position of the pilot sequence.
    @param PilotLength: The length of the pilot sequence.
    @param CIRLength: The length of the channel impulse response.
    @param Received: The received signal.
    @param Transmitted: The originally known transmitted sequence of symbols.
    @return: A list of the estimated channel impulse response."""
    Pilot=Transmitted[PilotStartPosition:PilotStartPosition+PilotLength]
    
    Q=[] #generate Q-matrix with P-L+1 rows, and L columns
    for x in range(0,PilotLength-CIRLength+1):
        row=[]
        for y in reversed(range(x,x+CIRLength)):
            row.append(Pilot[y])
        Q.append(row)
    print(Q)
    QH=np.array(np.matrix(Q).getH())
    print(QH)
    r=Received[PilotStartPosition:PilotStartPosition+len(Q)]
    QHr=np.matmul(QH,r)
    print(QHr)
    QHQ=np.matmul(QH,Q)
    print(QHQ)
    c_exact=np.matmul(QHr,np.linalg.inv(QHQ))
    k=QHQ[0][0]
    c_est=(QHr/k)
    return [c_exact,c_est]
#CLASS EXAMPLE
N=20
L=4
P=8
s= [ -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, -1] 
r = [ 0.5284, 1.6983, 0.9833,-0.5284,-1.6983,-0.9833, 0.3836, 0.0419,-1.6983, -0.9833, 0.5284,
1.6983, 0.9833,-0.3836,-0.1866, 0.1866,-0.1866, 0.1143, -0.8701, 0.2851] 
StartPos=int(len(s)/2)-int(P/2)#pilot placed in the middle of data
#print(ChannelEstimation(StartPos,P,L,r,s))

#TUTORIAL PROBLEM
N=30
P=16
L=4
s=[1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,1,1,-1,-1,-1,1,1,1,-1,1,-1] 
r=[0.7387,-0.7387,0.7387,0.3830,0.3801,1.0550,-0.7387,0.7387,0.3830,1.5018,0.6964,1.0550,0.3830,0.3801,1.0550,0.3830,0.3801,-0.0667,-0.3801,0.0667,1.5018,0.6964,-0.0667,-1.5018,-0.6964,-1.0550,0.7387,-0.1778,0.5594,0.1581] 
StartPos=int(len(s)/2)-int(P/2)#pilot placed in the middle of data
print(ChannelEstimation(StartPos,P,L,r,s))