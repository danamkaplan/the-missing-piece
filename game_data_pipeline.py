import json
import os
import pandas as pd
import sys

class Game_Data_Pipeline(object):

    def __init__(self, folder):
        self.folder = folder
        self.total_dict = {}

    def merge_dicts(self, *dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def load_data(self, location_str):
        f = open(location_str, 'r')
        json_to_dict = json.load(f)
        f.close()
        return(json_to_dict)

    def gather_files(self):
        files = os.listdir(self.folder)
        list_of_game_dicts = []
        for f in files:
            if f[:5] == 'games':
                f = self.folder + "/" + f
                game_dict = self.load_data(f)
                parsed_dict = {int(key): game_dict[key] for key in game_dict.keys()}
                list_of_game_dicts.append(parsed_dict)
        
        return list_of_game_dicts

    def create_total_dict(self):
        game_list = self.gather_files()
        self.total_dict = self.merge_dicts(*game_list)

    def get_total_dict(self):
        return self.total_dict

    def unravel_dict(self, d, feature_list):
        games = []
        categories = []
        for id_, game in d.iteritems():
            for feature in feature_list:
                for word in game[feature]:
                    if word == 'Dice':
                        word = 'Dice Rolling'
                    games.append(id_)
                    categories.append(word)
        ones = [1]*len(games)
        return games, categories, ones

    def pivot_features(self, ids_, features, ones):
        df = pd.DataFrame({'ids': ids_, 'features': features, 'ones': ones})
        feature_matrix = df.pivot_table(index='ids', columns='features', values='ones')
        return feature_matrix

    def create_set_features(self, feature_list):
        self.feature_matrix = self.pivot_features(*self.unravel_dict(self.total_dict, feature_list))

    def add_feature(self, feature):
        """
        Add a feature to final feature matrix

        Params:
            feature_key: String. Dict key of the feature. 
        
        Returns:
            None
        """
        new_feature_dict = self.get_feature(feature)
        column = pd.DataFrame.from_dict(new_feature_dict, orient='index')
        column.columns = [feature]
        self.feature_matrix = self.feature_matrix.join(column, how='left')
        self.feature_matrix.fillna(0, inplace=True)

    def get_feature(self, feature):
        """
        Returns game_id and feature as a dict

        Params: 
            feature_key: String. Dict key of the feature. 
        
        Returns:
        """
        d = self.total_dict
        return {int(key): d[key][feature] for key in d.keys()}

    def write_feature_matrix_csv(self):
        f = self.folder + '/feature_matrix.csv'
        self.feature_matrix.fillna(0, inplace=True)
        self.feature_matrix.to_csv(f, encoding='utf-8')

    def load_feature_matrix_csv(self):
        f = self.folder + '/feature_matrix.csv'
        self.feature_matrix = pd.read_csv(f, encoding='utf-8', index_col='ids') 
        return self.feature_matrix


if __name__ == '__main__':
    folder = sys.argv[1]
    data = Game_Data_Pipeline(folder)
    data.create_total_dict()
    
