# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 00:49:00 2022

@author: Xander
"""
import numpy as np

class Node:
    upper=None
    bottom=None
    content=""
    probability=0
    def __init__(self,content="",prob=0,bottomnode=None,uppernode=None):
        self.bottom=bottomnode
        self.upper=uppernode
        self.content=content
        self.probability=prob
        if (not bottomnode is None):
            self.content=bottomnode.content+uppernode.content
            self.probability=bottomnode.probability+uppernode.probability

def HuffmanCodes(Chars,CharProbabilities):
    """@brief: Creates a Huffman tree from a list of characters and their probabilities.
    @param Chars: A list of characters to be encoded.
    @param CharProbabilities: A list of probabilities for each character.
    @return: The top node of the Huffman tree."""
    nodelist=[]
    topnode=None
    for x in range(0,len(Chars)):
        nodelist.append(Node(Chars[x],CharProbabilities[x]))
    while len(nodelist)>1:
        minindex=0
        for x in range(0,len(nodelist)):
            if (nodelist[x].probability<nodelist[minindex].probability):
                minindex=x
        bottomnode=nodelist.pop(minindex)
        
        minindex=0
        for x in range(0,len(nodelist)):
            if (nodelist[x].probability<nodelist[minindex].probability):
                minindex=x
        uppernode=nodelist.pop(minindex)
        
        topnode=Node("",0,bottomnode,uppernode)
        nodelist.append(topnode)
    return topnode
def HuffmanEncode(topnode,char):
    """@brief: Encodes a character using a Huffman tree.
    @param topnode: The top node of the Huffman tree.
    @param char: The character to be encoded.
    @return: The encoded character."""
    returnval=""
    if char not in topnode.content:
        return None
    while len(topnode.content)>1:
        if (char in topnode.upper.content):
            returnval+="0"
            topnode=topnode.upper
        else:
            returnval+="1"
            topnode=topnode.bottom
    return returnval

#Example

chars=['a','b','c','d','e','f']#X1,X2,X3,X4,X5,X6
probs=[0.35,0.22,0.18,0.11,0.09,0.05]
huffman=HuffmanCodes(chars,probs)
for char in chars:
    print(HuffmanEncode(huffman,char))
    
        
