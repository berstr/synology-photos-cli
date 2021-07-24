

import requests
import json
from datetime import datetime
import config


def rename_to_date(foldername, item):
    result = {}
    path = '{}{}/{}'.format(config.SYNOLOGY_PHOTO_SHARE,foldername,item['info']['filename'])
    index=int(datetime.utcnow().strftime("%f"))%100
    
    name = '{}-{}-{}-{}{}-{}{:02d}.{}'.format(
                                                item['date']['year'],
                                                item['date']['month'],
                                                item['date']['day'],
                                                item['date']['hour'],
                                                item['date']['minute'],
                                                item['date']['second'],
                                                index,
                                                item['filename_analysis']['extension'])


    if item['filename_analysis']['time_synced'] == 'true':
        result = { 'result' : 'info', 'info' : 'item name already correct'}
    else:
    
        PARAMS = {
            "path": path,
            "name": name
        }
        #config.LOGGER.info("helper.rename() - path: {} - name: {}".format(path,name))
        URL = 'http://' + config.SYNOLOGY_FILESTATION_SERVICE + '/file/rename'

        r = requests.get(url=URL, params=PARAMS)
        if r.status_code != 200:
            result = {'result' : "HTTP error - helper.rename() - status_code: {}".format(r.status_code), 'path':path,'name':name, 'status_code' : r.status_code}     
        else:
            json_result = r.json()
            if json_result['result'] == 'ok':
                result = {'result' : 'ok'}
            else:
                result = {'result' : 'error' , 'error' : '{}'.format(json.dumps(json_result['synology']))}

    result['from'] = item['info']['filename']
    if result['result'] == 'ok':
        result['to'] = name
    else:
        result['to'] = '<none>'

    #config.LOGGER.info("helper.rename() - result: {}".format(result))
    return result

