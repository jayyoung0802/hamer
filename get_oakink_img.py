import os
import json
import numpy as np
import re
import glob

scene_list = [
    ("scene_01__A003++seq__783bd4550274783193c3__2023-04-15-09-58-39", 0, 'right'),
    ("scene_01__A003++seq__783bd4550274783193c3__2023-04-15-09-58-39", 1, 'left'),
    ("scene_01__A003++seq__d7c333b80728391e47c7__2023-04-16-10-44-48", 1, 'right'),
    ("scene_01__A004++seq__4b8138c463637dc9543d__2023-04-28-19-43-57", 0, 'left'),
    ("scene_01__A004++seq__4b8138c463637dc9543d__2023-04-28-19-43-57", 1, 'left'),
    ("scene_04__A008++seq__f93352845016c27d0fdc__2023-05-09-19-52-25", 1, 'left'),
]

def parse_entry(entry):
    # 正则匹配整数或 None
    matches = re.findall(r'\d+|None', entry)
    # 将数字转为 int，None 保留为 None
    return [int(m) if m.isdigit() else None for m in matches]

def group_into_tuples(parsed):
    # 根据长度将数据变成 [(a,b), (c,d)] 或 [None, (c,d)] 等结构
    if len(parsed) == 2:
        return [None if x == None else int(x) for x in parsed]
    elif len(parsed) == 4:
        return [(parsed[0], parsed[1]), (parsed[2], parsed[3])]
    elif parsed[0] == None:
        return [None, (parsed[1], parsed[2])]
    elif parsed[2] == None:
        return [(parsed[0], parsed[1]), None]

def get_image(scene):
    anno_path = '/home/jayyoung/code/ManipTransData/OakInk-v2/anno_preview'
    json_dir = '/home/jayyoung/code/ManipTransData/OakInk-v2/program/program_info'
    start, end = 0, 0
    scene_name, key, hand = scene
    with open(os.path.join(json_dir, scene_name)+'.json') as f:
        json_data = json.load(f)
        anno_data = np.load(os.path.join(anno_path, scene_name)+'.pkl', allow_pickle=True)
        k = list(json_data.keys())[key]
        left, right = group_into_tuples(parse_entry(k))
        if hand == 'left':
            left_start, left_end = left
            left_start = anno_data['frame_id_list'].index(left_start)
            left_end = anno_data['frame_id_list'].index(left_end)
            start = left_start
            end = left_end
        if hand == 'right':
            right_start, right_end = right
            right_start = anno_data['frame_id_list'].index(right_start)
            right_end = anno_data['frame_id_list'].index(right_end)
            start = right_start
            end = right_end
    
    img_path = '/home/jayyoung/code/ManipTransData/OakInk-v2/data/'
    images = sorted(glob.glob(os.path.join(img_path, scene_name, '104422070969', '*.png')))
    print(len(images), start, end)
    images = images[start:end]
    return images

if __name__ == '__main__':
    get_image(scene_list[0])