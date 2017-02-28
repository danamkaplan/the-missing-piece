from __future__ import division
from game_data_pipeline import Game_Data_Pipeline
import numpy as np
import sys
from sklearn.decomposition import NMF


class Topic_Model(object):
    
    def __init__(self, folder):
        self.folder = folder
        self.game_data = Game_Data_Pipeline(folder)

    def load_feature_matrix(self):
        """
        
        input:
            None

        output:
        """
        self.feature_matrix = self.game_data.load_feature_matrix_csv() 

    def write_topics_csv(self):
        """
        
        input:
            None

        output:
        """
        np.savetxt(self.folder + '/W.csv', self.W, delimiter=',') 
        np.savetxt(self.folder + '/H.csv', self.H, delimiter=',') 

    def load_topics_csv(self):
        """
        
        input:
            None

        output:
        """
        self.W = np.loadtxt(self.folder + '/W.csv', delimiter=',') 
        self.H = np.loadtxt(self.folder + '/H.csv', delimiter=',') 

    def normalize_games_to_topics(self):
        """
        
        input:
            None

        output:
        """
        return np.apply_along_axis(self.norm, 0, self.W) 

    def normalize_features_to_topics(self):
        """
        
        input:
            None

        output:
        """
        return np.apply_along_axis(self.norm, 1, self.H) 

    def normalize_topics_to_games(self):
        """
        
        input:
            None

        output:
        """
        return np.apply_along_axis(self.norm, 1, self.W) 

    def normalize_topics_to_features(self):
        """
        
        input:
            None

        output:
        """
        return np.apply_along_axis(self.norm, 0, self.H)  

    def norm(self, vector):
        """
        Scales a vector to have sum(vector) = 1
        
        input:
            vector: vector

        output:
            normed vector
        """
        return vector/float(sum(vector))

    def cluster_games(self):
        """
        Assigns the topic cluster (by topic index) to each game_id,
        based on the topic the game has the highest affinity with.

        input:
            None

        output:
            game_to_cluster: list of tuples of the format (topic index, game_id)
        """
        self.game_clusters = np.argsort(self.W)[:, -1]
        self.game_to_cluster = zip(self.game_clusters, self.feature_matrix.index.values)
        return self.game_to_cluster

    def generate_topics(self, k=47):
        """
        
        input:
            k: amount of topics to generate

        output:
        """
        self.nmf_model = NMF(n_components=k, init='random', random_state=0)
        self.W = self.nmf_model.fit_transform(self.feature_matrix)
        self.H = self.nmf_model.components_
        return self.W, self.H

    def match_topic_to_games(self, game_topic_vector):
        """
        
        input:

        output:
        """
        # grab the game title from gather json and zip
        return zip(game_topic_vector, self.feature_matrix.index.values)

    def match_topic_to_features(self, feature_topic_vector):
        """
        
        input:

        output:
        """
        return zip(feature_topic_vector, self.feature_matrix.columns.values)
    
    def get_gameid_to_index(self):
        """
        
        input:
            None

        output:
        """
        feature_matrix_ids = self.feature_matrix.index.values
        return {game_id: index[0] for index, game_id in np.ndenumerate(feature_matrix_ids)}

if __name__ == '__main__':
    folder = sys.argv[1]
    TM = Topic_Model()
    feature_matrix = TM.create_feature_matrix(folder)
    W, H = TM.generate_topics()
    TM.write_topics_csv(folder)
    


