import math
import operator
import matplotlib.pyplot as plt

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
N=114
q=len(Alphabet)

#Fonction renvoyant la matrice
def matrice(dtrain):
	liste1=[]
	for a in Alphabet:
		liste2=[]
		i=0
		while (i<48):
			liste2.append(n(i,a,dtrain))
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

plt.title("I en fonction de entropie")
plt.plot(x, y)
plt.xlabel('I')
plt.ylabel('Entropie')
#plt.show()

def f0(b):
	i=0
	somme=0
	while (i<L-1):
		somme+=w(i,b,dtrain)
		i+=1
	return (1.0/L)*somme

def l(b):
	i=0
	somme=0
	while (i<L-1):
		num=w(i,b[0][i],dtrain)
		denom=f0(b[0][i])
		somme+=math.log2(num/denom)
		i+=1
	return somme

print(l(testseq))


x=[]
y=[]
i=0

while i<N-L:
	x.append(i)
	j=i
	testseq2=[]
	chaine=""
	while (j<N-L):
		chaine+=testseq[0][j]
		j+=1
	testseq2.append(chaine)
	print (testseq2)
	y.append(l(testseq2))
	i+=1

plt.title("log-vraisemblance en fonction de sa premiere position i ")
plt.plot(x, y)
plt.xlabel('I')
plt.ylabel('log-vraisemblance')
plt.show()