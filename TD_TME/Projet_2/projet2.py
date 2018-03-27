import math
import operator
import matplotlib.pyplot as plt
import numpy as np

###############PART 1#####################
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
testseq2=read("test_seq2.txt")
distance=read("distances.txt")

Alphabet=['A','C','D','E','F','G','H','I','K','L','M','N','P','Q','R','S','T','V','W','Y','-']
L=48
M=len(dtrain)
q=len(Alphabet)

###############PART 2#####################

##############Q1
def matrice(liste):
	return np.array(liste)

#Fonction renvoyant nia
def n(i,a,liste):
	cpt=0
	for prot in liste :
		if (prot[i]==a):
			cpt=cpt+1
	return cpt

#Fonction renvoyant wia
def w(i,a,liste):
	numerateur= n(i,a,liste) + 1.0
	denominateur= len(liste) + q
	return numerateur/denominateur

#Fonction renvoyant la matrice des nombres d'occurence
def n_global(liste):
	liste1=[]
	for a in Alphabet:
		liste2=[]
		i=0
		while (i<48):
			liste2.append(n(i,a,liste))
			i=i+1
		liste1.append(liste2)
	return liste1

#Fonction renvoyant la matrice des poids
def w_global(liste):
	result=0.0
	liste1=[]
	for a in Alphabet:
		liste2=[]
		i=0
		while (i<48):
			liste2.append(w(i,a,liste))
			i=i+1
		liste1.append(liste2)
	return liste1
	
##############Q2
def s(i,liste):
	tmp=0
	log_q=math.log2(q)
	for a in Alphabet:
		tmp+=w(i,a,liste)*math.log2(w(i,a,liste))
	return log_q+tmp

#print(s(0,dtrain))

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

#print(s_global_trie(dtrain))

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

#print(ai(dtrain))
	
x=[]
y=[]
i=0
dico=s_global_dico(dtrain)

while i<48:
	x.append(i)
	y.append(dico[i])
	i+=1

#plt.title("Entropie en fonction de i")
#plt.plot(x, y)
#plt.xlabel('I')
#plt.ylabel('Entropie')
#plt.show()

##############Q3
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

##############Q4
def eq9(lb):
	i=0
	somme=0
	while (i<L-1):
		num=w(i,lb[0][i],dtrain)
		denom=eq8(lb[0][i])
		somme+=math.log2(num/denom)
		i+=1
	return somme

#def eq92(lb):
#	x=eq6(lb)
#	y=eq7(lb)
#	return math.log2(x/y)

#print(eq9(testseq))
#print(eq92(testseq))

def eqq4(L,listetest,listetrain):
	cpt=0
	chaine=""
	listecpt=[]
	listeeq9=[]
	taille=len(listetest[0])
	#print("Attendre que le compteur atteint", taille)
	while (cpt<len(listetest[0])-L):
		#print("ok")
		chaine=listetest[0][cpt:cpt+L]
		print (cpt+L)
		#print (chaine)
		listecpt.append(cpt)
		e9=eq9([chaine])
		if (e9>0):
			print ("log v",e9)
			print("position",cpt)
		listeeq9.append(e9)
		cpt=cpt+1
	return [listecpt,listeeq9]

#print(testseq)
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
	sa=0
	sb=0
	for a in Alphabet:
		for b in Alphabet:
			numerateur=eq11(i,j,a,b,liste)
			denominateur=w(i,a,liste)*w(j,b,liste)
			res=numerateur/denominateur
			somme+=eq11(i,j,a,b,liste)*math.log2(res)
	return somme

print(eq12(0,1,dtrain))
############################################
def liste_to_mat(train):
	mat=np.chararray((len(train), L));
	for i in range(len(train)):
		for j in range(len(train[i])):
			mat[i][j]=train[i][j]
	return mat.astype("U8")

def eq10g(mat):
	dict_nijab={}
	print("Prend ~8min // décommenter le print de la boucle de la fonction eq10g et attendre le print (46 47 - -)")
	for i in range (L):
		for j in range (i+1,L):
			for a in Alphabet:
				for b in Alphabet:
					r1 = (mat[:,i] == a) #[true, true, false, false false][false,true,true...]
					r2 = (mat[:,j] == b) #[true, true, false, false false][true,false...]
					print(i,j,a,b)
					dict_nijab[(a,b,i,j)]= np.logical_and(r1, r2).sum(0)  #[true, true, false, false false]
	return dict_nijab

def eq11g(mat):
	dict_nijab=eq10g(mat)
	dict_wijab={}
	for i in range (L):
		for j in range (i+1,L):
			for a in Alphabet:
				for b in Alphabet:
					numerateur= dict_nijab[(a,b,i,j)] + (1.0/q) 
					denominateur=(1.0* M + q)					
					dict_wijab[(a,b,i,j)]=numerateur/denominateur
	return dict_wijab

def dict_nia(mat):
	dict_nia={}
	for i in range (L):
		for a in Alphabet:
			#print (i,a)
			dict_nia[(i,a)]=n(i,a,dtrain)
	return dict_nia

def dict_wia(mat):
	dictnia=dict_nia(mat)
	dict_wia={}
	for i in range (L):
		for a in Alphabet:
			numerateur = dictnia[(i,a)] + 1.0
			denominateur= M + q
			dict_wia[i,a]=numerateur/denominateur
	return dict_wia

def eq12g(mat):
	dictwia=dict_wia(mat)
	dict_wijab=eq11g(mat)
	matij=[]
	matij=[[-1 for x in range (L)] for y in range(L)]
	for i in range (L):
		for j in range (i+1,L):
			somme=0
			for a in Alphabet:
				for b in Alphabet:
					num=dict_wijab[(a,b,i,j)]
					somme+= num * math.log(num/(dictwia[(i,a)]*dictwia[(j,b)]), 2)
			matij[i][j]=somme
	return matij

def func_4(mat):
	mij=eq12g(mat)
	index = np.argsort(mij)
	liste_retour = []
	liste_b=[]
	step = [0.0] * 5
	resultat = [0.0] * 5
	for i in range(L-1):
		for j in range(i+1, L):
			liste_b.append((i, j))
	for i in range(50):
			liste_retour.append(liste_b[index[0][len(mij[0])-1-i]])
	#Calcul de la fraction des paires qui sont des contacts
	for i in range(len(step)):
		step[i] = (len(liste_retour)/10) + (len(liste_retour)/10)*i
	for i in range(len(step)):
		res = liste_retour[0:int(step[i])]
		for j in range(len(res)):
			index = liste_b.index((int(res[j][0]), int(res[j][1])))
			#si la distance est plus petit que 8
			if float(distance[index][2]) < 8.0:
				resultat[i] = resultat[i] + 1.0
		resultat[i] = resultat[i] / step[i]
	#Affichage du graph
	plt.title("Fraction en fonction du nombre de paires considerées")
	plt.xlabel("Nb paires considerées")
	plt.ylabel("Fraction")
	plt.xticks(np.arange(10), step)
	plt.plot(resultat)
	plt.show()

############################################
##Test de la partie III##
##Prend du temps ~4/5min##
#mat_dtrain=liste_to_mat(dtrain)
#print(distance)
#mat12=eq12g(mat_dtrain)
#print (mat12[0][1]) #affiche bien 0.404
#dic10=eq10g(mat_dtrain)
#print(dic10[('R','F',0,3)]) #affiche 193
#print (eq10(0,3,'R','F',dtrain)) #affiche bien 193
#func_4(mat_dtrain) #plot graph Q4
############################################