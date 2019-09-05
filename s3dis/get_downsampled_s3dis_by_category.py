# coding =utf-8
import os
import shutil
import json

ROOT_PATH = '/data/S3DIS/Stanford3dDataset_v1.2_Aligned_Version/gt'


def get_s3dis_path(json_path):
    # area_name=json_path.split('-')[0].split('/')[-1]
    # name=''.join(json_path.split('-')[1].split('.')[0]).replace('copy','color01.txt')
    # print('name',name)
    # gt_path=os.path.join(ROOT_PATH,area_name,'_'.join(name.split('_')[0:2]),'Annotations',name)
    # print(gt_path)
    dst_path = './gt_data'
    if not os.path.exists(dst_path):
        os.mkdir('./gt_data')
    # shutil.copy(gt_path,dst_path)
    with open(json_path)as fp:
        data = json.load(fp)
        point_path_list = []
        for d in data:
            if d['parent'] == -1:
                point_path_list.extend(d['path'])
        for point_path in point_path_list:

            downsampled_path = '/'.join(point_path.split('/')[0:4]) + '/gt/' + '/'.join(point_path.split('/')[4:])
            downsampled_path = downsampled_path.replace('.txt', '_color01.txt')
            new_path = './gt_data/' + '/'.join(point_path.split('/')[4:-1])
            print()
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            shutil.copy(downsampled_path, new_path + '/' + point_path.split('/')[-1])
