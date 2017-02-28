from generate_topics import Topic_Model
from user_profile_pipeline import User_Profile
from game_data_pipeline import Game_Data_Pipeline
from scipy.spatial.distance import cosine
import sys


class Recommender(object):

    def __init__(self, folder):
        self.folder = folder
        self.TM = Topic_Model(folder)
        self.GDP = Game_Data_Pipeline(folder)
        
    def generate_feature_matrix(self):
        self.TM.load_topics_csv()
        self.topic_matrix = self.TM.W
    
    def generate_cosine_matrix(self):
        for i in range
    
    def write_cosine_matrix(self):


if __name__ == '__main__':

    folder = sys.argv[1]

    # Create initial game data
    GDP = Game_Data_Pipeline(folder)
    GDP.create_total_dict()

    GDP.create_set_features(['mechanics', 'categories'])
    GDP.add_feature('averageweight')
    GDP.write_feature_matrix_csv()

    TM = Topic_Model(folder)
    TM.load_feature_matrix()
    TM.generate_topics()
    TM.write_topics_csv()

    

''' 
    [u'mechanics',
    u'expansions', 
    u'image', 
    u'wishing', 
    u'owned', 
    u'trading', 
    u'artists', 
    u'id', 
    u'usersrated', 
    u'yearpublished', 
    u'maxplayers', 
    u'numweights', 
    u'wanting', 
    u'thumbnail', 
    u'publishers', 
    u'families', 
    u'description', 
    u'minplayers', 
    u'averageweight', 
    u'expansion', 
    u'bayesaverage', 
    u'implementations', 
    u'designers', 
    u'categories', 
    u'minage', 
    u'name', 
    u'playingtime', 
    u'ranks', 
    u'average', 
    u'median', 
    u'numcomments', 
    u'stddev', 
    u'expands', 
    u'alternative_names']

''' 
