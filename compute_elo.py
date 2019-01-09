import numpy as np
from collections import defaultdict

def prob_calc(rating1, rating2):
    return 1.0 / (1 + math.pow(10, 1.0 * (rating1 - rating2) / 400))

if __name__ == '__main__':
    
    event_ids = np.loadtxt('./event_ids.csv').astype(np.int64)
    #the event_ids file is already sorted temporally due to the way it was queried.
   
    for e_id in event_ids:
        try:
            matches = np.loadtxt('./matches/'+str(e_id)).astype(np.int64)
