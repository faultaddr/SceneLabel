import csv
import json
import logging
import os
import sys

import open3d as o3d

try:
    import numpy as np
except:
    print("Failed to import numpy package.")
    sys.exit(-1)
try:
    import imageio
except:
    print("Please install the module 'imageio' for image processing, e.g.")
    print("pip install imageio")
    sys.exit(-1)

logger = None


def get_up_down_face_coords(obbs):
    v = [[] for i in range(len(obbs))]
    for i, obb in enumerate(obbs):
        cent = obbs[i][:3]
        hsize0 = obbs[i][-3] * 0.5
        hsize1 = obbs[i][-2] * 0.5
        hsize2 = obbs[i][-1] * 0.5
        axis0 = obbs[i][3:6]
        axis1 = obbs[i][6:9]
        axis2 = obbs[i][9:12]
        # 计算上面四个个顶点

        v[i].append(cent + axis0 * hsize0 - axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent + axis0 * hsize0 + axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent - axis0 * hsize0 + axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent - axis0 * hsize0 - axis1 * hsize1 - axis2 * hsize2)

        v[i].append(cent + axis0 * hsize0 - axis1 * hsize1 + axis2 * hsize2)

        v[i].append(cent + axis0 * hsize0 + axis1 * hsize1 + axis2 * hsize2)

        v[i].append(cent - axis0 * hsize0 - axis1 * hsize1 + axis2 * hsize2)
        v[i].append(cent - axis0 * hsize0 + axis1 * hsize1 + axis2 * hsize2)
    # 计算下面四个顶点
    # print(v[i],v[i])
    return v


def get_room_data(path):
    if path == '':
        return [], []
    file_list = os.listdir(path)
    bbox = []
    label = []
    for i, file in enumerate(file_list):
        if file.split('.')[-1] == 'obb':
            bbox_array = np.loadtxt(os.path.join(path, file))
            bbox = get_up_down_face_coords(bbox_array)

        if file.split('.')[-1] == 'txt' and file.split('.')[0].split('_')[-1] != 'result':

            with open(os.path.join(path, file), 'r') as fp:
                line_list = fp.readlines()
                for line in line_list:
                    label.append(line.strip())
    return bbox, label


def get_ply_data(path):
    if path == '':
        return []
    file_list = os.listdir(path)
    all_box_point_array = []
    for i, file in enumerate(file_list):
        if file.split('.')[-1] == 'npy':
            all_box_point_array = np.load(os.path.join(path, file), allow_pickle=True)
    return all_box_point_array


# print an error message and quit
def print_error(message, user_fault=False):
    sys.stderr.write('ERROR: ' + str(message) + '\n')
    if user_fault:
        sys.exit(2)
    sys.exit(-1)


# if string s represents an int
def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def read_label_mapping(filename, label_from='raw_category', label_to='nyu40id'):
    assert os.path.isfile(filename)
    mapping = dict()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            mapping[row[label_from]] = int(row[label_to])
    # if ints convert
    if represents_int(list(mapping.keys())[0]):
        mapping = {int(k): v for k, v in mapping.items()}
    return mapping


# input: scene_types.txt or scene_types_all.txt
def read_scene_types_mapping(filename, remove_spaces=True):
    assert os.path.isfile(filename)
    mapping = dict()
    lines = open(filename).read().splitlines()
    lines = [line.split('\t') for line in lines]
    if remove_spaces:
        mapping = {x[1].strip(): int(x[0]) for x in lines}
    else:
        mapping = {x[1]: int(x[0]) for x in lines}
    return mapping


# color by label
def visualize_label_image(filename, image):
    height = image.shape[0]
    width = image.shape[1]
    vis_image = np.zeros([height, width, 3], dtype=np.uint8)
    color_palette = create_color_palette()
    for idx, color in enumerate(color_palette):
        vis_image[image == idx] = color
    imageio.imwrite(filename, vis_image)


# color by different instances (mod length of color palette)
def visualize_instance_image(filename, image):
    height = image.shape[0]
    width = image.shape[1]
    vis_image = np.zeros([height, width, 3], dtype=np.uint8)
    color_palette = create_color_palette()
    instances = np.unique(image)
    for idx, inst in enumerate(instances):
        vis_image[image == inst] = color_palette[inst % len(color_palette)]
    imageio.imwrite(filename, vis_image)


# color palette for nyu40 labels
def create_color_palette():
    return [
        (0, 0, 0),
        (174, 199, 232),  # wall
        (152, 223, 138),  # floor
        (31, 119, 180),  # cabinet
        (255, 187, 120),  # bed
        (188, 189, 34),  # chair
        (140, 86, 75),  # sofa
        (255, 152, 150),  # table
        (214, 39, 40),  # door
        (197, 176, 213),  # window
        (148, 103, 189),  # bookshelf
        (196, 156, 148),  # picture
        (23, 190, 207),  # counter
        (178, 76, 76),
        (247, 182, 210),  # desk
        (66, 188, 102),
        (219, 219, 141),  # curtain
        (140, 57, 197),
        (202, 185, 52),
        (51, 176, 203),
        (200, 54, 131),
        (92, 193, 61),
        (78, 71, 183),
        (172, 114, 82),
        (255, 127, 14),  # refrigerator
        (91, 163, 138),
        (153, 98, 156),
        (140, 153, 101),
        (158, 218, 229),  # shower curtain
        (100, 125, 154),
        (178, 127, 135),
        (120, 185, 128),
        (146, 111, 194),
        (44, 160, 44),  # toilet
        (112, 128, 144),  # sink
        (96, 207, 209),
        (227, 119, 194),  # bathtub
        (213, 92, 176),
        (94, 106, 211),
        (82, 84, 163),  # otherfurn
        (100, 85, 144)
    ]


import inspect


def get__function_name():
    """
    :rtype: name of running method
    """
    return inspect.stack()[1][3]


def get_all_json_data(path):
    model_array = []
    if os.path.exists(path):
        with open(path)as fp:
            model_array = json.load(fp)
    return model_array


def get_s3dis_json_data(path):
    room_array = get_all_json_data(path)
    return room_array


def json_2_obj(json_str):
    return json.loads(json_str)


# ===========================Liu's dataset============================
def get_json_data(path):
    """
    :rtype: a dict that contains all info of an area
    """
    if os.path.exists(path):
        with open(path)as fp:
            model_array = json.load(fp)
            first_hier = []
            for i, model in enumerate(model_array):
                if model['parent'] == '0':
                    group = [int(x) for x in model['children']]
                    print(path)
                    print(group)
                    for g in group:
                        first_hier.append(model_array[int(g)])
            return first_hier
    else:
        return []


def get_label_info(path):
    label_list = []
    hier_data = get_json_data(path)
    if hier_data:
        for group in hier_data:
            print(' '.join([str(i) for i in group['label'][1:]]))
            label_list.append(' '.join([str(i) for i in group['label'][1:]]))
    return label_list


def get_obj_data(path):
    """
    :rtype: vertices:np_array,triangles:np_array,normals:np_array
    """
    mesh = o3d.io.read_triangle_mesh(path)
    return np.asarray(mesh.vertices).tolist(), np.asarray(mesh.triangles).tolist(), np.asarray(
        mesh.vertex_normals).tolist()


# ===========================Liu's dataset============================

# ===========================ply data============================
def get_ply_data_origin(path):
    point_cloud = o3d.io.read_point_cloud(path)
    return np.asarray(point_cloud.points), np.asarray(point_cloud.colors)


# ===========================ply data============================
def get_logger():
    global logger
    if logger is None:
        # logger settings
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler("log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)

        logger.addHandler(handler)
        logger.addHandler(console)
    return logger
