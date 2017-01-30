import json
import os
import pandas as pd

def parse_data(j_dict, field):
    """Takes in dict chunks parses out only the field 
    to save space and time.

    Keyword arguments:
    j_dict - json dictionary of game data
    field - the field to return

    Returns:
    game_dict - dictgame_id
    """
    if field == 'all':
        return {int(key): j_dict[key] for key in j_dict.keys()}
    elif field == 'combine':
        return {int(key):
                set(j_dict[key]['mechanics']+j_dict[key]['categories']) for key in j_dict.keys()}
    else:
        return {int(key): j_dict[key][field] for key in j_dict.keys()}

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def load_data(location_str):
    f = open(location_str, 'r')
    j_to_dict = json.load(f)
    f.close()
    return(j_to_dict)

def gather_files(folder, field):
    files = os.listdir(folder)
    list_of_game_dicts = []
    for f in files:
        f = folder + "/" + f
        if f[-4:] == 'json':
            parsed_dict = parse_data(load_data(f),field)
            list_of_game_dicts.append(parsed_dict)
    
    return merge_dicts(*list_of_game_dicts)

def unravel_dict(d):
    games = []
    categories = []
    for game, keywords in d.iteritems():
        for word in keywords:
            games.append(game)
            categories.append(word)
    ones = [1]*len(games)
    return games, categories, ones

def create_feature_matrix(ids_, features, ones):
    df = pd.DataFrame({'ids': ids_, 'features': features, 'ones':ones})
    feature_matrix = df.pivot(index='ids', columns='features', values='ones')
    feature_matrix.fillna(0, inplace=True)
    return feature_matrix

def data_pipeline(folder, field):
    merged_dicts = gather_files(folder, field)
    feature_matrix = create_feature_matrix(*unravel_dict(merged_dicts))
    
    return feature_matrix
