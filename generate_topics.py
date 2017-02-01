from collect_json import data_pipeline
import numpy as np
import pandas as pd
import sys
from scipy.linalg import svd



def create_feature_matrix(folder):
    return data_pipeline(folder, 'combine', set=True)

def write_topics_csv(games, features):
    pass 

def generate_topics(feature_matrix):
    pass

if __name__=='__main__':
    folder = sys.argv[1]
    feature_matrix = create_feature_matrix(folder)


