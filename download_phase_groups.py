import queries
import time
from graphQLUtils import make_query
import numpy as np

#we assume that all of the events are the correct type
def get_all_phase_groups(event_array):
    phase_group_ids = list()
    failed_event_ids = list()
    for event_id in event_array:
        try:
            event_response = make_query(queries.event, {'id':event_id}) 
            event_json = event_response.json()
            event_json = event_json['data']['event']
            phase_group_ids.extend([pg['id'] for pg in event_json['phaseGroups']])
            print(len(phase_group_ids),event_json['name'],len(event_json['phaseGroups']))
            time.sleep(1)
        except:
            failed_event_ids.append(event_id)
            print('failed: ',event_id)
    return phase_group_ids,failed_event_ids

if __name__ == "__main__":
    event_ids = np.loadtxt('./event_ids.csv')
    print(event_ids)
    phase_group_ids,failed_event_ids = get_all_phase_groups(event_ids)
    
    phase_group_array = np.asarray(phase_group_ids,dtype = np.int64)
    failed_event_array = np.asarray(failed_event_ids, dtype= np.int64)
    np.savetxt('phase_group_ids.csv', phase_group_array.astype(int),fmt='%i', delimiter = ',')
    np.savetxt('failed_event_ids.csv', failed_event_array.astype(int),fmt='%i', delimiter = ',')
