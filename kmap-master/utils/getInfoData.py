import sys
import re
import csv
from math import sqrt, pow
import pickle
import os


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



"""
permet de faire le dico de tout les id item avec les 2 digit
"""
def creat_dico_tronc_two_first_digit(dict):
    dico_id_item_troc={}
    for k in dict.keys():
        # digits = list(k)
        # first_digit=digits[0:1]
        first_digit=k[- len(k)+2:]
        first_digit="".join(first_digit)
        if first_digit not in dico_id_item_troc :
            dico_id_item_troc[first_digit]=k
        print(first_digit,dico_id_item_troc[first_digit])
    file=open(os.path.expanduser("id_item_two_first_digit.p"),"wb")
    pickle.dump(dico_id_item_troc,file)

def creat_dico_tronc_two_last_digit(dict):
    dico_id_item_troc={}
    for k in dict.keys():

        first_digit=k[0:len(k)-2]
        first_digit="".join(first_digit)
        if first_digit not in dico_id_item_troc :
            dico_id_item_troc[first_digit]=k
        print(first_digit,dico_id_item_troc[first_digit])
    file=open(os.path.expanduser("id_item_two_last_digit.p"),"wb")
    pickle.dump(dico_id_item_troc,file)




def percentile(dict_price,path):
    out_percentile=open(path,"w+")

    dict_price.sort()
    i=0
    percentile=[]
    old_price=0
    for price in dict_price :
        mod=50000
        if i<300000 :
            mod=20000
        elif i<314000 :
            mod =2000
        else :
            mod= 200

        if i%mod==0:
            if price>0:
                if old_price!=price :
                    percentile.append(price)
                    print(i," : "   ,price)
                    out_percentile.write(str(i)+" : "+str(price)+"\n")
                    old_price=price

        i+=1


    out_percentile.close()
    return percentile


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

    dict_id_item={}
    dict_id_users={}

    list_id_item=[]

    dict_price=[]
    dict_qty=[]


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
                if ix==0:
                    dict_id_users
                    if a not in dict_id_users.keys() :
                        dict_id_users[a]=1
                    else :
                        dict_id_users[a]+=1

                elif ix==3 :
                    if a not in dict_id_item.keys() :
                        dict_id_item[a]=1
                    else :
                        dict_id_item[a]+=1

                    if a not in list_id_item:
                        list_id_item.append(a)

                elif ix==4: # price

                    a=float(a)
                    # print(a)
                    dict_price.append(a)
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
                    dict_qty.append(a)


            i=i+1
    k_trheshold=5
    k_cluster=0
    for k,v in dict_id_item.items():
        if v>=k_trheshold :
            k_cluster+=1
    print("done!")
    print("k-anonimity : ",k_trheshold," , k_cluster",k_cluster , 'out of ',len(dict_id_item.keys()))


    # creat_dico_tronc_two_first_digit(dict_id_item)
    # creat_dico_tronc_two_last_digit(dict_id_item)
    percentile_price=percentile(dict_price,os.path.expanduser("data/info_percentile_price.txt"))
    file=open(os.path.expanduser("percentile_price.p"),"wb")
    pickle.dump(percentile_price,file)

    percentile_qty=percentile(dict_qty,os.path.expanduser("data/info_percentile_qty.txt"))
    file=open(os.path.expanduser("percentile_qty.p"),"wb")
    pickle.dump(percentile_qty,file)


    file=open(os.path.expanduser("list_id_item.p"),"wb")
    pickle.dump(list_id_item,file)

    file_dict_id_item=open(os.path.expanduser("dict_id_item_sell.p"),"wb")
    pickle.dump(dict_id_item,file_dict_id_item)

    file_dict_id_users=open(os.path.expanduser("dict_id_users_buy.p"),"wb")
    pickle.dump(dict_id_users,file_dict_id_users)






    out=open(os.path.expanduser("data/info_ground_truth.txt"),"w+")

    out.write("max_price : "+str(max_price))
    out.write("min_price : "+str(min_price))
    out.write("avg_price : "+str(avg_price/i))
    out.write("ecart_type_price : "+str(sqrt(ecart_type_price/i)) )
    out.write("max_qty : "+str(max_qty))
    out.write("min_qty : "+str(min_qty))
    out.write("avg_qty : "+str(avg_qty/i))
    out.write("ecart_type_qty : "+str(sqrt(ecart_type_qty/i)))



    print("i",i)
    print("max_price",max_price)
    print("min_price",min_price)
    print("avg_price",avg_price/i)
    print("ecart_type_price",sqrt(ecart_type_price/i))


    print("max_qty",max_qty)
    print("min_qty",min_qty)
    print("avg_qty",avg_qty/i)
    print("ecart_type_qty",sqrt(ecart_type_qty/i))

    dict_id_item_out=open("info_dic_id_item.txt","w+")
    out.write("\n\ndico_it_item\n\n : ")
    sorted_by_value =  sorted(dict_id_item, key=dict_id_item.get, reverse=True) #sorted(dict_id_item.items(), key=lambda kv: kv[1], reverse=True)
    for k in sorted_by_value:
        dict_id_item_out.write(str(k)+" : "+str(dict_id_item[k])+'\n')

    out.write("\n\ndico_it_user\n\n : ")
    sorted_by_value = sorted(dict_id_users, key=dict_id_users.get, reverse=True) #sorted(dict_id_users.items(), key=lambda kv: kv[1], reverse=True)
    for k  in sorted_by_value:
        dict_id_item_out.write(str(k)+" : "+str(dict_id_users[k])+'\n')

    dict_id_item_out.close()
