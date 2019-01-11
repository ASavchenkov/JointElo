import numpy as np
import requests
import os

#this will not use the new graphQL stuff.
def get_all_sets(phase_group_array):
    failed_phase_groups = list()
    i = 0
    for event_id,pg_id in phase_group_array:
        try:
            r_string = '''https://api.smash.gg/phase_group/'''+str(pg_id)+'?expand[]=sets'
            response = requests.get(r_string)
            print(response)

            try:
                os.mkdir('./data/brackets/'+str(event_id))
            except:
                pass
            f = open('./data/brackets/'+str(event_id)+'/'+str(pg_id), 'w')
            f.write(response.text)
            print(i,len(phase_group_array))
        except Exception as e:
            failed_phase_groups.append(pg_id)
            print('failed: ',pg_id, e)
        i+=1

if __name__ == "__main__":
    phase_group_array = np.loadtxt('./data/phase_group_ids.csv',delimiter=',').astype(dtype=np.int64)
    print(len(phase_group_array))
    get_all_sets(phase_group_array)
    
