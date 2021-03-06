#!/usr/bin/env python3

# Make sure you have python3 installed.
# Ensure that the json_formatter is kept in Tools with this script. They must be in the same folder!
# For Windows:
# Using command prompt type "python barrellength_volume.py"
# For Max OS X or Linux:
# Swap any "\\" with "/", then run the script as in windows.

import json
import os


def gen_new(path):
    change = False
    with open(path, "r") as json_file:
        try:
            json_data = json.load(json_file)
        except UnicodeDecodeError:
            print("UnicodeDecodeError in {0}".format(path))
            return None
        for jo in json_data:
            # We only want JsonObjects
            if type(jo) is str:
                continue
            if not jo.get('name'):
                continue
            if type(jo['name']) == dict:
                continue
            if jo['type'] not in ['GENERIC', 'AMMO', 'MAGAZINE', 'ARMOR', 'PET_ARMOR', 'BOOK',
                                  'BIONIC_ITEM', 'COMESTIBLE', 'GUN', 'GUNMOD', 'BATTERY', 'TOOL',
                                  'SPELL', 'ENGINE', 'WHEEL', 'vitamin', 'ITEM_CATEGORY', 'bionic',
                                  'npc_class', 'mission_definition', 'TOOLMOD', 'mutation', 'fault',
                                  'martial_art', 'MONSTER', 'proficiency', 'tool_quality',
                                  'map_extra', 'skill', 'TOOL_ARMOR', 'item_action', 'vehicle_part']:
                continue
            if jo.get('name_plural'):
                if jo['name'] == jo['name_plural']:
                    name_obj = {'str_sp': jo['name']}
                else:
                    name_obj = {'str': jo['name'], 'str_pl': jo['name_plural']}
                jo['name'] = name_obj
                del jo['name_plural']
                change = True
            else:
                name_obj = {'str': jo['name']}
                jo['name'] = name_obj
                change = True

    return json_data if change else None


def change_file(json_dir):
    for root, directories, filenames in os.walk("..\\{0}".format(json_dir)):
        for filename in filenames:
            path = os.path.join(root, filename)
            if path.endswith(".json"):
                new = gen_new(path)
                if new is not None:
                    with open(path, "w") as jf:
                        json.dump(new, jf, ensure_ascii=False)
                    os.system(".\\json_formatter.exe {0}".format(path))


if __name__ == "__main__":
    json_dir = input("What directory are the json files in? ")
    change_file(json_dir)
