from collections import defaultdict
import json

#we want to have a json organized by game_id

def default_game():
    return {'characters': list()}

game_dict = defaultdict(default_game)


#we begin by removing the image json thingy, because... why.
with open('./data/characters.csv', 'r') as character_file:
    for line in character_file.readlines():
        split_line = line.split(',')

        game_id = int(split_line[-2])
        game_name = split_line[-1]
        character_id = int(split_line[0])
        character_name = split_line[1]

        game_dict[game_id]['characters'].append((character_id,character_name))
        if('game_name' not in game_dict[game_id]):
            game_dict[game_id]['game_name'] = game_name


with open('./data/characters.json', 'w') as outfile:
    json.dump(game_dict, outfile)
