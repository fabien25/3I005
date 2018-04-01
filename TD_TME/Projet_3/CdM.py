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
      self.stateToIndex[i]=j
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
    for (k,v) in state.items():
      mat[self.stateToIndex[k]]=v
    return mat

  def vector_to_distribution(self,vector):
    dico={}
    j=0
    for (k,v) in self.stateToIndex.items():
      if (vector[v]!=0):
          dico[k]=vector[v]
    return dico

  def show_distribution(self,state):
    lr=[]
    for (k,v) in self.stateToIndex.items():
      lr.append(0)
    for (k,v) in state.items():
      lr[self.stateToIndex[k]]=v
    return lr

  def get_transition_matrix(self):
    lr=[]
    for k in self.stateToIndex.keys():
      lr.append(self.distribution_to_vector(self.get_transition_distribution(k)).tolist());
    return np.array(lr)

  def get_transition_graph(self):
    #créer un graph orienté
    g=gum.DiGraph()
    mat=self.get_transition_matrix()
    for liste in mat:
      g.addNode()
    current_node=0
    for liste in mat:
      i=0
      while (i<len(liste)):
        if (liste[i]!=0):
          g.addArc(current_node,i)
        i=i+1
      current_node+=1
    return g

  def show_transition_graph(self,gnb):

    #Grossomodo on reconstruit la string digraph {...}
    s="digraph{"
    
    #Labels des nodes
    for (k,v) in self.stateToIndex.items():
      s+=""+str(v)+" "+"[label=\""+"["+str(v)+"]"+" "+str(k)+"\"];"
    
    #Labels des arcs (on reprend plus ou moin le meme code que get_transition_graph...)
    mat=self.get_transition_matrix()
    current_node=0
    for liste in mat:
      i=0
      while (i<len(liste)):
        if (liste[i]!=0):
          s+=""+str(current_node)+"->"+str(i)+"[label="+str(liste[i])+"];"
        i=i+1
      current_node+=1
    s+="}"
    gnb.showDot(s)