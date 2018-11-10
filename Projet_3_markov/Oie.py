# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
from CdM import CdM
import utils
import random

class Oie(CdM):
  """
  Class virtuelle représentant une Chaîne de Markov
  """

  def __init__(self,N,p,q,d):
    """
    Constructeur.
    """
    self.N=N #Nb cases
    self.p=p #Tremplin ou glissade
    self.q=q #Puit
    self.d=d #Dé
    self.plateau=self.genere_plateau()
    super(Oie, self).__init__()

  def genere_plateau(self):
    """
    :return: un ensemble d'états énumérable (list, n-uple, etc.)
    """
    lr=[]
    i=1
    while (i<self.N+1):
        #print("valeur de i", i)
        #Seulement 1 case sur 10 (en moyenne) est piègée.
        tirage=random.randint(1, 10)/10.0
        if ((tirage==0.1) and (i!=1) and (i!=self.N)):
            tirage2=random.randint(1, 10)/10.0
            #Probabilité p qu'une case soit un puit
            if (tirage2<=self.q):
                lr.append(0)
            #Probabilité p qu'une case soit une glissade ou un tremplin
            else:
                tirage3=random.randint(1,10)/10.0
                #Glissade
                if (tirage3<=0.5):
                    #print("glissade")
                    case_back=random.randint(1,i-1)
                    lr.append(case_back)
                #Tremplin
                if (tirage3>0.5):
                    #print("tremplin")
                    case_forward=random.randint(i+1,self.N)
                    lr.append(case_forward)
        else:
            lr.append(i)
        i=i+1
    #print(lr)
    return lr

  def get_states(self):
    """
    :return: un ensemble d'états énumérable (list, n-uple, etc.)
    """
    lr=[]
    cpt=1
    while cpt<=len(self.plateau):
        lr.append(cpt)
        cpt=cpt+1
    # lr=[]
    # for i in self.plateau:
    #     if i not in lr:
    #         lr.append(i)
    # return lr
    return lr

  def get_transition_distribution(self, state):
    """
    :param state: état initial
    :return: un dictionnaire {etat:proba} représentant l'ensemble des états atteignables à partir de state et leurs
    probabilités
    """ 
    dice=1
    dico=dict()
    while (dice<self.d+1):
        position_after_dice=state+dice
        #le joueur rebondit sur la case nn si le tirage du dé lui fait dépasser la case n.
        if (position_after_dice>self.N):
            position_after_dice=self.N
        futur_case=self.plateau[position_after_dice-1]
        if (futur_case in dico):
            dico[futur_case]+=(1/self.d)
        else:
            dico[futur_case]=(1/self.d)
        dice+=1
    return dico

  def get_initial_distribution(self):
    """
    :return: un dictionnaire représentant la distribution à t=0 {etat:proba}
    """
    return {1:1}


  def __len__(self):
    """
    permet d'utiliser len(CdM) pour avoir le nombre d'état d'un CdM

    :warning: peut être surchargée
    :return: le nombre d'état
    """
    return len(self.get_states())

  def show_transition_matrix(self):
    utils.show_matrix(self.get_transition_matrix())