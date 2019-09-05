# coding=utf-8
import os
import json

ROOT_PATH = './result_all'


def change_path():
    for json_path in os.listdir(ROOT_PATH):
        print(json_path)
        with open(os.path.join(ROOT_PATH, json_path))as fp:
            json_data = json.load(fp)
            for data in json_data:
                print(data['path'])
                for i, _ in enumerate(data['path']):
                    data['path'][i] = './gt_data/' + '/'.join(data['path'][i].split('/')[4:])
            fp.flush()
            fp.close()
        with open(os.path.join(ROOT_PATH, json_path), 'w')as fp:

            json.dump(json_data, fp)


change_path()
