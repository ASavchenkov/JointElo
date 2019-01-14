from collections import defaultdict
import numpy as np
import pickle

#probability that 1 will beat 2.
def prob_calc(rating1, rating2):
    return 1.0 / (1 + np.power(10, (rating2 - rating1) / 400))

#The previous algorithm was horribly wrong.
#The actual way to make sure this is correct even for
#cases where character choice is a PMF, is to "map"
#each character to each other character, thus simulating
#every single matchup that could exist.

#we don't do this because we don't need to.

def get_relevant_rating(all_ratings, char_choice):
    if(char_choice==-1):
        return np.mean(all_ratings)
    else:
        return all_ratings[char_choice]

def distribute_delta(all_ratings, char_choice, delta):
    if(char_choice == -1):
        return all_ratings + delta/72
    else:
        return all_ratings+np.eye(72)[char_choice]*delta

def update_rating(winner_rating, loser_rating, K, winner_choice, loser_choice):
    
    relevant_w_rating = get_relevant_rating(winner_rating, winner_choice)
    relevant_l_rating = get_relevant_rating(loser_rating, loser_choice)


    prob_win = prob_calc(relevant_w_rating, relevant_l_rating)
    
    winner_delta = K * (1-prob_win)
    loser_delta = K * (prob_win-1)
    #these now need to be distributed
    
    new_winner_rating = distribute_delta(winner_rating,winner_choice, winner_delta)
    new_loser_rating = distribute_delta(loser_rating, loser_choice, loser_delta)

    
    # error = np.sum(winner_rating+loser_rating)-np.sum(new_winner_rating+new_loser_rating)
    # if(np.abs(error)>0.0001):
        # print(new_winner_rating - winner_rating)
        # print(new_loser_rating - loser_rating)
        # print()
    return (new_winner_rating, new_loser_rating)

#Most of the data doesn't actually provide choices,
#so we need to make assumptions as to what they chose.
#One way is to assume a uniform distribution.-------------------
#The other is to figure out which characters they've chosen before,
#and then distribute based on those statistics.---------------
def default_player():
    return [(0,np.ones(72)*1200)]

#this dictionary is used to figure out
#which index of the array we should use.
def get_char_mapping():
    ids = dict()
    ids[-1] = -1
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
                
                winner_rating = joint_elo_history[winner][-1][1]
                loser_rating =  joint_elo_history[loser][-1][1]
                
                winner_choice = char_mapping[match[3]]
                loser_choice = char_mapping[match[4]]
                
                new_winner_rating, new_loser_rating = update_rating(winner_rating,loser_rating,K, winner_choice, loser_choice)

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
