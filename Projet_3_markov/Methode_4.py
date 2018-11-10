# -*- coding: utf-8 -*-

from Collector import Collector
from CdMSampler import CdMSampler
from MouseInMaze import MouseInMaze
from collections import defaultdict
import matplotlib.pyplot as plt
import utils
import numpy as np
import math

class Methode_4(Collector):
  def __init__(self,epsilon):
    self.epsilon=epsilon
    self.cpt=1
    self.old_d={}
    self.dico_proba={}
    self.current_d={}
    ##Q14
    self.liste_err=[]
    self.liste_ite=[]

  def initialize(self, cdm, max_iter):
    self.old_d=cdm.get_transition_matrix()

  def receive(self, cdm, iter, state):
    #Initialisation du dico du nombre d'états visités
    if (state in self.dico_proba):
      self.dico_proba[state]+=1
    else:
      self.dico_proba[state]=1
    #Création de la current distrib
    current_d1={}
    for (k,v) in self.dico_proba.items():
      current_d1[k]=v/(iter+1)

    #M^n
    vector_old=self.old_d
    #M^n-1*pi0
    vector_old_2=vector_old*cdm.distribution_to_vector(cdm.get_initial_distribution())
    #M^n
    vector_current_b=self.old_d*cdm.get_transition_matrix()
    #M^n*pi0
    vector_current=vector_current_b*cdm.distribution_to_vector(cdm.get_initial_distribution())

    #print(self.old_d)
    #print(cdm.get_transition_matrix())
    #print(vector_current)

    diff=vector_current-vector_old_2
    error=np.amax(np.abs(np.array(diff)))

    self.liste_err.append(error)
    self.liste_ite.append(iter)
    if (error<self.epsilon):                                ##Si l'erreur est inf au epsilon
          self.error=error
          self.current_d=current_d1
          return True

    self.old_d=vector_current_b
    self.cpt+=1
    return False

  def finalize(self, cdm, iteration):
    plt.scatter(self.liste_ite,self.liste_err)
    plt.ylabel('erreur')
    plt.xlabel('iteration')
    plt.title('Erreur en fonction de l\'itération')
    plt.show()
    
  def get_results(self, cdm):
    return {"Méthode 4 : distribution de la CdM à l'état n":self.current_d}