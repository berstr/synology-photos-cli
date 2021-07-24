import json
import re
from datetime import datetime


import config
from modules.synology import items as synology_items
from modules.menu import process_items as menu_process_items
from modules.helper import display_items as helper_display_items


def menue_main(id,foldername,parent_id):
    UPDATE_ITEMS_LIST=False
    ITEMS_LIST = get_folder_items(id,foldername)
    if ITEMS_LIST==None:
        return

    while True:
        if UPDATE_ITEMS_LIST:
            ITEMS_LIST = get_folder_items(id,foldername)
            if ITEMS_LIST==None:
                return
            else:
                UPDATE_ITEMS_LIST=False

        helper_display_items.display_items(foldername, ITEMS_LIST)

        print("")
        print('s<#>          -> select 1 item')
        print('s<#>,<#>, ... -> select multiple items')
        print('s<#>-<#>      -> select range of items')
        print('sp<pattern>   -> select based on filter')
        print("sa<#>         -> select all items")
        print("e             -> return to sub-folder menu")
        print('')
        user = input("=> ")
        if user == "e":
            return
        else:
            pattern = '^s([0-9]+)$'
            m = re.match(pattern,user)
            selected_items = None
            if m != None:
                selected_items = filter_list_single_item(ITEMS_LIST,int(m.group(1)))
            else:
                pattern = '^s([0-9]+)(,[0-9]+)+$'
                m = re.match(pattern,user)
                if m != None:
                    selections = user[1:].split(',')
                    selected_items = filter_list_selections(ITEMS_LIST,selections)
                else:
                    pattern = '^s([0-9]+)-([0-9]+)$'
                    m = re.match(pattern,user)
                    if m != None:
                        print('select range of items: {} - {}'.format(m.group(1),m.group(2)))
                        selected_items = filter_list_range(ITEMS_LIST,int(m.group(1)),int(m.group(2)))
                    else:
                        pattern = '^sp(.*)$'
                        m = re.match(pattern,user)
                        if m != None:
                            print('select based on filter: {}'.format(m.group(1)))
                            selected_items = filter_list_pattern(ITEMS_LIST,m.group(1))
            if selected_items != None and len(selected_items)>0 :
                menu_process_items.menu_main(foldername,selected_items)
                UPDATE_ITEMS_LIST=True


def get_folder_items(folder_id,foldername):
    result = None
    folder_items = synology_items.get_folder_items(folder_id)
    if folder_items['result'] == 'ok':
        result = folder_items['items']
    else:
        config.LOGGER.fatal('Error in getting items for folder [id: {} , name: {}]'.format(folder_id,foldername))
        config.LOGGER.fatal('Error Details: {}]'.format(json.dumps(folder_items)))
    return result


def filter_list_selections(items,selections):
    result = []
    for selection in selections:
        if int(selection) < 1 or int(selection) > len(items):
            print('Error: invalid selection: {} - valid: 1-{}'.format(selections,len(items)))
            return result
    for selection in selections:
        result.append(items[int(selection)-1])
    return result

def filter_list_single_item(items,single_item):
    result = []
    if single_item < 1 or single_item > len(items)+1:
            print('Error: invalid selection: {} - valid: 1-{}'.format(single_item,len(items)))
    else:
        result.append(items[single_item-1])
    return result


def filter_list_range(items,first,last):
    result = []
    if first < 1 or last < 1  or first > last or first > len(items) or last > len(items):
        print('Error: invalid selection: {}-{} - valid: 1-{}'.format(first,last,len(items)))
    else:
        result = items[first-1:last]
    return result

def filter_list_pattern(items,pattern):
    result = []
    for item in items:
        m = item['filename'].find(pattern)
        if m != -1:
            result.append(item)
    if len(result) == 0:
        print('Note: none of the items matches the pattern: {}'.format(pattern))
    return result

'''
def menue_items_list(id, foldername,parent_id):
    global current_items_list
    result = items_get(id, foldername)
    print('Items in {}:'.format(foldername))
    if result['result'] == 'ok':
        current_items_list = []
        if len(result['items']) == 0:
            print('  [-]  <EMPTY>')
        else:
            i=1
            for item in result['items']:
                print('  [{}]  {}'.format(i,item['filename']))
                current_items_list.append(item)
                i = i + 1
    else:
        config.LOGGER.fatal('Error in getting items for folder [id: {} , name: {}]'.format(id,foldername))
        config.LOGGER.fatal('Error Details: {}]'.format(json.dumps(result)))
'''

