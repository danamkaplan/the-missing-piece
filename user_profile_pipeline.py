from __future__ import division
import json
from generate_topics import Topic_Model
import sys
import pandas as pd


class User_Profile(object):
    def __init__(self, game_collection, W_norm):
        self.game_collection = game_collection
        self.W_norm = W_norm
        # self.W_normed = generate_topics.normalize_features_to_topics  
        self.num_games = len(game_collection)
    
    def get_game_model_vectors(self):
        # get the W vectors of the collection
        pass


if __name__ == '__main__':
    # get a list of User_Profiles
    # model them somehow
    path = sys.argv[1]
    f = open(path)
    collection_dict = json.load(f)
    f.close()
    
    TM = Topic_Model()
    W, H = TM.load_topics_csv(path)
    W_norm = TM.normalize_topics_to_games()

    profiles = []
    for user_name in collection_dict.keys():
        collection = collection_dict[user_name]
        profiles.append(User_Profile, collection, )

    game_titles = merge_dicts(*gather_files(folder, 'name'))
