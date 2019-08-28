import os
import shutil
import get_downsampled_s3dis_by_category as gdsbc


ROOT_PATH='./s3dis_json/'


def get_path_by_category(category):
    json_list=[]
    area_dir=os.listdir(ROOT_PATH)
    print(area_dir)
    for dir_name in area_dir:
        dir_path=os.path.join(ROOT_PATH,dir_name)
        if os.path.isdir(dir_path):
            file_list=os.listdir(dir_path)
            for file_name in file_list:
                if category in file_name and 'copy' in file_name:
                    json_list.append(os.path.join(dir_path,file_name))
    return json_list

def main():
    category='hallway'
    json_list=get_path_by_category(category)
    print(json_list)
    new_path='./result'
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    for json_data in json_list:
        name=json_data.split('/')[-1]
        area_name=json_data.split('/')[-2]
        new_name=area_name+'-'+name
        new_json_path=os.path.join(new_path,new_name)
        shutil.copy(json_data,new_json_path)
        gdsbc.get_s3dis_path(new_json_path)
main()
