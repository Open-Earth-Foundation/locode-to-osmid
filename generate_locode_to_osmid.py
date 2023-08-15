import requests
import sys
import csv
import time

def slurp_file(name):
    data = []
    with open(name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def prefixed_id_of(item):
    return "%s%s" % (item['osm_type'][0].upper(), item['osm_id'])

def get_osm_id(city, state=None, country=None):
    print("Getting OSM ID for %s, %s" % (city, state or country))
    url = "https://nominatim.openstreetmap.org/search"
    headers = {'User-Agent': 'locode-to-osmid/0.1.0 (https://github.com/Open-Earth-Foundation/locode-to-osmid)'}
    params = {
        'city': city,
        'format': 'json'
    }
    if state:
        params['state'] = state
    if country:
        params['country'] = country
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        json = response.json()
        if len(json) == 1:
            item = json[0]
            return prefixed_id_of(item)
        elif len(json) == 0:
            print("No matches for %s, %s" % (city, state or country))
            return None
        else:
            print("%d matches for %s, %s" % (len(json), city, state or country))
            # We prefer relations, if any
            candidates = list(filter(lambda x: x['osm_type'] == "relation", json))
            if len(candidates) == 0:
                candidates = json
            item = max(candidates, key=lambda x: x['importance'])
            return prefixed_id_of(item)
    else:
        return None

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    map = []
    data = slurp_file(infile)
    for row in data:
        time.sleep(1)
        if len(row['is_part_of']) == 2:
            osm_id = get_osm_id(city=row['name'], country=row['is_part_of'])
        else:
            osm_id = get_osm_id(city=row['name'], state=row['is_part_of'])
        if osm_id:
            map.append([row['actor_id'], osm_id])
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(map)
