from __future__ import division
import json
from generate_topics import Topic_Model
import sys
import pandas as pd
import numpy as np


class User_Profile(object):

    def __init__(self, game_collection, W_norm):
        self.game_collection = np.array(game_collection) 
        self.W_norm = W_norm
        self.num_games = len(game_collection)
    
    def get_game_model_vectors(self, feature_matrix_ids):
        # get the W vectors of the collection
        coll_indices = np.searchsorted(self.game_collection, feature_matrix_ids)
        self.game_vectors = self.W_norm[coll_indices]
        return self.game_vectors

    def make_weighted_topics(self):
        self.topic_profile = sum(self.game_vectors/self.num_games)

    def get_top_n_topics(self, n=5):
        top_n_topics = self.topic_profile.argsort()[::-1]
        zip(top_n_topics, self.topic_profile[top_n_topics])
            
    
    


if __name__ == '__main__':
    # get a list of User_Profiles
    # model them somehow
    path = sys.argv[1]
    f = open(path)
    collection_dict = json.load(f)
    f.close()
    
    TM = Topic_Model()
    W, H = TM.load_topics_csv(path)
    feature_matrix = TM.load_feature_matrix_csv(path)
    W_norm = TM.normalize_topics_to_games()

    profiles = []
    for user_name in collection_dict.keys():
        collection = collection_dict[user_name]
        profiles.append(User_Profile, collection, )

    game_titles = merge_dicts(*gather_files(folder, 'name'))
