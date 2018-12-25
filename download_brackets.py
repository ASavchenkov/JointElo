import numpy as np
import requests

#this will not use the new graphQL stuff.
def get_all_sets(phase_group_array):
    failed_phase_groups = list()
    i = 0
    for pg_id in phase_group_array:
        try:
            r_string = '''https://api.smash.gg/phase_group/'''+str(pg_id)+'?expand[]=sets'
            response = requests.get(r_string)
            print(response)
            f = open('./brackets/'+str(pg_id), 'w')
            f.write(response.text)
            print(i,len(phase_group_array))
        except:
            failed_phase_groups.append(pg_id)
            print('failed: ',pg_id)
        i+=1

if __name__ == "__main__":
    phase_group_array = np.loadtxt('./phase_group_ids.csv').astype(dtype=np.int64)
    print(len(phase_group_array))
    get_all_sets(phase_group_array)
    
