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

print (longueur(spam[0]))


##histogramme
import matplotlib.pyplot as plt
data=[]
data2=[]
for i in spam:
    data.append(longueur(i))
    #print (longueur(i))

#plt.hist(data)
#plt.show()

def apprend_modele(spam,nonspam):
    total=[]
    spam=[]
    non_spam=[]
    nb_spam=0
    nb_non_spam=0
    nb_spam_total=len(spam)
    nb_non_spam_total=len(nonspam)
    intervalle=50
    cpt=0
    while (cpt!=1600):
        nb_spam=0
        nb_non_spam=0

        for i in spam:
            if (cpt<=longueur(spam[i])<=cpt+50):
                nb_spam=nb_spam+1
            spam.append(nb_spam/nb_spam_total+nb_non_spam_total)

        for i in nonspam:
            if (cpt<=longueur(nonspam[i])<=cpt+50):
                nb_non_spam=nb_non_spam+1
            non_spam.append(nb_non_spam/nb_spam_total+nb_non_spam_total)

        cpt=cpt+50
    total.append(spam)
    total.append(non_spam)
    return total

