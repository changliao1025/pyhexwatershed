
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations
def generate_compset_json_file():
    iFlag_mesh_type = 1 #1 hexagon 2 3 4
    iFlag_flowline = 1

 

    compset = {}
    compset['people'] = []
    compset['people'].append({
        'name': 'Scott',
        'website': 'stackabuse.com',
        'from': 'Nebraska'
    })
    compset['people'].append({
        'name': 'Larry',
        'website': 'google.com',
        'from': 'Michigan'
    })
    compset['people'].append({
        'name': 'Tim',
        'website': 'apple.com',
        'from': 'Alabama'
    })

    with open('compset.txt', 'w') as outfile:
        json.dump(compset, outfile)

    return
