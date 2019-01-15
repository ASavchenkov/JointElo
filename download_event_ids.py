import queries
import time
import re
from graphQLUtils import make_query
import numpy as np

#note that this doesn't care about tournaments, just the specific events we care about
#specifically ones that say "Singles" in the name.
def get_all_events():
    event_ids = list()
    empty_page = False
    i = 0 
    while(not empty_page):
        i+=1
        tourney_json = make_query(queries.tournament, {'perPage':50,'page':i}).json() 
        nodes = tourney_json['data']['tournaments']['nodes']
        print(type(nodes))
        if(nodes == None):
            empty_page = True
        else:
            for node in nodes:
                for event in node['events']:
                    if(re.search('singles',event['name'],re.IGNORECASE) and event['videogame']['id']==1386):
                        event_ids.append(event['id'])
                        print(event)
        time.sleep(1)
        print(len(event_ids))
    return event_ids

if __name__ == "__main__":
    event_ids = get_all_events()
    
    event_array = np.asarray(event_ids,dtype = np.int64)
    print(event_array)
    np.savetxt('./data/event_ids.csv', event_array.astype(int),fmt='%i', delimiter = ',')
