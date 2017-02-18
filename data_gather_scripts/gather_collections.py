from gather_data import ElementTree, etree_to_dict
import requests
import json
from time import sleep
import sys
from tqdm import tqdm
from boardgamegeek import BoardGameGeek

method = 'api'
bgg = BoardGameGeek()


def format_url(guild_id, page_num):
    url = 'https://boardgamegeek.com/xmlapi2/guild?id='+str(guild_id)
    return url+'&members=1&page='+str(page_num)

# getting usernames from guilds 1 - 2800
def grab_users(start, stop):
    user_names = set()
    for guild_id in xrange(start, stop+1):
        page_num = 1
        while page_num != 'missing':
            url = format_url(guild_id, page_num)
            r = requests.get(url)
            tree = ElementTree.fromstring(r.content)
            guild_dict = etree_to_dict(tree)
            page_num += 1
            try:
                user_names = user_names.union(parse_user_names(guild_dict))
            except:
                page_num = 'missing'
            sleep(1)
    write_users(start, stop, user_names)
    return(user_names)

def gather_collections(users):
    counter = 0
    collection_dict = {}
    for user in tqdm(users):
        counter += 1
        collection_dict[user] = grab_collection(user)
        if counter == 1000:
            counter = 0
            write_collection_json(counter-1000, counter, collection_dict)
            collection_dict = {}
        sleep(3)
    write_collection_json('remaining', 'remaining', collection_dict)


def write_users(start, stop, user_list):
    location = './data/user_list_{}_{}.txt'.format(start, stop)
    f = open(location, 'w')
    user_list = ', '.join([i for i in user_list])
    f.write(user_list.encode('utf8'))
    f.close()

def grab_collection(user_name):
    if method == 'xml':
        url ='https://boardgamegeek.com/xmlapi/collection/username='+user_name+'own=1'
        r = requests.get(url)
        tree = ElementTree.fromstring(r.content)
        collection = etree_to_dict(tree)
        try:
            collection = collection['items']['item']
            return [item['@objectid'] for item in collection]
        except:
            return []
    else:
        try:
            coll_obj = bgg.collection(user_name=user_name)
            collection = coll_obj.data()['items'] 
            return [item['id'] for item in collection]
        except:
            return []

def parse_user_names(guild_dict):
    users = guild_dict['guild']['members']['member']
    return [user['@name'] for user in users]

def write_collection_json(first, last, collection_dict):
    j = json.dumps(collection_dict)
    loc = './data/collection_{}_{}.json'.format(first, last)
    f = open(loc, 'wb')
    f.write(j)
    f.close()

if __name__=='__main__':
    start = int(sys.argv[1])
    stop = int(sys.argv[2])
    global method 
    method = sys.argv[3]
    users = grab_users(start, stop)
    gather_collections(users)
    
