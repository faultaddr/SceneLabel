from plyfile import PlyData, PlyElement
import numpy as np
import os
from core import generate_instance_id
from core.new_parser import FitObb, save_obb
import sys

id_mapping_realation = {0: 'none', 1: 'wall', 2: 'floor', 3: 'cabinet', 4: 'bed', 5: 'chair', 6: 'sofa', 7: 'table',
                        8: 'door', 9: 'window', 10: 'bookshelf', 11: 'picture', 12: 'counter', 13: 'blinds', 14: 'desk',
                        15: 'shelves', 16: 'curtain', 17: 'dresser', 18: 'pillow', 19: 'mirror', 20: 'floor mat',
                        21: 'clothes', 22: 'ceiling', 23: 'books', 24: 'refridgerator', 25: 'television', 26: 'paper',
                        27: 'towel', 28: 'shower curtain', 29: 'box', 30: 'whiteboard', 31: 'person', 32: 'nightstand',
                        33: 'toilet', 34: 'sink', 35: 'lamp', 36: 'bathtub', 37: 'bag', 38: 'otherstructure',
                        39: 'otherfurniture', 40: 'otherprop'}

'''
path: 文件名数组 ply seg agg 
'''


def opt_ply(path):
    label_instance_list = generate_instance_id.get_combined_ids(seg_path=path[1], agg_path=path[2])
    ply_file = PlyData().read(path[0])
    v_list = np.array([list(x) for x in ply_file.elements[0]])
    coords = np.ascontiguousarray(v_list[:, :3] - v_list[:, :3].mean(0))
    colors = np.ascontiguousarray(v_list[:, 3:6]) / 127.5 - 1

    w = np.array(ply_file.elements[0]['label'])
    # ply_file.elements[0]['label']=label_instance_list
    # PlyData.write(ply_file)
    # sys.exit(0)

    dict_label = {}
    for _i, i in enumerate(w):
        if i == 0:
            pass
        else:
            dict_label[i] = True

    dict_w = {}
    colors_w = {}
    for i, _w in enumerate(label_instance_list):
        if _w in dict_w.keys():
            dict_w[_w].append(coords[i].tolist())
            colors_w[_w].append(colors[i].tolist())
        else:
            dict_w[_w] = []
            colors_w[_w] = []
            dict_w[_w].append(coords[i].tolist())
            colors_w[_w].append(colors[i].tolist())
    result = []
    for (key, value) in dict_w.items():
        # print(key,'\n',value)
        result.append((key, FitObb(np.array(value))))
    return result, dict_w, colors_w


def save_obb_label(path, label_list):
    with open(path, 'w')as fp:
        for i, label in enumerate(label_list):
            if i == len(label_list) - 1:
                fp.write(str(i) + ':' + str(label))
            else:
                fp.write(str(i) + ':' + str(label) + '\n')


def save_ply_part(path, coords_colors_list):
    np.save(path, coords_colors_list)


def opt_obb(path, for_save=False):
    point_group_result, coords_dict, colors_dict = opt_ply(path)
    value_list = []
    label_list = []
    coords_color_list = []
    valid_label_list = ['floor', 'cabinet', 'bed', 'chair', 'sofa', 'table', 'door', 'window', 'bookshelf', 'picture',
                        'counter', 'desk', 'curtain', 'refrigerator', 'shower curtain', 'toilet', 'sink', 'bathtub',
                        'otherfurniture']
    for (key, value) in point_group_result:
        # print(key)
        label = id_mapping_realation[int(key / 1000)]
        if key == 0:
            continue
        if label == 'wall' or label == 'ceiling':  # or label not in valid_label_list:
            continue
        if label not in valid_label_list:
            continue
        value_list.append(value)
        label_list.append(label)

        coords_dict[key].extend(colors_dict[key])
        coords_color_list.append(np.array(coords_dict[key]))
    if for_save:
        save_obb(str(path[0].split('.')[0]) + '_value.obb', value_list)
        save_obb_label(path[0].split('.')[0] + '_label.txt', label_list)
        save_ply_part(path[0].split('.')[0] + '_part', np.array(coords_color_list))
    return label_list


def main(path, for_save=True):
    scan_dir_list = os.listdir(path)
    for i, scan_dir_list in enumerate(scan_dir_list):
        print('-----', i)
        path = os.path.join(original_path, scan_dir_list)
        mesh_file = os.path.join(path, scan_dir_list + '_vh_clean_2.labels.ply')
        agg_file = os.path.join(path, scan_dir_list + '_vh_clean.aggregation.json')
        seg_file = os.path.join(path, scan_dir_list + '_vh_clean_2.0.010000.segs.json')
        try:
            opt_obb([mesh_file, seg_file, agg_file], for_save)
        except Exception:
            print(Exception)


if __name__ == '__main__':
    original_path = '/data/scans/scans/'
    main(original_path, True)
