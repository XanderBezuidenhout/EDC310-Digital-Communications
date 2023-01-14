# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 23:35:24 2022

@author: Xander
"""
import scipy as sp
import numpy as np
from scipy.fft import fft,ifft
def Fourier(N):
    return  sp.linalg.dft(N)
def OFDMEncode(CIR,Big_s,N):
    """@brief: Performs an OFDM encoder.
    @param CIR: The channel impulse response.
    @param Big_s: The symbols to encode.
    @param N: The number of symbols to encode.
    @return: The encoded signal."""
    small_s=ifft(Big_s)
    small_s=np.concatenate((small_s[-(len(CIR)-1):],small_s)).tolist()
    #print(small_s)
    pad_zeros=np.zeros(len(small_s)-len(CIR))
    firstcol=np.concatenate((CIR,pad_zeros))
    Channel_Matrix=sp.linalg.tril(sp.linalg.circulant(firstcol))
    #print(Channel_Matrix)
    r=np.matmul(Channel_Matrix,small_s)
    return r.tolist()
def OFDMDecode(r,CIR):
    """@brief: Performs an OFDM decoder.
    @param r: The received signal.
    @param CIR: The channel impulse response.
    @return: The decoded signal."""
    r=r[len(CIR)-1:]
    R=fft(r)
    pad_zeros=np.zeros((len(R)-len(CIR),))
    padded_c=np.concatenate((CIR,pad_zeros))
    Lambda=fft(padded_c)
    S_est=np.divide(R,Lambda)
    return S_est.tolist()
#TUTORIAL PROBLEM
S = [0.0000 + 1.0000j,   1.0000 + 0.0000j,   0.0000 - 1.0000j,   1.0000 + 0.0000j,  -1.0000 + 0.0000j,   0.0000 - 1.0000j,   1.0000 + 0.0000j,   0.0000 + 1.0000j]
N=len(S)
c = [-0.37, 0.84, -0.55] 
encoded=OFDMEncode(c, S, N)
#print(encoded)
decoded=np.around(OFDMDecode(encoded,c),5)
#print(decoded)
#print(np.all(decoded==S))

S22 = [0.0000 - 1.0000j,  -1.0000 + 0.0000j,   0.0000 - 1.0000j,   1.0000 + 0.0000j,   1.0000 + 0.0000j,   0.0000 + 1.0000j,   0.0000 + 1.0000j,   0.0000 + 1.0000j]
c22 = [0.0201 - 0.0049j,   1.3651 - 0.2392j,   0.6655 + 0.3735j]

encoded=OFDMEncode(c22,S22,len(S22))
print(encoded)
decoded=np.around(OFDMDecode(encoded,c),5)
print(decoded)