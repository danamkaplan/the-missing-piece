from boardgamegeek import BoardGameGeek
import sys

bgg = BoardGameGeek()

def get_collection_ids(collection):
    return [game['id'] for game in collection.data()['items']]

def get_top_ten_topics(collection_ids):
    #

if __name__=='__main__':
    name_string = sys.argv[1]
    collection = bgg.collection(user_name=name_string)
    collection_ids = get_collection_ids(collection)
