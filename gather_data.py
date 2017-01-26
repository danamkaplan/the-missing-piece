from boardgamegeek import BoardGameGeek
from collections import defaultdict
from tqdm import tqdm
import json
import sys
import requests
from time import sleep
from xml.etree import ElementTree

# BGG object
bgg = BoardGameGeek(requests_per_minute=90)


# latest game 218780
def write_json(first, last, game_dict):
    j = json.dumps(game_dict)
    loc = './data/games_{}_{}.json'.format(first, last)
    f = open(loc, 'wb')
    f.write(j)
    f.close()

def write_missing(missing_game_ids, start, stop):    
    f = open('./data/missing_games_{}_{}.txt'.format(start, stop), 'wb')
    f.write(', '.join([str(i) for i in missing_game_ids]))
    f.close()

def pull_game_data(start, stop):
    games = {}
    missing_game_ids = []
    found_game_ids = []
    loops = 0
    for id_ in tqdm(xrange(start, stop+1)):
        loops += 1
        try:
            game = bgg.game(game_id = id_)
            games[id_] = game.data()
            game = None
        except:
            missing_game_ids.append(id_)
        if loops == 10000:
            loops = 0
            write_json(id_, id_, games)
            games = {}
            write_missing(missing_game_ids, id_, id_)


def evaluate_xml(g):
    #turn xml pull into the same format as json
    game_dict = {}
    game_dict['mechanics'] =unpack_list(g['boardgamemechanic'])
    game_dict['playingtime'] = int(g['playingtime'])
    game_dict['id'] = int(g['@objectid'])
    game_dict['image'] = g['image']
    #game_dict['expansions'] 
    #game_dict['artists']
    game_dict['yearpublished'] = g['yearpublished']
    game_dict['maxplayers'] = int(g['maxplayers'])
    game_dict['thumbnail'] = g['thumbnail']
    game_dict['publishers'] = unpack_list(g['boardgamepublisher'])
    game_dict['families'] = unpack_list(g['boardgamefamily'])
    game_dict['description'] = g['description']
    game_dict['minplayers'] = int(g['minplayers'])
    #game_dict['expansion']
    #game_dict['implementations'] = 
    game_dict['designers'] = unpack_list(g['boardgamedesigner'])
    game_dict['categories'] = unpack_list(g['boardgamecategory'])
    #game_dict['minage']
    game_dict['name'] = g['name']
    #game_dict['alternative_names']
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
    rank_dict[0] = {
            'friendlyname': 'Board Game Rank',
            'name': 'boardgame',
            'value': stats[0]['@value']
            }
    rank_dict[1] = {
            'friendlyname': 'Strategy Game Rank',
            'name': 'strategygames',
            'value': stats[1]['@value']
            }
    game_dict['ranks'] = rank_dict  

    return game_dict[id], game_dict

def unpack_list(obj_to_eval):
    if type(obj_to_eval) == list:
        return [item['#text'] for item in obj_to_eval]
    else:
        return obj_to_eval

def etree_to_dict(t):

    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d



def format_url(start, stop):
    url = 'https://boardgamegeek.com/xmlapi/boardgame/'
    ids_ = ",".join([str(n) for  n in range(start, stop+1)])
    return url+ids_+'&stats=1'

def pull_game_data_xml(start, stop):
    url = format_url(start, stop)
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    many_game_dict = etree_to_dict(tree)
    #parse the xml now
    for game in many_game_dict['boardgames']['boardgame']:
        import pdb; pdb.set_trace()
        try:
            evaluate_xml(game['boardgame'])
        except:
            print game
            print 'error'

    return(many_game_dict.keys())


    
if __name__=='__main__':
    start = int(sys.argv[1])
    stop = int(sys.argv[2])
    method = sys.argv[3]
    if method == 'library':
        pull_game_data(start, stop)
    else:
        pull_game_data_xml(start, stop)
