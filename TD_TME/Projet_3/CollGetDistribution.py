# -*- coding: utf-8 -*-

from Collector import Collector
from CdMSampler import CdMSampler
from MouseInMaze import MouseInMaze
from collections import defaultdict
import matplotlib.pyplot as plt
import utils
import numpy as np

class CollGetDistribution(Collector):
  def __init__(self,epsilon,pas):
    self.epsilon=epsilon
    self.pas=pas
    self.dico_proba={}
    self.old_d={}
    self.error=0

  def initialize(self, cdm, max_iter):
    self.iteration = 0
    #print("init")

  def receive(self, cdm, iter, state):
    self.iteration=iter+1

    #Initialisation du dico du nombre d'états visités
    if (state in self.dico_proba):
      self.dico_proba[state]+=1
    else:
      self.dico_proba[state]=1
    
    #Création de la current distrib
    current_d={}
    for (k,v) in self.dico_proba.items():
      current_d[k]=v/(iter+1)

    #Distrib to vector
    vector_old=cdm.distribution_to_vector(self.old_d)
    vector_current=cdm.distribution_to_vector(current_d)
    diff=vector_current-vector_old                          ##différence avec current_d et old_d
    error=np.amax(np.abs(np.array(diff)))                   ##On stock dans error la valeur max de la diff
    if (error<self.epsilon):                                ##Si l'erreur est inf au epsilon
          self.error=error
          return True                                       ##STOP
    self.old_d=current_d                                    ##Sinon old_d=current_d
    # if(iter%self.pas==0):
    #   cdm.show_distribution(self.old_d)
    return False

  def finalize(self, cdm, iteration):
    pass
    
  def get_results(self, cdm):
    #print(self.dico_proba)
    #print(self.iteration+1)
    #print(self.max_iter)
    return {"erreur": self.error, "proba":self.old_d}