from boardgamegeek import BoardGameGeek
from collections import defaultdict
from tqdm import tqdm
import json
import sys
import requests
from time import sleep
from xml.etree import ElementTree
from collect_json import merge_dicts
from xml_exceptions import evaluate_xml 

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

def grab_game_data_xml(start, stop):
    url = format_url(start, stop)
    r = requests.get(url)
    tree = ElementTree.fromstring(r.content)
    many_game_dict = etree_to_dict(tree)
    #parse the xml now
    list_of_game_dicts = []
    for game in many_game_dict['boardgames']['boardgame']:
        try:
            list_of_game_dicts.append(evaluate_xml(game))
        except:
            pass
    return(list_of_game_dicts)

def pull_game_data_xml(start, stop):
    id_ = start
    loops = 0
    games = {}
    for id_ in tqdm(range(start, stop+1, 100)):
        #pull from api in batches of 100
        new_game_dict = grab_game_data_xml(id_, id_+99)
        games = merge_dicts(games, new_game_dict)
        loops = loops + 100 
        if loops == 10000:
            loops = 0
            write_json(id_ - 10000, id_, games)
            games = {}
        #be nice to that api
        sleep(5)


    #get that last bit
    write_json(id_ - 100, id_, games)

    
    
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
    
if __name__=='__main__':
    start = int(sys.argv[1])
    stop = int(sys.argv[2])
    method = sys.argv[3]
    if method == 'library':
        pull_game_data(start, stop)
    else:
        pull_game_data_xml(start, stop)
