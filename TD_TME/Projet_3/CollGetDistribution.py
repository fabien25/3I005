# -*- coding: utf-8 -*-

from Collector import Collector
from CdMSampler import CdMSampler
from MouseInMaze import MouseInMaze
from collections import defaultdict
import matplotlib.pyplot as plt
import utils

class CollGetDistribution(Collector):
  def __init__(self,epsilon,pas):
    self.epsilon=epsilon
    self.pas=pas
    self.dico_proba={}
    self.erreur=0
    self.iteration=0
    self.max_iter=0
    self.liste_state=[]

  def initialize(self, cdm, max_iter):
    self.iteration = 0
    self.max_iter = max_iter

    #print("init")

  def receive(self, cdm, iter, state):
    self.liste_state.append(state)
    if (state in self.dico_proba):
      self.dico_proba[state]+=1
    else:
      self.dico_proba[state]=1
    #fig, ax = plt.subplots()
    #fig.set_size_inches(5, 0.5)
    #ax.set_yticks([])
    #ax.set_xticklabels(self.liste_state)
      #lr=[]
    #for (k,v) in self.stateToIndex.items():
        #lr.append(v)
    #ax.set_xticks(lr)
    #ax.set_xticks(lr)
    #ax.imshow(self.liste_state, cmap=utils.ProbaMap)
    #if iter % self.pas == 0:
    #  for (k,v) in self.dico_proba.items():
    #    self.dico_proba[k]=self.dico_proba[k]/(self.max_iter)
    #    if (self.dico_proba[k]<self.epsilon):
    #      return True
    #return False
    #cdm.show_distribution(cdm.get_transition_distribution(state))
  	#if (diff<self.epsilon):
  		#if (self.pas !=0):
  			#Dessin ??

  def finalize(self, cdm, iteration):
    self.iteration = iteration
    print('fin')

  def get_results(self, cdm):
    #print(self.dico_proba)
    #print(self.iteration+1)
    #print(self.max_iter)
    for (k,v) in self.dico_proba.items():
      self.dico_proba[k]=self.dico_proba[k]/(self.iteration+1)
    return {"erreur": self.erreur, "proba":self.dico_proba}