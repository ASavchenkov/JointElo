import queries
import time
import json
import os
import traceback
import sys
from graphQLUtils import make_query

def json_default_load(path, default):
    try:
        return json.load(open(path,'r'))
    except:
        print('faied to load')
        print(path)
        return default

def write_three_datas(root_dir,failed,completed,phase_groups):

    json.dump(failed,open(root_dir+'failed_events.json','w'))
    json.dump(completed,open(root_dir+'completed_events.json','w'))
    json.dump(phase_groups,open(root_dir+'phase_groups.json','w'))

#we assume that all of the events are the correct type
def get_all_phase_groups(game_id):
    root_dir = 'data/'+game_id+'/'

    all_events = set(json_default_load(root_dir+'event_ids.json',list()))
    completed_events = json_default_load(root_dir+'completed_events.json',list())
    failed_events = json_default_load(root_dir+'failed_events.json',list())
    phase_groups = json_default_load(root_dir+'phase_groups.json',list())

    todo_events = all_events.difference(set(completed_events),set(failed_events))
    
    
    for event_id in todo_events:
        try:
            event_response = make_query(queries.event, {'id':str(event_id)}) 
            response_json = event_response.json()
            event_json = response_json['data']['event']
            if( event_json['phaseGroups'] is not None ):
                phase_groups.extend([(event_id, pg['id']) for pg in event_json['phaseGroups']])
                print(len(phase_groups),event_json['name'],len(event_json['phaseGroups']))
            completed_events.append(event_id)
            time.sleep(1)
       
        
        except KeyboardInterrupt: #when ctrl-c is hit
            write_three_datas(root_dir,failed_events,completed_events,phase_groups)
            sys.exit()
        except Exception:
            print('failed: ',event_id)
            traceback.print_exc()
            print(event_json)
            print()
            failed_events.append(event_id)

    write_three_datas(root_dir,failed_events,completed_events,phase_groups)

if __name__ == "__main__":

    with open('./data/characters.json') as f:
        characters = json.load(f)
    
    for game_id in characters:
        if(not os.path.isfile('./data/'+game_id+'/phase_group_ids.json')):
            get_all_phase_groups(game_id)
            
