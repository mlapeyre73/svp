import sys
import re
import numpy
import pickle
import os
import random
import hashlib
import time
from datetime import datetime, timedelta

generalized_data=open("../data/ground_truthground_truth_id_user_hashsalte1sur20_diffPrivacyDate7days_hours_uniq_id_item_Delete5_price_percent20000_qty_percent20000.csv","r+")
# ground_truth_data=open("../data/ground_truth.csv", "r+")

generated_file=open("./reidentified_price_hashsalte1sur20etc.csv", "w+")

lines_read_generalized = 0
lines_read_ground_truth = 0
saved_line=""


for l in generalized_data.readlines():
    lines_read_ground_truth = 0
    if(lines_read_generalized != 0):
        a = l.split(',')
        saved_line=""
        dist = 1000

        ground_truth_data=open("../data/ground_truth.csv", "r+")
        for k in ground_truth_data.readlines():
        
            if(lines_read_ground_truth != 0):
                k = k.replace('\n','')
                b = k.split(',')
                if(a[3] == b[3]):
                    if(abs(float(a[4]) - float(b[4])) < dist):
                        dist = abs(float(a[4]) - float(b[4]))
                        saved_line = k
                        print(dist)
                        print(saved_line)

            lines_read_ground_truth += 1
            # print(k)

        generated_file.write(saved_line+'\n')
        ground_truth_data.close()

    lines_read_generalized += 1
    if(lines_read_generalized > 100):
        break

generated_file.close()
generated_file=open("./reidentified_price_hashsalte1sur20etc.csv", "r+")
nb=0
for i, line in enumerate(generated_file):
    ground_truth_100lines=open("../data/ground_truth_100lines.csv", "r+")
    for j, line2 in enumerate(ground_truth_100lines):
        if(i == j):
            if(line == line2):
                print('YES PUTAIN')
                nb += 1
                print(nb)

    ground_truth_100lines.close()