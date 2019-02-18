import pymongo
from collections import defaultdict
import time
import requests
import json
import traceback
import math

import queries
from graphQLUtils import make_query

#depends on the document having an _id
def upsert_one(collection, document):
    if document['_id'] is None:
        raise(ValueError('document does not have an _id.'))
    collection.update_one({'_id':document['_id']},{
        '$set': document
    }, upsert=True)

def unset_processed(collection, query = {}):
    print(collection.find().count())
    collection.update_many(query,{'$set':{'processed':False}})

# handles taking stuff out of the character csv and putting it into the db
def insert_characters(db):

    def default_game():
        return {'characters': list()}

    game_dict = defaultdict(default_game)

    with open('./data/characters.csv', 'r') as character_file:
        for line in character_file.readlines():
            split_line = line.split(',')

            game_id = int(split_line[-2])
            game_name = split_line[-1]
            character_id = int(split_line[0])
            character_name = split_line[1]

            db['characters'].insert_one({'_id':character_id,
                                         'name': character_name,
                                         'game_id':game_id})
            upsert_one(db['video_games'],{'_id':game_id, 'name':game_name})


# game_id comes as a string now.
def update_tournaments(db):
    i=0


    try: #this is a bad way to go about this but I don't want to write more code
        max_ts = db['tournaments'].find_one(sort=[('startAt',-1)])['startAt']
    except:
        max_ts = 0
    while(True):
        per_page = 100
        while(True):
            starttime = time.time()
            tourney_json = make_query(queries.tournament, {'perPage': int(per_page), 'startAt':max_ts+1}).json()
            if 'data' in tourney_json:
                break
            print(tourney_json)
            time.sleep(3/4)
            per_page /= 2
        print(max_ts, per_page)

        try:
            nodes = tourney_json['data']['tournaments']['nodes']
            if(nodes == None):
                break
            else:
                max_ts = nodes[-1]['startAt']
                for node in nodes:
                    upsert_one(db['tournaments'], {
                        '_id': node['id'],
                        'startAt': node['startAt'],
                        'events': node['events'],
                        'processed': False
                    })

        except Exception:
            print('FAILED PAGE: ', max_ts)
            print(tourney_json)
            traceback.print_exc()
        sleep_time = 3/4-(time.time()-starttime)
        if(sleep_time>0):
            time.sleep(sleep_time)

def set_processed(collection, item):
    collection.update_one({'_id':item['_id']}, {
        '$set': {
            'processed' : True
        }
    })

def extract_events(db):
    todo = db['tournaments'].find({'processed': False})
    for tournament in todo:
        print('extract_events: ',tournament)

        if 'events' not in tournament or tournament['events'] is None:
            set_processed(db['tournaments'], tournament)
            continue
        for e in tournament['events']:
            starttime = time.time()
            upsert_one(db['events'], {
                '_id': e['id'],
                'parent': tournament['_id'],
                'name': e['name'],
                'slug': e['slug'],
                'videogame': e['videogame']['id'],
                'startAt': tournament['startAt'],
                'processed': False
            })

        set_processed(db['tournaments'], tournament)

def get_pg(event_id, pg_id):
    try:
        r_string = '''https://api.smash.gg/phase_group/''' + str(pg_id) + '?expand[]=sets&expand[]=entrants'
        response = requests.get(r_string).text
        return json.loads(response)
    except Exception as e:
        print('failed: ', pg_id, e)
        return {}

def get_phase_groups(db):
    todo = db['events'].find({'processed': False})
    # todo = db['events'].find()
    for event in todo:

        starttime = time.time()
        try:
            event_json = make_query(queries.event, {'id':str(event['_id'])}).json()['data']['event']
            if(event_json['phaseGroups'] is not None):
                pgs = event_json['phaseGroups']
                for pg in pgs:
                    raw_json = get_pg(event['_id'],pg['id'])
                    try:
                        team_size = len(raw_json['entities']['entrants'][0]['participantIds'])
                    except:
                        #if we can't get that info then boo hoo, we don't use those phase groups.
                        team_size = -1
                        pass
                    upsert_one(db['phase_groups'],{
                        '_id': pg['id'],
                        'parent': event['_id'],
                        'startAt': event['startAt'],
                        'raw_json': raw_json,
                        'videogame': event['videogame'],
                        'processed': False,
                        'team_size' : team_size
                    })
                    print('phase_group',pg['id'])

            set_processed(db['events'], event)



        except Exception:
            print('failed: ', event['_id'])
            print(event_json)
            traceback.print_exc()

        sleep_time = 3/4-(time.time()-starttime)
        if sleep_time>0:
            time.sleep(sleep_time)

def update_all_videogames(db):
    phase_groups = db['phase_groups'].find({})
    i = 0
    for pg in phase_groups:
        # print(db['events'].find_one({'_id':pg['parent']})['videogame'])
        db['phase_groups'].update_one({'_id': pg['_id']}, {
            '$set': {'videogame':db['events'].find_one({'_id':pg['parent']})['videogame']}
        })
        i+=1
        print(i, pg['_id'])
if __name__ == '__main__':
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client['joint_elo_base']

    # if the character info hasn't been put in the database it needs to be done.
    if 'characters' not in db.list_collection_names():
        insert_characters(db)
    update_tournaments(db)
    extract_events(db)
    get_phase_groups(db)