
def display_items(foldername, items):
    #for item in items:
    #    print(item)
    #    print('--------------')
    max_filename_len = 6
    max_tag_len = 4
    max_camera_len = 6
    for item in items:
        if len(item['info']['filename']) > max_filename_len:
            max_filename_len = len(item['info']['filename'])
        if len(item['info']['additional']['exif']['camera']) > max_camera_len:
            max_camera_len = len(item['info']['additional']['exif']['camera'])
        temp=0
        for tag in item['info']['additional']['tag']:
            if len(tag['name']) > 0:
                temp = temp + len(tag['name']) + 1
            if temp > max_tag_len:
                max_tag_len = temp
    i = 1
    print('Folder:  {}'.format(foldername))
    print('')
    format_string = '[{:>3}] | {:>8} |  {:' + str(max_filename_len) + '} | {:^10} | {:20} | {:^12} | {:' + str(max_camera_len) + '} | {:10} | {:' + str(max_tag_len) + '} | {}'
    print(format_string.format('','id','name','valid name','date','time synced','camera','gps','tags','description'))
    print('{}'.format('-'*185))
    for item in items:
        valid_filename = 'not valid'
        filename_timevalue = 'not synced'
        if item['filename_analysis']['result'] == 'ok':
            valid_filename = 'valid'
            if item['filename_analysis']['time_synced'] == 'true':
                filename_timevalue = 'synced'
        has_gps = 'no gps'
        if 'gps' in item['info']['additional'].keys():
            has_gps = 'has gps'
        tags = []
        for tag in item['info']['additional']['tag']:
            tags.append(tag['name'])
        print(format_string.format(i,item['id'],item['info']['filename'],valid_filename, item['date']['date'],filename_timevalue, item['info']['additional']['exif']['camera'],has_gps, ','.join(tags),item['info']['additional']['description']))
        i = i + 1