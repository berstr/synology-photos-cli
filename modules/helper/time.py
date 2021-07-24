

import requests
import json
from datetime import datetime, timezone

import config


def set_time_from_filename(item):
    result = None
    if item['filename_analysis']['time_synced'] == 'true':
        result = { 'result' : 'info', 'info' : 'item time and filename are already in sync'}
    elif item['filename_analysis']['result'] != 'ok':
        result = { 'result' : 'info', 'info' : 'not a valid filename: {}'.format(item['info']['filename']) }
    else:
        # creates a datetime object based on the filename - in the local timezone
        dt = datetime(int(item['filename_analysis']['year']),int(item['filename_analysis']['month']), int(item['filename_analysis']['day']),int(item['filename_analysis']['hour']),int(item['filename_analysis']['minute']),int(item['filename_analysis']['second']))
        # converts the datetime object and calculates a timestanp in GMT/UTC timezone
        utc_timestamp = int((dt - datetime(1970, 1, 1)).total_seconds())
        PARAMS = {
            "id": item['info']['id'],
            'time':utc_timestamp
        }
        URL = 'http://' + config.SYNOLOGY_PHOTO_SERVICE + '/item/time'
        r = requests.put(url=URL, params=PARAMS)
        if r.status_code != 200:
            result = {'result' : "HTTP error - helper.rename() - status_code: {}".format(r.status_code),  'status_code' : r.status_code}
        else:
            json_result = r.json()
            if json_result['result'] == 'ok':
                result = {'result' : 'ok'}
            else:
                result = {'result' : 'error' , 'error' : '{}'.format(json.dumps(json_result['synology']))}
            
    result['filename'] = item['info']['filename']
    if 'date' in item['filename_analysis']:
        result['date'] = item['filename_analysis']['date']
    else:
        result['date'] = ''
    if 'time' in item['filename_analysis']:
        result['time'] = item['filename_analysis']['time']
    else:
        result['time'] = ''

    return result

