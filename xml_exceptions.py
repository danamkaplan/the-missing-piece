
def evaluate_xml(g):
    #turn xml pull into the same format as json
    game_dict = {}
    #import pdb; pdb.set_trace()
    game_dict['mechanics'] =unpack_list(g.get('boardgamemechanic', []))
    game_dict['playingtime'] = int(g.get('playingtime', 0))
    game_dict['id'] = int(g.get('@objectid', 0))
    game_dict['image'] = g.get('image', '')
    game_dict['yearpublished'] =int(g.get('yearpublished', 0))
    game_dict['maxplayers'] = int(g.get('maxplayers', 0))
    game_dict['thumbnail'] = g.get('thumbnail','')
    game_dict['publishers'] = unpack_list(g.get('boardgamepublisher', []))
    game_dict['families'] = unpack_list(g.get('boardgamefamily', []))
    game_dict['description'] = g.get('description', '')
    game_dict['minplayers'] = int(g.get('minplayers', 0))
    game_dict['designers'] = unpack_list(g.get('boardgamedesigner', 0))
    game_dict['categories'] = unpack_list(g.get('boardgamecategory', 0))
    if type(g['name']) == list:
        game_dict['name'] = g['name'][0]['#text']
    else:
        game_dict['name'] = g.get('name', '')
    #game_dict['alterative_names']
    #game_dict['expands']
    
    #Utilizing the stats field
    stats = g['statistics']['ratings']
    #ratings statistics
    game_dict['median'] = float(stats['median'])
    game_dict['numcomments'] = int(stats['numcomments'])
    game_dict['stddev'] = float(stats['stddev'])
    game_dict['wishing'] = int(stats['wishing'])
    game_dict['usersrated'] = int(stats['usersrated'])
    game_dict['averageweight'] = float(stats['averageweight'])
    game_dict['trading'] = int(stats['trading'])
    game_dict['average'] = float(stats['average'])
    game_dict['owned'] = int(stats['owned'])
    game_dict['wanting'] = int(stats['wanting'])
    game_dict['bayesaverage'] = float(stats['bayesaverage'])
    game_dict['numweights'] = int(stats['numweights'])
    
    #rank transformation
    rank_dict = []
    try:
        rank_dict.append({
                'friendlyname': 'Board Game Rank',
                'name': 'boardgame',
                'value': stats['ranks']['rank'][0]['@value']
                })
        rank_dict.append({
                'friendlyname': 'Strategy Game Rank',
                'name': 'strategygames',
                'value': stats['ranks']['rank'][1]['@value']
                })
    except:
        rank_dict.append({
                'friendlyname': 'Strategy Game Rank',
                'name': 'strategygames',
                'value': stats['ranks']['rank']['@value']
                })
    game_dict['ranks'] = rank_dict  

    return game_dict['id'], game_dict


def unpack_list(obj_to_eval):
    try:
        if type(obj_to_eval) == list:
            return [item['#text'] for item in obj_to_eval]
        else:
            return [obj_to_eval['#text']]
    except:
        return []

