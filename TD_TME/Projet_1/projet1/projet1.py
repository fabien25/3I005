import email
import re

def read_file(fname):
    """ Lit un fichier compose d'une liste de emails, chacun separe par au moins 2 lignes vides."""
    f = open(fname,'rb')
    raw_file = f.read()
    f.close()
    raw_file = raw_file.replace(b'\r\n',b'\n')
    emails =raw_file.split(b"\n\n\nFrom")
    emails = [emails[0]]+ [b"From"+x for x in emails[1:] ]
    return emails

def get_body(em):
    """ Recupere le corps principal de l'email """
    body = em.get_payload()
    if type(body) == list:
        body = body[0].get_payload()
    try:
        res = str(body)
    except Exception:
        res=""
    return res

def clean_body(s):
    """ Enleve toutes les balises html et tous les caracteres qui ne sont pas des lettres """
    patbal = re.compile('<.*?>',flags = re.S)
    patspace = re.compile('\W+',flags = re.S)
    return re.sub(patspace,' ',re.sub(patbal,'',s))

def get_emails_from_file(f):
    mails = read_file(f)
    return [ s for s in [clean_body(get_body(email.message_from_bytes(x))) for x in mails] if s !=""]

spam = get_emails_from_file("spam.txt" )
nospam = get_emails_from_file("nospam.txt")

def split (liste,x):
    lr1=[]
    lr2=[]
    lr3=[]
    nb=len(liste)*x
    cpt=0
    for i in liste :
        if (cpt<nb):
            lr1.append(i)
            cpt=cpt+1
        else:
            lr2.append(i)
    lr3.append(lr1)
    lr3.append(lr2)
    #return lr2,lr3
    #lr1,lr2=split(liste,x)
    return lr3

#print(split(spam,0.01))
#print(spam[0]) #premier mail

def longueur(mail):
    cpt=0
    for i in mail:
        if (i==" "):
            cpt=cpt+1
    return cpt+1

#print (longueur(spam[0]))


##histogramme
import matplotlib.pyplot as plt
data=[]
data2=[]
for i in spam:
    data.append(longueur(i))
    #print (longueur(i))

#plt.hist(data)
#plt.show()

#print (spam[0])

def apprend_modele(spam,nonspam):
    total_intervalle=[]
    total_res=[]
    total=[]
    taille_spam=len(spam)
    taille_nonspam=len(nonspam)
    intervalle=50
    cpt=0
    while (cpt!=1600):
        nb_spam=0
        nb_non_spam=0
        total_intervalle.append(cpt)
        for i in spam:
            if (cpt<longueur(i)<=cpt+intervalle):
                nb_spam=nb_spam+1
        for i in nonspam:
            if (cpt<longueur(i)<=cpt+intervalle):
                nb_non_spam=nb_non_spam+1
        if (nb_spam>=nb_non_spam):
                total_res.append("spam")
        else:
                total_res.append("non spam")
        cpt=cpt+intervalle
    total.append(total_intervalle)
    total.append(total_res)
    return total



def predit_mail (emails,modele):
	nb_mots=longueur(emails)
	cpt=0
	a=0
	for i in modele[0]:
		if (i==nb_mots):
			a=cpt	
		cpt=cpt+1
	return modele[1][a]

#print(predit_mail(spam[0],modele1))


#liste_mail = [  [mail]   [spam/non spam] ]
#modele = [ [0 , 50 , 100]  [spam/non spam] ]

def accuracy (liste_mail,modele):
	win = 0
	not_win_1 =0
	not_win_2 =0
	cpt=0
	for i in liste_mail[0]:
		taille=longueur(i)
		j=0
		if (taille > 1550):
			taille=1550
		while (modele[0][j]<taille):
			j=j+1
		#j-1
		#Si la prédiction est bonne
		if (modele[1][j-1]==liste_mail[1][cpt]):
			win = win + 1
		if (modele[1][j-1]=="spam") and (liste_mail[1][cpt]=="non spam"):
			print("ok")
			not_win_1= not_win_1 +1
		if (modele[1][j-1]=="non spam") and (liste_mail[1][cpt]=="spam"):
			not_win_2= not_win_2 +1
		cpt = cpt+1
	print(not_win_1/cpt)
	print(not_win_2/cpt)
	return win/cpt



#faire varier le pourcentage d'exemples
spam1=split(spam,0.5)
apprentissage_spam = spam1[0]
test_spam = spam1[1]

#faire varier le pourcentage d'exemples
nospam1=split(nospam,0.5)
apprentissage_nospam=nospam1[0]
test_nospam =nospam1[1]

mail1=[]

for i in test_spam:
	mail1.append(i)

for j in test_nospam:
	mail1.append(j)
label1=[]

cpt=0

while (cpt <len(test_spam)):
	label1.append("spam")
	cpt=cpt+1

cpt=0
while (cpt <len(test_nospam)):
	label1.append("no spam")
	cpt=cpt+1



liste_mail1=[]
liste_mail1.append(mail1)
liste_mail1.append(label1)

spam2=[]
nospam2=[]

for i in apprentissage_spam:
	spam2.append(i)

for j in apprentissage_nospam:
	nospam2.append(j)

modele1 = apprend_modele(spam2,nospam2)

print(accuracy(liste_mail1,modele1))












