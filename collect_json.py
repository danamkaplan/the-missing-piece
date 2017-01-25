import json
import os

def parse_data(j_dict, field):
    """Takes in dict chunks parses out only the field 
    to save space and time.

    Keyword arguments:
    j_dict - json dictionary of game data
    field - the field to return

    Returns:
    game_dict - dictgame_id
    """ 
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

def gather_files(folder):
    files = os.listdir(folder)
    list_of_game_dicts = []
    for f in files:
        f = folder + "/" + f
        print f
        if f[-4:] == 'json':
            parsed_dict = parse_data(load_data(f), 'mechanics')
            print parsed_dict
            list_of_game_dicts.append(parsed_dict)
    
    return merge_dicts(*list_of_game_dicts)

