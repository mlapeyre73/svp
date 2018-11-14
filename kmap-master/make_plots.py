import pickle
import matplotlib.pyplot as plt
from utils.kmap import plot_kmap
import csv
import os
from utils.csv2pickle import csv2pickle
from utils.generalize import generalize
from utils.getInfoData import getInfoData

import argparse




def get_args():
	parser=argparse.ArgumentParser()
	parser.add_argument('-i', "--inputfilecsv", help="csv file path", default='null')
	parser.add_argument('-o', "--outputfilepickle", help="pickle output path", default='null')
	parser.add_argument('-g', "--generalizing", help="lance la generalisation ", default=False)
	parser.add_argument('-a', "--analyseData", help="lance l'analyseData ", default=False)


	args = parser.parse_args()
	return args

def build_fingerprint_dataset(records, attr_ixs):
	data = []
	dict = []
	for r in records:
		attrs = str([r[_] for _ in attr_ixs])
		try:
			ix = dict.index(attrs)
		except ValueError:
			ix = len(dict)
			dict.append(attrs)
		data.append(ix)
	return data

# Note -- data attributes indexes are for the following
#  0 - id_user
#  1 - date
#  2 - hours
#  3 - id_item
#  4 - price-num
#  5 - qty-status


args = get_args()

if args.generalizing is not False :
	print("GENERALISATION")
	generalize(os.path.expanduser("data/ground_truth.csv"))
	exit(0)

if args.analyseData is not False :
	print("GET INFO DATA")
	getInfoData(os.path.expanduser("data/ground_truth.csv"))
	exit(0)


if args.inputfilecsv is not "null" :
	if args.outputfilepickle is not "null":
		csv2pickle(os.path.expanduser(args.inputfilecsv),os.path.expanduser(args.outputfilepickle))
		exit(0)


records = pickle.load(open("ground_truth_new_generalized_date_hours_id_item_twoLastDigits_pricePercentile_qtyPercentileDifferential.p", "r+b"))
# records = pickle.load(open("ground_truth.csv", "r+b"))
# records = csv.reader(os.path.expanduser("ground_truth.csv"))

# Dataset-1: age, sex, native-country
# data1 = build_fingerprint_dataset(records, attr_ixs=[0, 1, 2])
# plot_kmap(data=data1, data_label="id_user, date, hours", filename=os.path.expanduser("images/kmap_attrnum=3"), plot_annotation=[[1, 3], [100, 1000]], annotation_params=dict(radius=.1, linestyle=dict(color='r', width=2, style=':')), colormap=plt.cm.viridis)

# Dataset-2: age, sex, native-country, race, relationship, workclass
data2 = build_fingerprint_dataset(records, attr_ixs=[ 1, 2, 3, 4, 5])
plot_kmap(data=data2, data_label="date, hours, id_item, price, qty", filename=os.path.expanduser("images/ground_truth_new_generalized_date_hours_id_item_twoLastDigits_pricePercentile_qtyPercentileDifferential=5"), plot_annotation=[[1, 3], [100, 1000]], colormap=plt.cm.viridis)
