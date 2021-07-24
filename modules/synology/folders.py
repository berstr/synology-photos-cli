import requests

import config

def folders_get(folder_id):
    result = None
    PARAMS = {
        "id": folder_id
    }
    URL = 'http://' + config.SYNOLOGY_PHOTO_SERVICE + '/folders/get'
    r = requests.get(url=URL, params=PARAMS)
    #print(config.SYNOLOGY_PHOTO_SERVICE)
    #print(r)
    if r.status_code != 200 and r.status_code != 500:
        result = {'result' : "HTTP error - GET /folders/get - folder_id: {} - status code: {}".format(folder_id,r.status_code)}
    elif r.status_code == 500:
        result = {'result':'ok','folders':[]}
    else:
        json_result = r.json()
        #print(json_result)
        if json_result["result"] == 'ok':
            result = {'result':'ok','folders':json_result['folders']}
        else:
            result = {'result':'synology photos error','synology':json_result}
    return result

