from collect_json import data_pipeline
import numpy as np
import pandas as pd
import sys
from sklearn.decomposition import NMF


class Topic_Model(object):
    
    def __init__(self):
        pass
    
    def create_feature_matrix(self, folder):
        # import pdb; pdb.set_trace()        
        self.feature_matrix = data_pipeline(self.folder, 'combine', set=True)
        return self.feature_matrix

    def write_feature_matrix_csv(self):
        np.savetxt(self.folder + '/feature_matrix.csv', W, delimiter=',') 

    def write_topics_csv(self, folder):
        np.savetxt(folder + '/W.csv', W, delimiter=',') 
        np.savetxt(folder + '/H.csv', H, delimiter=',') 

    def load_topics_csv(self, folder):
        W = np.loadtxt(folder + '/W.csv', delimiter=',') 
        H = np.loadtxt(folder + '/H.csv', delimiter=',') 
        return W, H

    def normalize_games_to_topics(self):
        return np.apply_along_axis(self.norm, 1, self.W) 

    def normalize_features_to_topics(self):
        return np.apply_along_axis(self.norm, 0, self.H) 

    def normalize_topics_to_games(self):
        return np.apply_along_axis(self.norm, 0, self.W) 

    def normalize_topics_to_features(self):
        return np.apply_along_axis(self.norm, 1, self.H) 

    def norm(vector):
        return vector/sum(vector)

    def generate_topics(self, k=47):
        self.nmf_model = NMF(n_components=k, init='random', random_state=0)
        self.W = self.nmf_model.fit_transform(self.feature_matrix)
        self.H = self.nmf_model.components_
        return self.W, self.H

    def match_topic_to_games(self, topic_vector):
        # grab  
        pass

    def match_topic_to_features(self, feature_topic_vector):
        return zip(feature_topic_vector, self.feature_matrix.columns.values)
        

if __name__ == '__main__':
    folder = sys.argv[1]
    TM = Topic_Model()
    feature_matrix = TM.create_feature_matrix(folder)
    W, H = TM.generate_topics()
    TM.write_topics_csv(folder)
    


