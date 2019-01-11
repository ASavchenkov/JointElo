

character_mapping = list()
mapping_file = open('./data/char_mapping.csv','w')

with open('characters.csv', 'r') as character_file:
    for line in character_file.readlines():
        if 'Super Smash Bros. Ultimate' in line:
            split_line = line.split(',')
            mapping_file.write(split_line[0]+','+split_line[1].strip('"')+'\n')



