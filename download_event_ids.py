import queries
import time
import re
import json
import os
import traceback
import json
from graphQLUtils import make_query
import numpy as np

#note that this doesn't care about tournaments, just the specific events we care about
#specifically ones that say "Singles" in the name.
def get_all_events(game_id):
    event_ids = list()
    empty_page = False
    i = 0 
    while(not empty_page):
        i+=1
        if(i>200): break #smash.gg can't seem to handle tournaments greater than 10,000
        starttime = time.time()
        tourney_json = make_query(queries.tournament, {'perPage':50,'page':i,'gameID':game_id}).json() 
        try:
            nodes = tourney_json['data']['tournaments']['nodes']
            if(nodes == None):
                empty_page = True
            else:
                for node in nodes:
                    for event in node['events']:
                        if(re.search('singles',event['name'],re.IGNORECASE) and event['videogame']['id']==int(game_id)):
                            event_ids.append(event['id'])
                            print(event)

            nowtime = time.time()
            if(nowtime-starttime<1):
                time.sleep(1-(time.time()-starttime))
            print(len(event_ids))
        except Exception:
            print('FAILED PAGE: ',i)
            print(tourney_json)
            traceback.print_exc()
    return event_ids

if __name__ == "__main__":

    with open('./data/characters.json') as f:
        characters = json.load(f)
    
    existing_dirs = [name for name in os.listdir('./data')] #careful. This also includes files
    for game_id in characters:
        if(game_id not in existing_dirs):
            event_ids = get_all_events(game_id)
            
            print('finished game_id: ', game_id,'| name: ' + characters[game_id]['game_name'])
            try:
                os.mkdir('./data/'+game_id)
                f = open('./data/'+game_id+'/event_ids.json','w')
                json.dump(event_ids,f)
            except:
                print('failed game_id: '+str(game_id))
