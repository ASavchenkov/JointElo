import numpy as np
import os
import json
import traceback
import sys

#while we would like to sort by match time,
#that information is quite uncommon,
#thus we assume that a players skill
#does not change much over a single event

#format of game entries
#game_id | winner_id | loser_id | winner_pick | loser_pick

def get_matches(event_id):
    dirname ='./data/brackets/'+str(event_id)
    games = list()
    for _,dirnames,filenames in os.walk(dirname):
        for f in filenames:
            try:
                bracket_json = json.load(open(dirname+'/'+f))
                if 'sets' not in bracket_json['entities']:
                    break
                sets = bracket_json['entities']['sets']
                
                for s in sets:
                    if(s['games']!=None and len(s['games'])!=0):
                        for game in s['games']:
                            game_id = game['id']
                            winner_id = game['winnerId']
                            loser_id = game['loserId']
                            sel = game['selections']
                            
                            if(winner_id is not None and loser_id is not None):
                                if(sel!=None and len(sel)!=0):
                                    
                                    winner_pick = -1
                                    loser_pick = -1
                                    if(winner_id in sel): 
                                        winner_pick = sel[str(winner_id)]['character'][0]['selectionValue']
                                    if(loser_id in sel): 
                                        loser_pick = sel[str(loser_id)]['character'][0]['selectionValue']
                                else:
                                    winner_pick = -1
                                    loser_pick = -1
                                games.append((game_id, winner_id, loser_id, winner_pick, loser_pick))
            except Exception :
                print(dirname+'/'+f)
                traceback.print_exc(file=sys.stdout)
    return np.array(games) if len(games)!=0 else None
    

#we do this temporally based on events.
#Then we sort matches based on time. Then run those sequentially.

if __name__ == '__main__':
    
    event_ids = np.loadtxt('./data/event_ids.csv').astype(np.int64)
    for e_id in event_ids:
        match_array = get_matches(e_id)
        if(match_array is not None):
            # print(e_id)
            # print(match_array)
            np.savetxt('./data/matches/'+str(e_id)+'.csv', match_array.astype(np.int32),fmt='%i', delimiter = ',')
            # print(len(match_array))
     
