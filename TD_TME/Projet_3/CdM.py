# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum

import utils



class CdM (object):
  """
  Class virtuelle représentant une Chaîne de Markov
  """

  def __init__(self):
    """
    Constructeur. En particulier, initalise le dictionaire stateToIndex

    :warning: doit être appelé en fin de __init__ des classes filles
    avec ` super().__init__()`
    """
    self.state=self.get_states()
    self.stateToIndex=dict()
    j=0
    for i in self.state:
      self.stateToIndex[j]=i
      j=j+1

  def get_states(self):
    """
    :return: un ensemble d'états énumérable (list, n-uple, etc.)
    """
    return self.state

  def get_transition_distribution(self, state):
    """
    :param state: état initial
    :return: un dictionnaire {etat:proba} représentant l'ensemble des états atteignables à partir de state et leurs
    probabilités
    """
    raise NotImplementedError

  def get_initial_distribution(self):
    """
    :return: un dictionnaire représentant la distribution à t=0 {etat:proba}
    """
    raise NotImplementedError


  def __len__(self):
    """
    permet d'utiliser len(CdM) pour avoir le nombre d'état d'un CdM

    :warning: peut être surchargée
    :return: le nombre d'état
    """
    return len(self.get_states())

  def show_transition_matrix(self):
    utils.show_matrix(self.get_transition_matrix())

  def distribution_to_vector(self, state):
    mat=np.zeros(len(self.stateToIndex))
    for j in mat:
      
    return np.array(lr)