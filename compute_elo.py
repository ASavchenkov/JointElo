from collections import defaultdict
import numpy as np
import pickle

#probability that 1 will beat 2.
def prob_calc(rating1, rating2):
    return 1.0 / (1 + np.power(10, (rating2 - rating1) / 400))

#K1 and K2 can either be a vector or scalar, however,
#SUM(K1) = SUM(K2) must be true for this to be correct.
def update_rating(winner_rating, loser_rating, K1, K2):
    prob_win = prob_calc(winner_rating, loser_rating)
    new_winner_rating = winner_rating + K1 * (1-prob_win)
    new_loser_rating = loser_rating + K2 * (prob_win-1)
    print(np.sum(winner_rating+loser_rating)-np.sum(new_winner_rating+new_loser_rating))
    return (new_winner_rating, new_loser_rating)

#Most of the data doesn't actually provide choices,
#so we need to make assumptions as to what they chose.
#One way is to assume a uniform distribution.-------------------
#The other is to figure out which characters they've chosen before,
#and then distribute based on those statistics.---------------
def default_player():
    return [(0,np.ones(72)*1200)]

def set_K(K,char_choice, char_mapping):
    if(char_choice==-1):
        # return 0
        return K/72
    else:
        K_arr = np.zeros(72)
        K_arr[char_mapping[char_choice]] = K
        return K_arr

#this dictionary is used to figure out
#which index of the array we should use.
def get_char_mapping():
    ids = dict()
    with open('./data/char_mapping.csv', 'r') as character_file:
        for i,line in enumerate(character_file.readlines()):
            ids[int(line.split(',')[0])] = i
    return ids

if __name__ == '__main__':
    
    K = 30*72 #we steal this constant from chess. Seems common enough.
    joint_elo_history = defaultdict(default_player)
    
    char_mapping = get_char_mapping()
    event_ids = np.loadtxt('./data/event_ids.csv').astype(np.int64)
    #the event_ids file is already sorted temporally due to the way it was queried.
   
    for e_id in event_ids:
        try:
             
            matches = np.loadtxt('./data/matches/'+str(e_id)+'.csv',delimiter=',').astype(np.int64)
            for match in matches:
                
                winner = match[1]
                loser = match[2]
                winner_K = set_K(K, match[3],char_mapping)
                loser_K = set_K(K, match[4],char_mapping)
                
                winner_rating = joint_elo_history[winner][-1][1]
                loser_rating =  joint_elo_history[loser][-1][1]
                
                new_winner_rating, new_loser_rating = update_rating(winner_rating,loser_rating,winner_K, loser_K)

                joint_elo_history[winner].append((e_id, new_winner_rating))             
                joint_elo_history[loser].append((e_id, new_loser_rating))         
                
                
        except OSError:
            pass
            # traceback.print_exc()
            #This just means that event didn't have any games recorded for that event.
            #That's OK. We will make it through.
    
    history_file = open('./data/history_file','wb')
    pickle.dump(joint_elo_history,history_file)
    history_file.close()
