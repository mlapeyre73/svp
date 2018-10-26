import sys
import re

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


def generalize_id_item(a):
    return a

# arrondi a 1/10 de l'ecart type   teta=77
# c'est vraiment pas bien faudra plutot  faire du bruit
def generalize_price(a):
    a = float(a)
    b = float(7*round(a/7)+1)
    b=str(b)
    return b

# generalise a 1/10 de l'ecart type   teta=45
def generalize_qty(a):
    a = float(a)
    b = str(4*round(a/4)+1)
    return b


def generalize(pathfile) :
    """
    print(generalize_date("2011/01/31"))
    print(generalize_date("2011/03/30"))
    print(generalize_date("2011/02/29"))
    print(generalize_date("2011/02/28"))
    print(generalize_date("2011/02/27"))
    exit(0)
    """

    infile =  pathfile
    print ("Input file name: %s" % infile)
    outfile = re.sub("\.","_generalized_date_hours_price_qty.",infile)
    print ("Output file name: %s" % outfile)

    out = open(outfile,'w')


    i=0

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
                    r[ix] = generalize_id_item(a)
                elif(ix==4): # price
                    r[ix] = generalize_price(a)
                elif(ix==5): # date
                    r[ix] = generalize_qty(a)
                else:
                    r[ix]  =a










        #out.write(["%s," % item  for item in r])
        out.write(",".join(r))
        out.write("\n")
    out.close()
    print("done!")
