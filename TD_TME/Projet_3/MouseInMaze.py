# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum

import utils

class MouseInMaze:
  """
  Class virtuelle représentant une Chaîne de Markov
  """

  def __init__(self):
    """
    Constructeur. En particulier, initalise le dictionaire stateToIndex
    """
    self.state=2

  def get_states(self):
    """
    :return: un ensemble d'états énumérable (list, n-uple, etc.)
    """
    return [1,2,3,4,5,6]

  def get_transition_distribution(self, state):
    """
    :param state: état initial
    :return: un dictionnaire {etat:proba} représentant l'ensemble des états atteignables à partir de state et leurs
    probabilités
    """
    if (self.state==1):
    	return {'1 vers 1':0.5, '1 vers 2': 0.5}
    if (self.state==2):
    	return {'2 vers 1':0.5, '2 vers 4': 0.5}
    if (self.state==3):
    	return {'3 vers 5':0.25, '3 vers 6': 0.25, '3 vers 1':0.25, '3 vers 2': 0.25}
    if (self.state==4):
    	return {'4 vers 3':1}
    if (self.state==5):
    	return {'5 vers 5':1}
    if (self.state==6):
    	return {'6 vers 6':1}
    else:
    	raise IndexError

  def get_initial_distribution(self):
    """
    :return: un dictionnaire représentant la distribution à t=0 {etat:proba}
    """
    return {'2 vers 1':0.5, '2 vers 4': 0.5}


  def __len__(self):
    """
    permet d'utiliser len(CdM) pour avoir le nombre d'état d'un CdM

    :warning: peut être surchargée
    :return: le nombre d'état
    """
    return len(self.get_states())

  def show_transition_matrix(self):
    utils.show_matrix(self.get_transition_matrix())