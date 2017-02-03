import json
import requests as rq

# Reads application config, which has API keys and
# SoQL parameters.
APP_CONFIG = json.loads(open('app-config.json', 'r').read())


# If title includes the words in this list,
# the record will be used.
# Original data has more than 400 different titles.
KEEP_LIST = [
    'arson',
    'assault',
    'burglary',
    'firearm',
    'homicide',
    'larceny',
    'murder',
    'rape',
    'robbery',
    'sex',
    'shots',
    'theft',
    'weapons'
    ]


# Further, narrows down to six categories
CATEGORIES = {
    'arson': 'fire',
    'assault': 'action',
    'burglary': 'theft',
    'firearm': 'gun',
    'homicide': 'murder',
    'larceny': 'theft',
    'murder': 'murder',
    'rape': 'sex',
    'robbery': 'theft',
    'sex': 'sex',
    'shots': 'gun',
    'theft': 'theft',
    'weapons': 'gun',
    }


# Location list
AREAS = [
    {'name': 'Brier Creek',
     'lat': 35.912697,
     'lng': -78.781792},
    {'name': 'Cameron Village',
     'lat': 35.789403,
     'lng': -78.663048},
    {'name': 'Crabtree Pines',
     'lat': 35.862744,
     'lng': -78.711886},
    {'name': 'Downtown',
     'lat': 35.778315,
     'lng': -78.640196},
    {'name': 'Laurel Hills',
     'lat': 35.833097,
     'lng': -78.698538},
    {'name': 'Mordecai',
     'lat': 35.797566,
     'lng': -78.629338},
    {'name': 'Northeast Raleigh',
     'lat': 35.867382,
     'lng': -78.563709},
    {'name': 'North Hills',
     'lat': 35.834982,
     'lng': -78.638971},
    {'name': 'North Raleigh',
     'lat': 35.879601,
     'lng': -78.625057},
    {'name': 'Six Forks North',
     'lat': 35.900966,
     'lng': -78.652319},
    {'name': 'Six Forks South',
     'lat': 35.819788,
     'lng': -78.623952},
    {'name': 'Southwest Raleigh',
     'lat': 35.768438,
     'lng': -78.694160},
    {'name': 'Stonehenge',
     'lat': 35.882922,
     'lng': -78.679141},
    {'name': 'Umstead',
     'lat': 35.890672,
     'lng': -78.750061},
    {'name': 'Wade',
     'lat': 35.809230,
     'lng': -78.734234}
    ]


def category(words):
    """Given words (title), returns its category"""
    for listed in KEEP_LIST:
        if listed in words:
            return CATEGORIES[listed]
    return None


def extract(f, result, j_data):
    """Given original data from OpenData, cleans up and narrows down
    to relevant records. Returns a count of relevant records."""
    for record in j_data:
        tmp = {}
        desc = record['lcr_desc'].lower().split('/')
        title = desc[0]
        cat = category(title)
        if cat and 'location' in record:
            f(result, record, title, cat)
    return result


def getExtracted(f, lat, lng):
    """API endpoint to return crime data.
    This method expects the request, /api/JSON?lat=xxx&lng=xxx ,
    and returns JSON data."""
    url = APP_CONFIG['opendata']['url']
    url = url + '$limit=' + str(APP_CONFIG['opendata']['limit'])
    url = url + '&$$app_token=' + APP_CONFIG['opendata']['app_token']
    # SoQL query: within_circle(field, lat, lng, radius)
    where_query = '&$where=within_circle(location, %s, %s, %s)' % (
        lat, lng, APP_CONFIG['opendata']['radius'])
    print(where_query)
    url += where_query
    print(url)
    response = rq.get(url)
    print("status_code: " + str(response.status_code))
    result = []
    if response.status_code == 200:
        j_data = response.json()
        return extract(f, result, j_data)
    else:
        return response.status_code

