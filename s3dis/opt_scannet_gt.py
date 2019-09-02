# coding =utf-8
import json
import os


class GT:
    id = 0
    parent = -1
    children = []
    label = ''
    path = ''

    def __init__(self, id=None, parent=None, children=None, label=None, path=None):
        self.id = id
        self.parent = parent
        self.children = children
        self.label = label
        self.path = path


def obj_2_json(pc):
    return {
        "id": pc.id,
        "parent": pc.parent,
        "children": pc.children,
        "label": pc.label,
        "path": pc.path
    }


def translate_2_json(path, json_path):
    print(json_path)
    instance_dir = os.listdir(path)
    gt_list = []
    for i, instance in enumerate(instance_dir):
        print(instance)
        if '.ply' in instance:
            gt = GT()
            print(instance)
            label = instance.split('_')[0]
            parent = -1
            children = []
            instance_path = [os.path.join(path, instance)]
            gt.id = i
            gt.parent = parent
            gt.children = children
            gt.label = label
            gt.path = instance_path
            gt_list.append(gt)
        print(path.split('/'))
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    with open(json_path + '/%s.json' % path.split('/')[-1], 'w')as json_data:
        json.dump(gt_list, json_data, default=obj_2_json)


def opt_all_data(path, json_path):
    for i, room in enumerate(os.listdir(path)):
        if os.path.isdir(os.path.join(path, room)):
            translate_2_json(os.path.join(path, room), json_path)


def main(path, json_path):
    opt_all_data(path, json_path)
