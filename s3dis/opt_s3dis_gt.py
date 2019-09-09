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
    print(path)
    instance_dir = os.listdir(os.path.join(path, 'Annotations'))

    gt_list = []
    count = 0
    for i, instance in enumerate(instance_dir):
        print(instance)
        if '.txt' in instance:
            gt = GT()
            print(instance)
            label = instance.split('_')[0]
            parent = -1
            children = []
            instance_path = [os.path.join(os.path.join(path, 'Annotations'), instance)]
            gt.id = count
            gt.parent = parent
            gt.children = children
            gt.label = label
            gt.path = instance_path
            gt_list.append(gt)
            count += 1
        print(path.split('/'))
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    with open(json_path + '/%s' % path.split('/')[-2] + '-%s.json' % path.split('/')[-1], 'w')as json_data:
        json.dump(gt_list, json_data, default=obj_2_json)


def opt_all_data(path, json_path):
    room_list = []
    for d in os.listdir(path):
        room_list.append(os.path.join(path, d))
    # area1 area2
    for i, room in enumerate(room_list):
        for s_r in os.listdir(room):
            if os.path.isdir(os.path.join(room, s_r)):
                translate_2_json(os.path.join(room, s_r), json_path)


def main(path, json_path):
    opt_all_data(path, json_path)


# opt_all_data('/data/S3DIS/Stanford3dDataset_v1.2_Aligned_Version/Area_6/')
def analysis_json(json_path):
    with open(json_path)as fp:
        json_data = json.load(fp)
        count = json_data[-1]['id']
        if not count == len(json_data) + 1:
            print(json_path)


def analysis_all(path):
    file_list = os.listdir(path)
    for file in file_list:
        analysis_json(os.path.join(path, file))


# analysis_all('./result_all')
