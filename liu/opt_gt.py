# coding=utf-8
import json
import os


class Gt:
    newModel = 0
    parent = -1
    is_meaningful = 'yes'
    children = []
    leaf_group = []
    next_rep = -1
    label = ()
    rule = ''
    unary_descriptor_ZAligned = []
    binary_descriptor_BBoxIn3D = []
    proxy_box = []
    confidence = 1
    collada_label = None

    def __init__(self, newModel=None, parent=None, is_meaningful=None, children=None, leaf_group=None, next_rep=None,
                 label=None, rule=None,
                 unary_descriptor_ZAligned=None, binary_descriptor_BBoxIn3D=None, proxy_box=None, confidence=None,
                 collada_label=None):
        self.newModel = newModel
        self.parent = parent
        self.is_meaningful = is_meaningful
        self.children = children
        self.leaf_group = leaf_group
        self.next_rep = next_rep
        self.label = label
        self.rule = rule
        self.unary_descriptor_ZAligned = unary_descriptor_ZAligned
        self.binary_descriptor_BBoxIn3D = binary_descriptor_BBoxIn3D
        self.proxy_box = proxy_box
        self.confidence = confidence
        self.collada_label = collada_label


def obj_2_json(obj):
    return {
        "newModel": obj.newModel,
        "parent": obj.parent,
        "is_meaningful": obj.is_meaningful,
        "children": obj.children,
        "leaf_group": obj.leaf_group,
        "next_rep": obj.next_rep,
        "label": obj.label,
        "rule": obj.rule,
        "unary_descriptor_ZAligned": obj.unary_descriptor_ZAligned,
        "binary_descriptor_BBoxIn3D": obj.binary_descriptor_BBoxIn3D,
        "proxy_box": obj.proxy_box,
        "confidence": obj.confidence,
        "collada_label": obj.collada_label
    }


def read_hier(path, i):
    with open(path)as fp:
        gt_list = []
        gt = Gt()
        for line in fp.readlines():
            if line.split()[0] == 'newModel':
                gt = Gt(newModel=int(line.split()[1]))
            elif line.split()[0] == 'parent':
                gt.parent = line.split()[1]
            elif line.split()[0] == 'is_meaningful':
                gt.is_meaningful = line.split()[1]
            elif line.split()[0] == 'children':
                gt.children = line.split()[1:]
            elif line.split()[0] == 'leaf_group':
                gt.leaf_group = line.split()[1:]
            elif line.split()[0] == 'next_rep':
                gt.next_rep = line.split()[1]
            elif line.split()[0] == 'label':
                gt.label = line.split()[1:]
            elif line.split()[0] == 'rule':
                gt.rule = line.split()[1:]
            elif line.split()[0] == 'unary_descriptor':
                gt.unary_descriptor_ZAligned = line.split()[2:]
            elif line.split()[0] == 'binary_descriptor':
                gt.binary_descriptor_BBoxIn3D = line.split()[2:]
            elif line.split()[0] == 'proxy_box':
                gt.proxy_box = line.split()[1:]
            elif line.split()[0] == 'confidence':
                gt.confidence = line.split()[1]
            elif line.split()[0] == 'collada_label':
                gt.collada_label = line.split()[1]
                gt_list.append(gt)
        if not os.path.exists('./liu_json'):
            os.mkdir('./liu_json')
        with open('./liu_json/%s.json' % i, 'w', encoding='utf-8')as json_data:
            json.dump(gt_list, json_data, default=obj_2_json)


def opt_all_data(path):
    for i, hier in enumerate(os.listdir(path)):
        read_hier(os.path.join(path, hier), hier.split('.')[0])


opt_all_data('/data/Liu/scenegraphs/cleaned/bedroom/gtSceneGraphs/')
