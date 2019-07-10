# coding=utf-8

import json
import os
import sys

try:
    import numpy as np
except:
    print("Failed to import numpy package")
    sys.exit(-1)


def read_aggregation(filename):
    print(filename)
    assert os.path.isfile(filename)
    object_id_to_segs = {}
    label_to_segs = {}
    with open(filename) as f:
        data = json.load(f)
        num_objects = len(data['segGroups'])
        for i in range(num_objects):
            object_id = data['segGroups'][i]['objectId'] + 1  # instance ids should be 1-indexed
            label = data['segGroups'][i]['label']
            segs = data['segGroups'][i]['segments']
            object_id_to_segs[object_id] = segs
            if label in label_to_segs:
                label_to_segs[label].extend(segs)
            else:
                label_to_segs[label] = segs
    return object_id_to_segs, label_to_segs


def read_segmentation(filename):
    assert os.path.isfile(filename)
    seg_to_verts = {}
    with open(filename) as f:
        data = json.load(f)
        num_verts = len(data['segIndices'])
        for i in range(num_verts):
            seg_id = data['segIndices'][i]
            if seg_id in seg_to_verts:
                seg_to_verts[seg_id].append(i)
            else:
                seg_to_verts[seg_id] = [i]
    return seg_to_verts, num_verts


'''
object_id_to_segs: 例如 id =1 对应着 哪些 segs
label_to_segs: 例如 floor 对应着 哪些 segs
----------------------------
seg_to_verts: 例如 
num_verts: 多少个verts
'''


def get_combined_ids(agg_path, seg_path):
    object_id_to_segs, label_to_segs = read_aggregation(agg_path)
    seg_to_verts, num_verts = read_segmentation(seg_path)

    label_ids = np.zeros(shape=(num_verts), dtype=np.uint32)

    import core.util as util

    label_map = util.read_label_mapping('../data/scannetv2-labels.combined.tsv', label_from='raw_category',
                                        label_to='nyu40id')

    for label, segs in label_to_segs.items():
        label_id = label_map[label]
        for seg in segs:
            verts = seg_to_verts[seg]
            label_ids[verts] = label_id
    instance_ids = np.zeros(shape=(num_verts), dtype=np.uint32)
    for object_id, segs in object_id_to_segs.items():
        for seg in segs:
            verts = seg_to_verts[seg]
            instance_ids[verts] = object_id
    return label_ids * 1000 + instance_ids
# 其实就是把 instance 和label 结合起来
# util_3d.export_ids("./test.txt", label_ids * 1000 + instance_ids)
