import sys
import re
import csv
from math import sqrt, pow

"""

max_price=38970
min_price=0.001
avg_price=3.503359
ecart_type_price=77.519
max_qty=4800
min_qty=-9360
avg_qty=12.0.21
ecart_type_qty=46.321
"""

const_average_price=3.503359
const_ecart_type_price=77.519
const_average_qty=12.021
const_ecart_type_qty=46.321



def getInfoData(pathfile) :


    print ("Input file name: %s" % pathfile)
    file=open(pathfile,"r+")

    i=0
    max_price=0
    min_price=1000000
    avg_price=0.0
    ecart_type_price=0.0
    max_qty=0
    min_qty=100000
    avg_qty=0.0
    ecart_type_qty=0.0

    dict={}

    for l in file.readlines():
        r_ = l.replace('\r', '').replace('\n', '').replace(', ', ',').split(',')
        for ix, a in enumerate(r_):
            """
            if(ix==0): #id_user
                 r[ix] = a
            elif(ix==1): # date
                r[ix] = a
            elif(ix==2): # hours
                r[ix] = a
            elif(ix==3): # id_item
                r[ix] = a
            """
            if i<6 :
                print("premiere boucle")
            else :
                if ix==3 :
                    if a not in dict.keys() :
                        dict[a]=1
                    else :
                        dict[a]+=1
                elif ix==4: # price
                    a=float(a)
                    avg_price+=a
                    ecart_type_price+=pow((a-const_average_price),2)
                    if max_price< a :
                        max_price=a
                    if min_price>a :
                        min_price=a

                elif ix==5 : # qty

                    a=float(a)
                    avg_qty+=a
                    ecart_type_qty+=pow((a-const_average_qty),2)
                    if max_qty< a :
                        max_qty=a
                    if min_qty>a :
                        min_qty=a


            i=i+1
    k_trheshold=5
    k_cluster=0
    for k,v in dict.items():
        if v>=k_trheshold :
            k_cluster+=1



    out=open("info_ground_truth.txt","w+")

    out.write("max_price : "+str(max_price))
    out.write("min_price : "+str(min_price))
    out.write("avg_price : "+str(avg_price/i))
    out.write("ecart_type_price : "+str(sqrt(ecart_type_price/i)) )
    out.write("max_qty : "+str(max_qty))
    out.write("min_qty : "+str(min_qty))
    out.write("avg_qty : "+str(avg_qty/i))
    out.write("ecart_type_qty : "+str(sqrt(ecart_type_qty/i)))

    print("done!")
    print("k-anonimity : ",k_trheshold," , k_cluster",k_cluster , 'out of ',len(dict.keys()))

    print("i",i)
    print("max_price",max_price)
    print("min_price",min_price)
    print("avg_price",avg_price/i)
    print("ecart_type_price",sqrt(ecart_type_price/i))


    print("max_qty",max_qty)
    print("min_qty",min_qty)
    print("avg_qty",avg_qty/i)
    print("ecart_type_qty",sqrt(ecart_type_qty/i))

    dict_out=open("info_list_id_item.txt","w+")
    for k,v in dict.items():
        dict_out.write(str(k)+'\n')

    dict_out.close()
