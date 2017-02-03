from __future__ import division
import json
import generate_topics


class User_Profile(object):
    def __init__(self, game_collection, W):
        self.game_collection = game_collection
        self.W = W
        self.W_normed = generate_topics.normalize_features_to_topics  
        self.num_games = len(game_collection)
    
    def get_game_model_vectors(self):
        #get the W vectors of the collection
        pass


if __name__=='__main__':
    #get a list of User_Profiles
    #model them somehow
    pass
