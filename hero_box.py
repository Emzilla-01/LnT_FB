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
    least_x = min([t[0] for t in list_of_4tupls])
    least_y = min([t[1] for t in list_of_4tupls])
    greatest_x = max([t[2] for t in list_of_4tupls])
    greatest_y = max([t[3] for t in list_of_4tupls])
    return( ((k),(least_x, least_y, greatest_x, greatest_y)))

def process_hero_box_annotations(post_to_boxes):
    data=filter_falsy_lists(post_to_boxes)
    data = list(data.items())
    print(f"type(data):{type(data)}")
    with Pool() as pool:
        result = pool.map(min_max_coords, data)
    return result

if __name__ == '__main__':
    with open(argv[1], "rt") as f_:
        data=json.loads(f_.read())
    main_result=process_hero_box_annotations(data)
    print(main_result)