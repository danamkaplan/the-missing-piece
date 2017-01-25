from boardgamegeek import BoardGameGeek
from tqdm import tqdm
import json
import sys

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

if __name__=='__main__':
    start = int(sys.argv[1])
    stop = int(sys.argv[2])
    pull_game_data(start, stop)
