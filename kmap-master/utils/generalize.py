import sys
import re
# Note -- data attributes indexes are for the following
#  0 - age
#  1 - workclass
#  2 - fnlwgt
#  3 - education
#  4 - education-num
#  5 - marital-status
#  6 - occupation
#  7 - relationship
#  8 - race
#  9 - sex
# 10 - capital-gain
# 11 - capital-loss
# 12 - hours-per-week
# 13 - native-country
# 14 - salary (>50K, <=50K)

continent = {"United-States" : "AM", "Cambodia" : "AS", "England" : "EU", "Puerto-Rico" : "AM", "Canada" : "AM", "Germany" : "EU", "Outlying-US(Guam-USVI-etc)":"AM", "India":"AS", "Japan":"AS", "Greece" : "EU", "South":"AM", "China":"AS", "Cuba":"AM", "Iran":"AS", "Honduras":"AM", "Philippines":"OC", "Italy":"EU", "Poland":"EU", "Jamaica":"AM", "Vietnam":"AS", "Mexico":"AM", "Portugal":"EU", "Ireland":"EU", "France":"EU", "Dominican-Republic":"AM", "Laos":"AS", "Ecuador":"AM", "Taiwan":"AS", "Haiti":"AM", "Columbia":"AM", "Hungary":"EU", "Guatemala":"AM", "Nicaragua":"AM", "Scotland":"EU", "Thailand":"AS", "Yugoslavia":"EU", "El-Salvador":"AM", "Trinadad&Tobago":"AM", "Peru":"AM", "Hong":"AS", "Holand-Netherlands":"EU","?":"?"}



def generalize_country(c):
    d=c
    try :
        d = continent[c]
    except KeyError:
        d = "Other"
    #print "generalizing country: %s -> %s" % (c,d)

    return d

def generalize_id_user(a):
    return a
def generalize_date(a):
    return a
def generalize_hours(a):
    return a
def generalize_id_item(a):
    return a
def generalize_price(a):
    a = float(a)

    b = str(7*round(a/7)+1)
    #print "generalizing age: %d -> %s" % (a,b)
    return b
def generalize_qty(a):
    a = float(a)
    b = str(4*round(a/4)+1)
    #print "generalizing age: %d -> %s" % (a,b)
    return b


def generalize(pathfile) :

    infile =  pathfile
    print ("Input file name: %s" % infile)
    outfile = re.sub("\.","_generalized.",infile)
    print ("Output file name: %s" % infile)

    out = open(outfile,'w')


    i=0

    for l in open(infile, "r").readlines():
        r_ = l.replace('\r', '').replace('\n', '').replace(', ', ',').split(',')

        r = [""] *  len(r_)
        for ix, a in enumerate(r_):
            if i<6 :
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
