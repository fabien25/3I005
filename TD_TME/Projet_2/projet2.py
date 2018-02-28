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

#print(dtrain[0])

def n(i,a,liste):
	cpt=0
	for prot in liste :
		if (prot[i]==a):
			cpt=cpt+1
	return cpt

#Q1 - Calcul ni(a) | pour tout i appartenant [0,L-1]
#		   | pour tout a appartenant Alphabet

Alphabet=["A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y","-"]
L=48
liste2=[]
dico={}

#for i in Alphabet:
#	s=i
#	for j in range (L):
#		a=s+str(j)
#		if a not in dico:
#			dico[a]=1
#		else:
#			dico[a]=dico[a]+1
#print (dico)

print (n(0,"-",dtrain))

#def w(i,a,liste):
#	numerateur= n(i,a,liste)+1
#	denominateur= len(liste) + 
