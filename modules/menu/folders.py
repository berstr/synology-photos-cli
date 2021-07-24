import requests
import json
import os
import re

import config
from modules.menu import items
from modules.synology import folders as synology_folders


def menue_main():

    FOLDER_TREE = {1:{'id':1,'name':'/','parent':None}}
    CURRENT_FOLDER = FOLDER_TREE[1]
    PARENT_FOLDER = None
    SUBFOLDERS_LIST_UPDATE = True

    while True:

        if SUBFOLDERS_LIST_UPDATE:
            SUBFOLDERS_LIST = get_subfolders(CURRENT_FOLDER['id'], CURRENT_FOLDER['name'])

        if SUBFOLDERS_LIST_UPDATE == False:
            SUBFOLDERS_LIST_UPDATE = True

        # print('>>>>>>>>>>>>>>')
        # for f in SUBFOLDERS_LIST:
        #     print(f)
        # print('  ............')
        # for f in FOLDER_TREE:
        #     print(FOLDER_TREE[f])
        # print('current folder: id={}  -  name={}  -  parent={}'.format(CURRENT_FOLDER['id'],CURRENT_FOLDER['name'],CURRENT_FOLDER['parent']))
        # print('<<<<<<<<<<<<<<')
        #print('par folder: {}'.format(PARENT_FOLDER))
        #print('cur folder: {}'.format(CURRENT_FOLDER))
        #print('subfolders: {}'.format(SUBFOLDERS_LIST))

        if SUBFOLDERS_LIST==None:
            return

        display_subfolders(CURRENT_FOLDER['name'],SUBFOLDERS_LIST)
        print('')

        if len(SUBFOLDERS_LIST) > 0:
            print('{:6} -> {}'.format('f <#>','list sub-folders'))
            print('{:6} -> {}'.format('i <#>','list items in folder'))
        print('{:6} -> {}'.format('/','return to root, top level folder'))
        if CURRENT_FOLDER['parent'] != None:
            print('{:6} -> {}'.format('..','return to parent folder: {}'.format(FOLDER_TREE[CURRENT_FOLDER['parent']]['name'])))
        print('{:6} -> {}'.format('e','return to previous menu'))
        print('')
        user = input("=> ")
        if user == "e":
            return
        elif user == '/':
            CURRENT_FOLDER = FOLDER_TREE['1']
            PARENT_FOLDER = None
        elif user == '..':
            if CURRENT_FOLDER['parent'] != None:
                CURRENT_FOLDER = FOLDER_TREE[CURRENT_FOLDER['parent']]
                if CURRENT_FOLDER['parent'] == None:
                    PARENT_FOLDER = None
                else:
                    PARENT_FOLDER = FOLDER_TREE[CURRENT_FOLDER['parent']]
            else:
                PARENT_FOLDER = None
        else:
            m=re.match('^([if]) *([0-9]+)$',user)
            if m != None:
                if m.group(1) == 'i':
                    folder_num = int(m.group(2))
                    if folder_num == 0:
                        #print('item selection: folder: f {}'.format(CURRENT_FOLDER))
                        items.menue_main(CURRENT_FOLDER['id'],CURRENT_FOLDER['name'],CURRENT_FOLDER['parent'])
                    elif folder_num > 0 and folder_num <= len(SUBFOLDERS_LIST)-1:
                        folder_num = folder_num - 1
                        #print('item selection: folder: f {}'.format(SUBFOLDERS_LIST[folder_num]))
                        items.menue_main(SUBFOLDERS_LIST[folder_num]['id'],SUBFOLDERS_LIST[folder_num]['name'],SUBFOLDERS_LIST[folder_num]['parent'])
                elif m.group(1) == 'f':
                    folder_num = int(m.group(2))
                    if folder_num > 0 and folder_num <= len(SUBFOLDERS_LIST)-1:
                        folder_num = folder_num - 1
                        PARENT_FOLDER = FOLDER_TREE[CURRENT_FOLDER['id']]
                        #print('folder selection: folder: f {}'.format(SUBFOLDERS_LIST[folder_num]))
                        id = SUBFOLDERS_LIST[folder_num]['id']
                        parent = SUBFOLDERS_LIST[folder_num]['parent']
                        FOLDER_TREE[id] = {'id':id,'name':SUBFOLDERS_LIST[folder_num]['name'],'parent':parent}                        
                        CURRENT_FOLDER = FOLDER_TREE[id]
                    else:
                        SUBFOLDERS_LIST_UPDATE = False
                else:
                    SUBFOLDERS_LIST_UPDATE = False
            else:
                SUBFOLDERS_LIST_UPDATE = False



def display_subfolders(foldername,subfolders):
    print('')
    print('Sub-Folders of:  [ {} ]'.format(foldername))
    print('')
    if len(subfolders) == 0:
        print('  [0]  <current folder>')
    else:
        print('  [{:3}]  <current folder>'.format(0))
        i=0
        while i < len(subfolders):
            print('  [{:3}]  {}'.format(i+1,subfolders[i]['name']))
            i = i + 1

    
def get_subfolders(folder_id,foldername):
    result = None
    subfolders = synology_folders.folders_get(folder_id)
    if subfolders['result'] == 'ok':
        result = subfolders['folders']
    else:
        config.LOGGER.fatal('Error in getting subfolders in folder [id: {} , name: {}]'.format(folder_id,foldername))
        config.LOGGER.fatal('Error Details: {}]'.format(json.dumps(subfolders)))
    return result    

