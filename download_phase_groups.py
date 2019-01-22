import queries
import time
import json
import os
import traceback
from graphQLUtils import make_query
import numpy as np

#we assume that all of the events are the correct type
def get_all_phase_groups(event_array, game_id):
    todo_events = set([x for x in event_array])
    try:
        completed_events = np.loadtxt('./data/'+game_id+'/completed_events.csv')
        failed_events = np.loadtxt('./data/'+game_id+'/failed_events.csv')
         
    except:
        e
    phase_groups = list()
    failed_event_ids = list()
    for event_id in event_array:
        try:
            event_response = make_query(queries.event, {'id':str(event_id)}) 
            response_json = event_response.json()
            event_json = response_json['data']['event']
            if( event_json['phaseGroups'] is not None ):
                phase_groups.extend([(event_id, pg['id']) for pg in event_json['phaseGroups']])
                print(len(phase_groups),event_json['name'],len(event_json['phaseGroups']))
            time.sleep(1)

        except Exception:
            print('failed: ',event_id)
            traceback.print_exc()
            print(event_json)
            print()
            failed_event_ids.append(event_id)
    return phase_groups,failed_event_ids

if __name__ == "__main__":

    with open('./data/characters.json') as f:
        characters = json.load(f)
    
    for game_id in characters:
        if(not os.path.isfile('./data/'+game_id+'/phase_group_ids.csv')):
            event_ids = np.loadtxt('./data/'+game_id+'/event_ids.csv').astype(np.int32)
            print(event_ids)
            phase_group_ids,failed_event_ids = get_all_phase_groups(event_ids)
            
            phase_group_array = np.asarray(phase_group_ids,dtype = np.int64)
            failed_event_array = np.asarray(failed_event_ids, dtype= np.int64)
            np.savetxt('./data/'+game_id+'/phase_group_ids.csv', phase_group_array.astype(int),fmt='%i', delimiter = ',')
            np.savetxt('./data/'+game_id+'/failed_event_ids.csv', failed_event_array.astype(int),fmt='%i', delimiter = ',')
