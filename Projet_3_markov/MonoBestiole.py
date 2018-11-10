# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
from CdM import CdM
import utils
import matplotlib.pyplot as plt

class MonoBestiole(CdM):
  """
  Class virtuelle représentant une Chaîne de Markov
  """

  def __init__(self,N,p,q):
    """
    Constructeur. En particulier, initalise le dictionaire stateToIndex
    """
    self.N=N
    self.p=p
    self.q=q
    super(MonoBestiole, self).__init__()    

  def get_states(self):
    """
    :return: un ensemble d'états énumérable (list, n-uple, etc.)
    """
    lr=[]
    i=1
    while (i<self.N+1):
        lr.append(i)
        i=i+1
    return lr

  def get_transition_distribution(self, state):
    """
    :param state: état initial
    :return: un dictionnaire {etat:proba} représentant l'ensemble des états atteignables à partir de state et leurs
    probabilités
    """
    if (state==1):
        return {1:self.q, 2: self.p}
    elif (state==self.N):
        return {self.N-1:self.q, self.N: self.p}
    else:
        return {state-1:self.q,state+1:self.p}
    	#raise IndexError

  def get_initial_distribution(self):
    """
    :return: un dictionnaire représentant la distribution à t=0 {etat:proba}
    """
    return self.get_transition_distribution(1)


  def __len__(self):
    """
    permet d'utiliser len(CdM) pour avoir le nombre d'état d'un CdM

    :warning: peut être surchargée
    :return: le nombre d'état
    """
    return len(self.get_states())

  def show_transition_matrix(self):
    """
    permet d'afficher la matrice de transition
    """
    utils.show_matrix(self.get_transition_matrix())

  def show_distribution(self, distribution):
    """
    permet d'afficher la distribution passé en paramètre
    """
    fig, ax = plt.subplots()
    fig.set_size_inches(5, 1.5)
    ax.set_yticks([])
    ax.set_xticklabels(self.get_states())
    lr=[]
    for (k,v) in self.stateToIndex.items():
        lr.append(v)
    ax.set_xticks(lr)
    ax.imshow(self.distribution_to_vector(distribution).reshape(1, len(self.stateToIndex)), cmap=utils.ProbaMap)