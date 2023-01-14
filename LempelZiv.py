# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 15:12:01 2022

@author: Xander
"""
import numpy as np
def LempelZivEncodeBinary(Data):
    """@brief: Encodes a binary string using the Lempel-Ziv algorithm.
    @param Data: The binary string to be encoded.
    @return: A list of encoded binary strings and a list of unique data pieces."""
    #Dictionary is entry of unique datapieces
    FullString=Data
    SubSet=""
    codewords=[]
    dictionary=[]
    #CREATE DICTIONARY AND POPULATE UNIQUE CODEWORDS
    LastIndex=0
    while (len(FullString)>0):
        SubSet+=FullString[0]
        FullString=FullString[1:]
        if (SubSet not in dictionary):
            dictionary.append(SubSet)
            codewords.append(format(LastIndex,'b')+SubSet[-1])
            SubSet=""
            LastIndex=0
        else:
            LastIndex=dictionary.index(SubSet)+1
    if (SubSet!=""):#last non-unique data left
        codewords.append(format(LastIndex,'b')+SubSet[-1])
        SubSet=""
    for x in range(0,len(codewords)):
        codewords[x]="0"*(int((np.log2(len(dictionary))))+1-len(codewords[x])) + codewords[x]
    return [codewords,dictionary]
    
def LempelZivEncodeChar(Data):
    """@brief: Encodes a string using the Lempel-Ziv algorithm.
    @param Data: The string to be encoded.
    @return: A list of encoded binary strings and a list of unique data pieces."""
    #Dictionary is entry of unique datapieces
    FullString=Data
    SubSet=""
    codewords=[]
    dictionary=[]
    #CREATE DICTIONARY AND POPULATE UNIQUE CODEWORDS
    LastIndex=0
    while (len(FullString)>0):
        SubSet+=FullString[0]
        FullString=FullString[1:]
        if (SubSet not in dictionary):
            dictionary.append(SubSet)
            codewords.append(str(LastIndex)+SubSet[-1])
            SubSet=""
            LastIndex=0
        else:
            LastIndex=dictionary.index(SubSet)+1
    if (SubSet!=""):#last non-unique data left
        codewords.append(str(LastIndex)+SubSet[-1])
        SubSet=""
    
    return [codewords,dictionary]


    
#CLASS EXAMPLE 1
BinaryData="10101101001001110101000011001110101100011011"
EncodedBinary=LempelZivEncodeBinary(BinaryData)
#print(EncodedBinary)
#CLASS EXAMPLE 2
CharData="AABABBBABAABABBBABBABBA"
#EncodedChar=LempelZivEncodeChar(CharData)
#print(EncodedChar)
#TUTORIAL QUESTION
BinaryData="00010010000001100001000000010000001010000100000011010000000110"
EncodedBinary=LempelZivEncodeBinary(BinaryData)
#print(EncodedBinary)


BinaryData='1100010101101010010011001101111001000111'
EncodedBinary=LempelZivEncodeBinary(BinaryData)
print(EncodedBinary)