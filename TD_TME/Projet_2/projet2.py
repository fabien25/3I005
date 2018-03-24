import math
import operator
import matplotlib.pyplot as plt
import numpy as np

def read(monfichier):
	read = open(monfichier, "r")
	i = 0
	tab=[]	
	while (read.readline()):
		a = read.readline()
		tab.append(a[:-1])
	read.close()
	return tab

dtrain=read("Dtrain.txt")
testseq=read("test_seq.txt")
distance=read("distances.txt")

#print(dtrain[0])
#print(testseq[0])

#Fonction renvoyant nia
def n(i,a,liste):
	cpt=0
	for prot in liste :
		if (prot[i]==a):
			cpt=cpt+1
	return cpt

#print (n(46,"A",dtrain))

#Q1 - Calcul ni(a) | pour tout i appartenant [0,L-1]
#		   | pour tout a appartenant Alphabet

Alphabet=["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y","-"]
L=48
q=len(Alphabet)

#Fonction renvoyant la matrice
def matrice(liste):
	liste1=[]
	for a in Alphabet:
		liste2=[]
		i=0
		while (i<48):
			liste2.append(n(i,a,liste))
			i=i+1
		liste1.append(liste2)
	return liste1

matrice_dtrain=matrice(dtrain)

#print(matrice_dtrain)

#Fonction renvoyant wia
def w(i,a,liste):
	numerateur= n(i,a,liste) + 1.0
	denominateur= len(liste) + q
	return numerateur/denominateur

print(w(0,"-",dtrain))

#Fonction renvoyant la matrice des poids
def w_global(dtrain):
	result=0.0
	liste1=[]
	for a in Alphabet:
		liste2=[]
		i=0
		while (i<48):
			liste2.append(w(i,a,dtrain))
			i=i+1
		liste1.append(liste2)
	return liste1

#print(w_global(dtrain))

def s(i,liste):
	tmp=0
	log_q=math.log2(q)
	for a in Alphabet:
		tmp+=w(i,a,liste)*math.log2(w(i,a,liste))
	return log_q+tmp

print(s(0,dtrain))

def s_global_trie (liste):
	i=0
	dico={}
	while (i<48):
		dico[i]=s(i,liste)
		i+=1
	mondico=dico.items()
	sorted_x = sorted(mondico, key=operator.itemgetter(1),reverse=True)
	lr=[sorted_x[0],sorted_x[1],sorted_x[2]]
	return lr

print(s_global_trie(dtrain))

def s_global_dico (liste):
	i=0
	dico={}
	while (i<48):
		dico[i]=s(i,liste)
		i+=1
	return dico

def ai(liste):
	lis=s_global_trie(liste)
	a=lis[0][0]
	a2=lis[1][0]
	a3=lis[2][0]
	lr=[a,a2,a3]
	acide1=""
	nb=0
	liste2=[]
	for j in lr:
		maximum=0
		for acide in Alphabet:
			nb=n(j,acide,liste)
			if (nb>maximum):
				maximum=nb
				acide1=acide
		liste2.append(acide1)
	return liste2

print(ai(dtrain))
	
x=[]
y=[]
i=0
dico=s_global_dico(dtrain)

while i<48:
	x.append(i)
	y.append(dico[i])
	i+=1

#plt.title("I en fonction de entropie")
#plt.plot(x, y)
#plt.xlabel('I')
#plt.ylabel('Entropie')
#plt.show()

def eq6(lb):
	sp=1
	i=0
	while (i<L-1):
		sp=sp*w(i,lb[0][i],dtrain)
		i+=1
	return sp

def eq8(b):
	i=0
	somme=0
	while (i<L-1):
		somme+=w(i,b,dtrain)
		i+=1
	return (1.0/L)*somme

def eq7(lb):
	sp=1
	i=0
	while (i<L-1):
		sp=sp*eq8(lb[0][i])
		i+=1
	return sp

def eq91(lb):
	i=0
	somme=0
	while (i<L-1):
		num=w(i,lb[0][i],dtrain)
		denom=eq8(lb[0][i])
		somme+=math.log2(num/denom)
		i+=1
	return somme

def eq92(lb):
	x=eq6(lb)
	y=eq7(lb)
	return math.log2(x/y)

print(eq91(testseq))
#print(eq92(testseq))

def eqq4(L,listetest,listetrain):
	cpt=0
	chaine=""
	listecpt=[]
	listeeq91=[]
	print(len(listetest[0]))
	while (cpt<len(listetest[0])-L):
		#print("ok")
		chaine=listetest[0][cpt:cpt+L]
		print (cpt+L)
		#print (chaine)
		listecpt.append(cpt)
		listeeq91.append(eq91([chaine]))
		cpt=cpt+1
	return [listecpt,listeeq91]

#a=eqq4(48,testseq,dtrain)

#x=a[0]
#y=a[1]

#print (x)
#print (y)

#plt.title("log-vraisemblance en fonction de sa premiere position i ")
#plt.plot(x, y)
#plt.xlabel('I')
#plt.ylabel('log-vraisemblance')
#plt.show()

###############PART 3#####################
def eq10 (i,j,a,b,liste):
	cpt=0
	for prot in liste :
		if ((prot[i]==a) and (prot[j]==b)):
			cpt=cpt+1
	return cpt

def eq11 (i,j,a,b,liste):
	numerateur= eq10(i,j,a,b,liste) + (1.0/q)
	denominateur= len(liste) + q
	return numerateur/denominateur

def eq12 (i,j,liste):
	somme=0.0
	for a in Alphabet:
		for b in Alphabet:
			numerateur=eq11(i,j,a,b,liste)
			denominateur=w(i,a,liste)*w(j,b,liste)
			res=numerateur/denominateur
			somme+=eq11(i,j,a,b,liste)*math.log2(res)
	return somme


print (eq12(0,1,dtrain))
#print (distance[0]) 

############################################


def eq11v2(z,liste):
	numerateur= z + (1.0/q)
	denominateur= len(liste) + q
	return numerateur/denominateur

def eq12v2 (z,liste,a,b,i,j):
	somme=0.0
	numerateur=z
	denominateur=w(i,a,liste)*w(j,b,liste)
	res=numerateur/denominateur
	somme+=z*math.log2(res)
	return somme

def Q2_Q3(liste):
	liste_nb_occu=[]
	liste_poid=[]
	liste_mij=[]

	liste2=[]
	liste3=[]
	liste4=[]
	for a in Alphabet:
		for b in Alphabet:
			i=1
			while (i<L):
				j=i+1
				while (j<L):
					print(a,b,i,j)
					nijab=eq10(i,j,a,b,liste)
					wijab=eq11v2(nijab,liste)
					liste2.append(nijab)
					liste3.append(wijab)
					liste4.append(eq12v2(wijab,liste,a,b,i,j))
					j=j+1
				i=i+1
		liste_nb_occu.append(liste2)   #Q2
		liste_poid.append(liste3)	   #Q2
		liste_mij.append(liste4)	   #Q3
	return (liste_nb_occu,liste_poid,liste_mij)

print (Q2_Q3(dtrain))

def Trier():
	dm={}
	for i in range (48):
		print(i)
		for j in range (i+1,48):
			print(j)
			clef=str(i)+"/"+str(j)
			dm[clef]=eq12(i,j,dtrain)
	return dm