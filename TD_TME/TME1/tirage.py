# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 15:59:19 2018

@author: 3408748
"""

import random
import matplotlib.pyplot as plt
#carte = (num (1-13),coul(c,k,p,t))

c = (1,"c")


#random.randint(low, high)


def paquet ():
    l=[]  
    cpt=1
    while (cpt<=13):
        c1=(cpt,"C")
        c2=(cpt,"K")
        c3=(cpt,"P")
        c4=(cpt,"T")
        l.append(c1)
        l.append(c2)
        l.append(c3)
        l.append(c4)
        cpt=cpt+1
    random.shuffle(l)
    return l

def meme_position (p,q):
    l=[]
    cpt=0
    for i in p:        
        if (i==q[cpt]):
            l.append(cpt)
        cpt=cpt+1
    return l
    
c1=paquet()
c2=paquet()

#print (c1)
#print (c2)
#print (meme_position(c1,c2))

def moyenne_meme_position(iteration):
    cpt=0
    somme=0
    while (cpt<iteration):
        c1=paquet()
        c2=paquet()
        cpt=cpt+1
        l=meme_position(c1,c2)
        somme=somme+len(l)
    return float(somme)/cpt

print (moyenne_meme_position(10))

l=[]
e=[]
cpt=1
while cpt<100:
    l.append(moyenne_meme_position(cpt))    
    e.append(cpt)
    cpt=cpt+1    

plt.plot(e,l)
plt.ylabel('Nb positions communes')
plt.xlabel('Iterrations')
plt.show()

