import sys
import re
import numpy
import pickle
import os

const_average_price=3.503359
const_ecart_type_price=77.519
const_average_qty=12.021
const_ecart_type_qty=46.321

"""
continent = {"United-States" : "AM", "Cambodia" : "AS", "England" : "EU", "Puerto-Rico" : "AM", "Canada" : "AM", "Germany" : "EU", "Outlying-US(Guam-USVI-etc)":"AM", "India":"AS", "Japan":"AS", "Greece" : "EU", "South":"AM", "China":"AS", "Cuba":"AM", "Iran":"AS", "Honduras":"AM", "Philippines":"OC", "Italy":"EU", "Poland":"EU", "Jamaica":"AM", "Vietnam":"AS", "Mexico":"AM", "Portugal":"EU", "Ireland":"EU", "France":"EU", "Dominican-Republic":"AM", "Laos":"AS", "Ecuador":"AM", "Taiwan":"AS", "Haiti":"AM", "Columbia":"AM", "Hungary":"EU", "Guatemala":"AM", "Nicaragua":"AM", "Scotland":"EU", "Thailand":"AS", "Yugoslavia":"EU", "El-Salvador":"AM", "Trinadad&Tobago":"AM", "Peru":"AM", "Hong":"AS", "Holand-Netherlands":"EU","?":"?"}



def generalize_country(c):
    d=c
    try :
        d = continent[c]
    except KeyError:
        d = "Other"
    #print "generalizing country: %s -> %s" % (c,d)

    return d
"""


"""
fonction de generalisation
"""
def generalize_id_user(a):
    a="".join(["L",a,"D"])

    return a

# generalise a la semaine
def generalize_date(a):

    date=a.split("/")
    if(int(date[2])!=28):

        date[2]=int(date[2])-int(date[2])%7+1
        date[2]='{0:02}'.format(date[2])
        date[2]=str(date[2])

    a="/".join(date)
    return a

# generalise a l'heure
def generalize_hours(a):
    hours=a.split(":")
    a=":".join([hours[0],"00"])
    return a


def generalize_id_item(a,dico_id_item_tronc):
    letters = list(a)
    first_digit=letters[0:2]
    first_digit="".join(first_digit)
    # try si le dernier char est un int
    a=dico_id_item_tronc[first_digit]
    return a


def generalize_price(a):
    a = float(a)
    if a < const_average_price + const_ecart_type_price :
        b=float(round(a))
    else :
        b = float(50*round(a/50))
    b=str(b)
    return b

def generalize_qty(a):
    a = float(a)
    if a < const_average_qty + const_ecart_type_qty :
        b=int(3*round(a/3)+1)
    else :
        b = int(25*round(a/25))
    b = str(b)
    return b

"""
fonction de bruit
"""
# probleme de mauvaise valeurs font planter l'algo de metric.py


def differential_privacy_price(a):
    a = float(a)
    noise=numpy.random.laplace(0,const_ecart_type_price/4)
    if a +noise > 0 :
        a+=noise
    a= str(a)
    return a

def differential_privacy_qty(a):
    a = float(a)
    noise=numpy.random.laplace(0,const_ecart_type_qty/4)
    if a +noise > 0 :
        a+=noise
    a= str(int(round(a)))
    return a





def generalize(pathfile) :
    # permet de recuperer item qui ne sont pas bcp vendu
    # sert pour generalisation_item
    list_item=[]
    list_out=open("info_list_id_item.txt","r+")
    for l in list_out :
        l=l.split("\n")
        list_item.append(l[0])


    infile =  pathfile
    print ("Input file name: %s" % infile)
    outfile = re.sub("\.","ground_truth_new_generalized_date_hours_id_item_twoFirstDigits_price_qty.",infile)
    print ("Output file name: %s" % outfile)

    out = open(outfile,'w')


    i=0

    file=open(os.path.expanduser("id_item_two_first_digit.p"),"rb")
    dico_id_item_tronc=pickle.load(file)

    for l in open(infile, "r").readlines():
        r_ = l.replace('\r', '').replace('\n', '').replace(', ', ',').split(',')

        r = [""] *  len(r_)
        for ix, a in enumerate(r_):
            if i<6 :
                r[ix] = a
                print("premiere boucle")
                i=i+1
            else :
                if(ix==0): #id_user
                    r[ix] = generalize_id_user(a)
                elif(ix==1): # date
                    r[ix] = generalize_date(a)
                elif(ix==2): # hours
                    r[ix] = generalize_hours(a)
                elif(ix==3): # id_item
                    r[ix] = generalize_id_item(a,dico_id_item_tronc)
                    r[ix]  =a

                elif(ix==4): # price
                    r[ix] = generalize_price(a)
                    # r[ix] = differential_privacy_price(a)

                elif(ix==5): # date
                    # r[ix] = differential_privacy_qty(a)
                    r[ix] = generalize_qty(a)
                    # r[ix]  =a
                else:
                    r[ix]  =a










        #out.write(["%s," % item  for item in r])
        out.write(",".join(r))
        out.write("\n")
    out.close()
    print("done!")
