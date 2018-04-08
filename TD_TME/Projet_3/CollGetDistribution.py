# -*- coding: utf-8 -*-

from Collector import Collector
from CdMSampler import CdMSampler
from MouseInMaze import MouseInMaze
from collections import defaultdict

class CollGetDistribution(Collector):
  def __init__(self,epsilon,pas):
  	self.epsilon=epsilon
  	self.pas=pas
  	self.dico_proba={}
  	self.dico_state=defaultdict(int)

  def initialize(self, cdm, max_iter):
  	self.counter = 0

  def receive(self, cdm, iter, state):
  	self.dico_state[state]+=1
  	self.counter += 1
  	#diff = ??
  	if (diff<self.epsilon):
  		if (self.pas !=0):
  			#Dessin ??
  			cdm.show_distribution(cdm.get_transition_distribution(state))
  		return true;
  	return false;

  def finalize(self, cdm, iteration):
  	print('fin')

  def get_results(self, cdm):
  	return {"erreur": self.erreur, "nbr_iterations":self.counter,"proba":self.dico_proba}