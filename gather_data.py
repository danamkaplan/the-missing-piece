from boardgamegeek import BoardGameGeek
import pickle
import time
from tqdm import tqdm

# BGG object
bgg = BoardGameGeek()

games = {}
missing_game_ids = []
for id_ in tqdm(xrange(1,100)):
    try:
        game = bgg.game(game_id = id_)
        games[id_] = game.data()
    except:
        missing_game_ids.append(id_)
    #time.sleep(0.1)

f = open('./data/games.pkl', 'wb')
pickle.dump(games, f)
f.close()

