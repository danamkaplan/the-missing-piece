from boardgamegeek import BoardGameGeek
from tqdm import tqdm
import json

# BGG object
bgg = BoardGameGeek()


# latest game 218780
def write_json(first, last, game_dict):
        j = json.dumps(games)
        loc = './data/games_{}_{}.json'.format(first, last)
        f = open(loc, 'wb')
        f.write(j)
        f.close()

games = {}
missing_game_ids = []
found_game_ids = []
every_10k = 0
min_id = 0
for id_ in tqdm(range(1, 218780)):
    if every_10k == 0:
        min_id = id_
    try:
        game = bgg.game(game_id = id_)
        games[id_] = game.data()
        every_10k += 1
        found_game_ids.append(id_)
    except:
        missing_game_ids.append(id_)

    if every_10k == 10000:
        write_json(min_id, id_, games)
        min_id = 0
        games = {}


write_json('first', 'last', games)
f = open('./data/found_games.txt', 'wb')
f.write(found_game_ids)
f.close()
f = open('./data/missing_games.txt', 'wb')
f.write(missing_game_ids)
f.close()
