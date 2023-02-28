from multiprocessing import Pool
from sys import argv # passing data file input as argv[1]
import json # Using json as data staging for assessment, expecting that would be some db calls

def filter_falsy_lists(post_to_boxes):
    return({k:v for k,v in post_to_boxes.items() if v not in [[], None, "none", 0, [""]]})

def min_max_coords(items_list_of_4tupls):
    list_of_4tupls = items_list_of_4tupls[1]
    k=items_list_of_4tupls[0]
    if list_of_4tupls == []:
        return
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')
    for t in list_of_4tupls:
        if t[0]<min_x:
            min_x=t[0]

        if t[1]<min_y:
            min_y=t[1]

        if t[2]>max_x:
            max_x=t[2]

        if t[3]>max_y:
            max_y=t[3]

    return( ((k),(min_x, min_y, max_x, max_y)))

def process_hero_box_annotations(post_to_boxes):
    data=filter_falsy_lists(post_to_boxes)
    data = list(data.items())
    with Pool() as pool:
        result = pool.map(min_max_coords, data)
    return result

if __name__ == '__main__':
    with open(argv[1], "rt") as f_:
        data=json.loads(f_.read())
    main_result=process_hero_box_annotations(data)
    print(main_result)
