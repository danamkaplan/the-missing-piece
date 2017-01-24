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
    return {int(id_): j_dict[key][field] for key  in j_dict.keys()}

def gather_files(folder):
    files = os.listdir(folder)
    for f in files:
        if f[0] == 'g':
            pass

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def load_data(field):
    pass    
