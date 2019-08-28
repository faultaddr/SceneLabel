#coding = utf-8
import json
import os

ROOT_PATH='./result'
def analysis():
    area_dict={}
    json_path_list=[os.path.join(ROOT_PATH,x)for x in os.listdir(ROOT_PATH)]
    for json_path in json_path_list:
        with open(json_path)as fp:
            json_data=json.load(fp)
            for data in json_data:
                if data['parent']==-1:
                    if 'area' not in data['label']and 'clutter'not in data['label']:
                        print(data['label'],json_path)
                    if data['label']not in area_dict.keys():
                        area_dict[data['label']]=1
                    else:
                        area_dict[data['label']]+=1
    print(area_dict)

analysis()
