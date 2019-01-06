import numpy as np
import os
import json
import traceback
import sys
#format of game entries
#game_id | winner_id | loser_id | winner_pick | loser_pick

def get_matches(event_id):
    dirname ='brackets/'+str(event_id)
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
    return games 
    

#we do this temporally based on events.
#Then we sort matches based on time. Then run those sequentially.

if __name__ == '__main__':
    
    event_ids = np.loadtxt('./event_ids.csv').astype(np.int64)
    for i in range(1000):
        get_matches(event_ids[i])
    
    
