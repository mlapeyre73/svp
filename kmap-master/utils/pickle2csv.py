import csv
from six.moves import cPickle as pickle
import numpy as np


def pickletocv2(path_pickle,path_csv):

    x = []
    with open(path_pickle,'rb') as f:
        x = pickle.load(f)

    with open(path_csv,'wb') as f:
        writer = csv.writer(f)
        for line in x: writer.writerow(line)
