import sqlite3

database = './bgg.sqlite'
conn = sqlite3.connect(database)
cursor = conn.cursor()

games_table = '''
DROP TABLE IF EXISTS games;
CREATE TABLE games (
    id INTEGER PRIMARY KEY,
    mechanics TEXT,
    median REAL,
    image TEXT,
    wishing INTEGER,
    owned INTEGER,
    expansions TEXT,
    trading INTEGER,
    artists TEXT,
    yearpublished INTEGER,
    maxplayers INTEGER,
    numweights INTEGER,
    wanting INTEGER,
    thumbnail TEXT,
    publishers TEXT,
    families TEXT,
    description TEXT,
    minplayers INTEGER,
    averageweight REAL,
    expansion TEXT,
    bayesaverage REAL,
    implementations TEXT,
    designers TEXT,
    categories TEXT,
    minage INTEGER,
    name TEXT,
    playingtime INTEGER,
    ranks TEXT,
    average REAL,
    usersrated INTEGER,
    alternative_names TEXT,
    stddev REAL,
    expands TEXT,
    numcomments INTEGER
);
'''
users_table = '''
CREATE TABLE users (
    webaddress TEXT,
    steamaccount TEXT,
    buddies TEXT,
    avatarlink TEXT,
    firstname TEXT,
    lastname TEXT,
    top TEXT,
    xboxaccount TEXT,
    psnaccount TEXT,
    hot TEXT,
    lastlogin TEXT,
    country TEXT,
    yearregistered TEXT,
    guilds INTEGER,
    stateorprovince TEXT,
    wiiaccount TEXT,
    id INTEGER,
    traderating TEXT,
    name TEXT
);
'''

collections_table = '''
CREATE TABLE collections (
    owner TEXT,
    items TEXT,
    amount INTEGER
);
'''
