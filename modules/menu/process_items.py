import json
import re

import config
from modules.synology import items as synology_items
from modules.helper import rename as helper_rename
from modules.helper import time as helper_time
from modules.helper import display_items as helper_display_items



def menu_main(foldername, items):

    REFRESH_ITEMS=False
    ITEMS_LIST = items

    while True:
        if REFRESH_ITEMS:
            result = synology_items.refresh_items(items)
            if result['result'] != 'ok':
                print('FATAL: could not refesh list of selected items from folder {}'.format(foldername))
                print('{}'.format(result))
                return
            else:
                ITEMS_LIST = result['items'] 
                REFRESH_ITEMS=False

        helper_display_items.display_items(foldername, ITEMS_LIST)

        print("")
        print('r  -> rename automatically - based on date taken')
        print('rm -> rename manually')
        print('d  -> set date taken automatically - based on filename')
        print('dm -> set date taken manually')
        print('i  -> print item details')
        print('e  -> return to previous menu')
        user = input("=> ")
        if user == "e":
            return
        elif user == 'd':
            __date_taken_auto(ITEMS_LIST)
            REFRESH_ITEMS=True
        elif user == 'r':
            __rename_auto(foldername,ITEMS_LIST)
            REFRESH_ITEMS=True
        elif user == 'i':
            __item_details(foldername,ITEMS_LIST)

def __item_details(foldername,items):
    i = 0
    while i < len(items):
        item = items[i]
        print('{}'.format(json.dumps(item,indent=2)))
        print('')
        i = i + 1
        if i < len(items):
            user = input('next item => ')
    print('')
    user = input('Enter to return to menu =>')
    print('\n------------------------------\n')

def __date_taken_auto(items):
    print('')
    print('please confirm the change of item date with:  [ Y ]   (<Enter> or any other input will exit and return to previous memu)')
    user = input('Date change for {} items ==> '.format(len(items)))
    if user != "Y":
        print('')
        print('\n------------------------------\n')
        return

    processed_items = []
    i = 0
    while i < len(items):
        item = items[i]
        print('.',end='',flush=True)
        result = helper_time.set_time_from_filename(item)
        processed_items.append(result)
        i = i + 1
    print('')
    i = 1
    print('')
    print('###  Result of updating date taken based on filename  [SUCCESS , NOTE, ERROR] ###')
    print('')
    for pi in processed_items:
        if pi['result'] == 'ok':
            print('[{:>3}] SUCCESS - filename: {:25}  ->  new date: {}'.format(i,pi['filename'],pi['date']))
        elif pi['result'] == 'info':
            print('[{:>3}] NOTE    - filename: {:25}  ->  new date: {:25} - {}'.format(i,pi['filename'],pi['date'], pi['info']))
        elif pi['result'] == 'error':
            print('[{:>3}] ERROR   - filename: {:25}  ->  new date: {:25} - {}'.format(i,pi['filename'],pi['date'], pi['error']))
        else:
            print('[{:>3}] ERROR   - filename: {:25}  ->  new date: {:25} - {}'.format(i,pi['filename'],pi['date'], pi['result']))
        i=i+1
    print('')
    user = input('Enter to list all items =>')
    print('\n------------------------------\n')


def __rename_auto(foldername,items):
    print('')
    print('please confirm the renaming of photo items with:  [ Y ]   (<Enter> or any other input will exit and return to previous memu)')
    user = input('Rename {} items ==> '.format(len(items)))
    if user != "Y":
        print('')
        print('\n------------------------------\n')
        return
    processed_items = []
    i = 0
    while i < len(items):
        item = items[i]
        print('.',end='',flush=True)
        rename_result = helper_rename.rename_to_date(foldername,item)
        processed_items.append(rename_result)
        i = i + 1
    print('')
    i = 1
    print('')
    print('###  Result of renaming file to date taken  [SUCCESS , NOTE, ERROR]  ###')
    print('')

    for pi in processed_items:
        if pi['result'] == 'ok':
            print('[{:>3}] SUCCESS - from: {:35} -> to: {}'.format(i,pi['from'],pi['to']))
        elif pi['result'] == 'info':
            print('[{:>3}] NOTE    - from: {:35} -> to: {:25} - {}'.format(i,pi['from'],pi['to'], pi['info']))
        elif pi['result'] == 'error':
            print('[{:>3}] ERROR   - from: {:35} -> to: {:25} - {}'.format(i,pi['from'],pi['to'], pi['error']))
        else:
            print('[{:>3}] ERROR   - from: {:35} -> to: {:25} - {}'.format(i,pi['from'],pi['to'], pi['result']))
        i=i+1
    print('')
    user = input('Enter to list all items =>')
    print('\n------------------------------\n')

'''
def __print_items(foldername, items):
    i = 1
    print('Selected items in: {}'.format(foldername))
    print('')
    format_string = '[{:>3}] {:>8} |  {:>20} | {:>5} | {:>12} | {:>18} | {}'
    print(format_string.format('','id','date','GPS','name syntax','name time-synced','name'))
    print('-------------------------------------------------------------------------------------------------------------')
    for item in items:
        valid_filename = 'not valid'
        filename_timevalue = 'false'
        if item['filename_analysis']['result'] == 'ok':
            valid_filename = 'valid'
            if item['filename_analysis']['time_synced'] == 'true':
                filename_timevalue = 'true'
        has_gps = 'false'
        if 'gps' in item['info']['additional'].keys():
            has_gps = 'true'
        print(format_string.format(i,item['id'], item['date']['date'],has_gps,valid_filename,filename_timevalue,item['info']['filename']))
        i = i + 1
'''
