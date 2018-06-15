import json
import time
import urllib.request
import urllib.parse

def _parseResponse(response):
    retVal = []
    for places in response['rows']:
        if(places['elements'][0]['status'] == 'OK'):
            retVal.append({'duration' : places['elements'][0]['duration']['value']/60,
                           'distance' : places['elements'][0]['distance']['value']/1000})
    return retVal

def distance(origin, destination,mode,key):
    maps_key = key
    distance_base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    for i in range(len(origin)):
        if 'toronto' not in origin[i].lower():
            origin[i] += ' toronto'
    origin = '|'.join([i.replace(", "," ").replace(","," ") for i in origin])
    destination = '|'.join([i.replace(", "," ").replace(","," ") for i in destination])
    url = distance_base_url + '?' + urllib.parse.urlencode({
        'origins': origin,
        'destinations': destination,
        'mode' : mode,
        'key': maps_key,
    }, safe='|')
    # print(url)
    current_delay = 0.1
    max_delay = 3600
    while True:
        try:
            response = str(urllib.request.urlopen(url).read().decode('UTF-8'))
        except IOError:
            pass
        else:
            result = json.loads(response.replace('\\n', ''))
            if result['status'] == 'OK':
                return _parseResponse(result)
            elif result['status'] != 'UNKNOWN_ERROR':
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception('Too many retry attempts.')
        print('Waiting', current_delay, 'seconds before retrying.')
        time.sleep(current_delay)
        current_delay *= 2

if __name__ == "__main__":
    listings = json.load(open('result.json'))
    #google maps stuff, updates travel time and distance for each listing to destination
    locations = []
    for i in range(len(listings)):
        locations.append(listings[i]['location'])
    with open('api_key.txt','r') as f:
        info = distance(locations,["College St at St George St"],'transit',f.read.strip())
        print(info)
