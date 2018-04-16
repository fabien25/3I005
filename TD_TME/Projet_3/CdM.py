# -*- coding: utf-8 -*-
import numpy as np
import pyAgrum as gum
import matplotlib.pyplot as plt
import utils
import functools
from collections import deque


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

  def show_distribution(self, distribution):
    fig, ax = plt.subplots()
    fig.set_size_inches(5, 1.5)
    ax.set_yticks([])
    ax.set_xticklabels(self.get_states())
    lr=[]
    for (k,v) in self.stateToIndex.items():
        lr.append(v)
    ax.set_xticks(lr)
    ax.imshow(self.distribution_to_vector(distribution).reshape(1, len(self.stateToIndex)), cmap=utils.ProbaMap)

######Q8- A REVOIR #######################################
  def get_communication_classes(self):
    lr=[]
    s=set()
    for i in self.get_states():
      dico=self.get_transition_distribution(i)
      boole=0
      for (k,v) in dico.items():
        ##Si il y a un cycle sur lui même
        if ((k==i) and (v==1)):
          boole=1
          lr.append({k})
          break;
      if (boole==0):
        s.add(i)
    lr.append(s)
    return lr

  def get_absorbing_classes(self):
    liste=self.get_communication_classes()
    lr=[]
    for i in liste:
      if (len(i)==1):
        lr.append(i)
    if (len(lr)==0):
      return liste
    else:
      return lr

  # def get_absorbing_classes(self):
  #   graph = self.get_transition_graph()
  #   comm = self.get_communication_classes()                               #comm=[{5}, {6}, {1, 2, 3, 4}]
  #   lr = []
  #   for a in comm:
  #     set1=set()
  #     for node in a:
  #       set1.add(graph.children(node))                                    #On ajoute dans set1 tous les fils du current node en regardant le graph
  #     if (len(set1)==len(a)):                                             #Si il n'y a aucune diff, alors a est absorbant
  #       lr.append(a)
  #   return lr
##########################################################
  def explore(self,graph, node, explore):
    graph2 = graph.children(node)                                           #On recup le sous_graph du current node
    for node2 in graph2:                                                    #On parcourt le sous_graph
      if node2 not in explore:                                              #On ajoute à notre set d'exploration si on rencontre un nouveau noeud
        explore.add(node2)                                                  
        self.explore(graph,node2,explore)                                   #On repete l'opération sur les autres noeuds
    return explore

  def is_irreducible(self):
    states = self.stateToIndex.values()
    graph = self.get_transition_graph()
    for node in states:
      explore=self.explore(graph, node, set([node]))                        #On va voir pour chaque noeud, quel noeud il peut atteindre
      #print(states)
      #print(explore)
      if (len(states)!=len(explore)):                                       #Si la longueur de explore != longueur de tous les états, ce n'est pas irreductible
        return False
    return True

  def explore2(self,graph, node, graph2, explore, period, cpt):
    for node2 in graph2:                                                    #On parcourt le sous_graph de base
      if (node2==node):                                                     #On vient de boucler
        period.add(cpt)
        return period
      if (node2 in explore):                                                #Si on a deja croisé le noeud
        return period
      explore.add(node2)
      self.explore2(graph,node,graph.children(node2),explore,period,cpt+1)  #On parcourt en profondeur l'arbre
    return period

  def get_periodicity(self):
    states = self.stateToIndex.values()
    graph = self.get_transition_graph()
    for node in states:
      graph2 = graph.children(node)
      period = self.explore2(graph, node, graph2, set(), set(), 1)
      #print(period)                                                        #Si period = {1,2,3,4,5}
      pgcd = functools.reduce(utils.pgcd, period)                           #Alors reduce => pgcd(pgcd(pgcd(pgcd(1,2),3),4),5)
    return pgcd

  def is_aperiodic(self):
      states = self.stateToIndex.values()
      graph = self.get_transition_graph()
      for node in states:
        #sous_graphe
        graph2 = graph.children(node)
        period = self.explore2(graph, node ,graph2, set(), set(),1)
        #print(period)                                                      #Si period = {1,2,3,4,5}
        pgcd=functools.reduce(utils.pgcd, period)                           #Alors reduce => pgcd(pgcd(pgcd(pgcd(1,2),3),4),5)
        if pgcd == 1:
          return True
      return False
##########################################################