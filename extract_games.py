import numpy as np
from os import listdir

#we do this temporally based on events.
#Then we sort matches based on time. Then run those sequentially.

if __name__ == '__main__':
    
    event_ids = np.loadtxt('./event_ids.csv')
    
    
