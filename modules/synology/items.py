import requests

import config


def get_folder_items(folder_id):
    result = None
    items = []
    PARAMS = {
        "id": folder_id
    }
    URL = 'http://' + config.SYNOLOGY_PHOTO_SERVICE + '/folder/items'
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200 and r.status_code != 500:
        result = {'result' : "HTTP error - GET /folder/items: folder_id: {}) - status code: {}".format(folder_id,r.status_code)}
    elif r.status_code == 500:
        result = {'result':'ok','items':[]}
    else:
        json_result = r.json()
        if json_result["result"] == 'ok':
            result = {'result':'ok','items':json_result['items']}
        else:
            result = {'result':'synology photos error','synology':json_result}
    return result


def get_items(ids):
    if len(ids) == 0:
        return {'result':'ok','items':[]}    
    result = None
    items = []
    ids_string = ''
    for id in ids:
        ids_string = ids_string + '{},'.format(id)
    ids_string = ids_string[:len(ids_string)-1] # cut off the trailing , in the string

    PARAMS = {
        "ids": ids_string
    }
    URL = 'http://' + config.SYNOLOGY_PHOTO_SERVICE + '/items/info'
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200 and r.status_code != 500:
        result = {'result' : "HTTP error - GET /items/info : ids: {}) - status code: {}".format(ids_string,r.status_code)}
    elif r.status_code == 500:
        result = {'result':'ok','items':[]}
    else:
        json_result = r.json()
        if json_result["result"] == 'ok':
            result = {'result':'ok','items':json_result['items']}
        else:
            result = {'result':'synology photos error','synology':json_result}
    return result


def refresh_items(items):
    ids = []
    for item in items:
        ids.append(item['info']['id'])
    return get_items(ids)
