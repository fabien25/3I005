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

def apprend_modele(spam,nonspam,intervalle):
    total_intervalle=[]
    total_res=[]
    total=[]
    taille_spam=len(spam)
    taille_nonspam=len(nonspam)
    cpt=0
    while (cpt<=1600):
        nb_spam=0
        nb_non_spam=0
        total_intervalle.append(cpt)
        for i in spam:
            if (cpt<longueur(i)<=cpt+intervalle):
                nb_spam=nb_spam+1
        for i in nonspam:
            if (cpt<longueur(i)<=cpt+intervalle):
                nb_non_spam=nb_non_spam+1
        if (nb_spam>nb_non_spam):
                total_res.append("spam")
        if (nb_spam<nb_non_spam):
                total_res.append("non spam")
        nb_alter=0
        if (nb_spam==nb_non_spam):
            if (nb_alter%2 == 0):
                total_res.append("spam")
            else:
                total_res.append("non spam")
            nb_alter+=1
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
    win_1 = 0
    win_2 = 0
    passe = 0
    not_win_1 =0
    not_win_2 =0
    i=0
    w=0
    while (i < len(liste_mail[0])):
        #Si le nb mot est > 1600
        if (longueur(liste_mail[0][i]) > 1600):
            w=w+1
            i=i+1
        else:
            j=0
            for k in modele[0]:
                if (k>longueur(liste_mail[0][i])):
                    if (modele[1][j]=="spam") and (liste_mail[1][i]=="spam"):
                        win_1 = win_1 + 1
                    if (modele[1][j]=="non spam") and (liste_mail[1][i]=="non spam"):
                        win_2 = win_2 + 1
                    if (modele[1][j]=="spam") and (liste_mail[1][i]=="non spam"):
                        not_win_1= not_win_1 +1
                    if (modele[1][j]=="non spam") and (liste_mail[1][i]=="spam"):
                        not_win_2= not_win_2 +1
                    break
                else:
                    j=j+1
            i=i+1
    print("-------------------------------")
    print("predict|result")
    print("-------------------------------")
    print("win")
    print("spam|spam: ",win_1)
    print("non spam|non spam:",win_2)
    print("-------------------------------")
    print("fail")
    print("spam|non spam: ",not_win_1)
    print("non spam|spam: ",not_win_2)
    print("-------------------------------")
    print("nombre de mail test: ", i)
    print("nombre de mail test ignoré (car nb mot>1600) : ", w)
    return (win_1+win_2)/(i-w)


#in : spam, nospam %
#split spam/nospam in learning and test dataset by % given
#out : accuracy between test and learning dataset
def test (sp,nosp,pourcentage):
    spam=split(sp,pourcentage)
    nospam=split(nosp,pourcentage)
    apprentissage_spam=spam[0]
    apprentissage_nospam=nospam[0]
    test_spam=spam[1]
    test_nospam=nospam[1]
    mail=[]
    label=[]
    liste_test=[]

    #Liste mail/label test
    for i in test_spam:
        mail.append(i)
    for j in test_nospam:
        mail.append(j)
    a=len(test_spam)
    b=len(test_nospam)
    k=0
    l=0
    while k<a:
        label.append("spam")
        k+=1
    while l<b:
        label.append("non spam")
        l+=1
    liste_test.append(mail)
    liste_test.append(label)

    #Apprentissage intervalle
    spam2=[]
    nospam2=[]
    for i in apprentissage_spam:
        spam2.append(i)
    for j in apprentissage_nospam:
        nospam2.append(j)
    modele = apprend_modele(spam2,nospam2,50)

    return accuracy(liste_test,modele)

print(test(spam,nospam,0.5))

#Q2.4 voir code
#tab=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
#tab_res=[]
#for i in tab:
#    tab_res.append(test(spam,nospam,i))
#print (tab_res)

#Renvoie le mot d'indice donné d'un mail
def mot_mail(mail,indice):
    mot=""
    cpt=0
    for i in mail:
        if ((cpt==indice) and (i!=" ")):
            mot=mot+i
        if (i==" "):
            cpt=cpt+1
    return mot

#print (mot_mail(spam[0],0))

#Renvoie un booléen indiquant si un mot est present dans un mail ou non
def mot_present(mail,mot):
    cpt=0
    while (cpt<longueur(mail)):
        mot_courant=mot_mail(mail,cpt)
        if (mot_courant==mot):
            return True
        cpt=cpt+1
    return False

#print(mot_present(spam[0],"Wanna"))

def compte_mot_coll(collection):
    i=0
    tab_mot=[]
    tab_apparition=[]
    tab_total=[]
    for mail in collection:
        mot_courant = mot_mail(mail,i)
        if (mot_courant not in tab_mot):
            tab_mot.append(mot_courant)
            cpt=0
            for mail in collection:
                if (mot_present(mail,mot_courant)):
                    cpt=cpt+1
            tab_apparition.append(cpt)
        i=i+1
    tab_total.append(tab_mot)
    tab_total.append(tab_apparition)
    return tab_total

#print(compte_mot_coll(spam))