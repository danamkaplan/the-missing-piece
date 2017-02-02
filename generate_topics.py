from collect_json import data_pipeline
import numpy as np
import pandas as pd
import sys
from scipy.linalg import svd
from sklearn.decomposition import NMF


def create_feature_matrix(folder):
    return data_pipeline(folder, 'combine', set=True)

def write_topics_csv():
    pass 

def normalize_games_to_topics(W):
    return np.apply_along_axis(norm, 1 , W) 

def normalize_features_to_topics(H):
    return np.apply_along_axis(norm, 0 , W) 

def normalize_topics_to_games(W):
    return np.apply_along_axis(norm, 1 , W) 

def normalize_topics_to_features(H):
    return np.apply_along_axis(norm, 0 , W) 

def norm(vector):
    return vector/sum(vector)


def generate_topics(feature_matrix):
    nmf_model = NMF(n_components=47, init='random', random_state=0)
    W = nmf_model.fit_transform(feature_matrix)
    H = nmf_model.components_
    return W, H

def match_topic_to_games(topic_vector):
    pass

def match_topic_to_mechanics(topic_vector):
    pass

if __name__=='__main__':
    folder = sys.argv[1]
    feature_matrix = create_feature_matrix(folder)
    W, H = generate_topics(feature_matrix)


