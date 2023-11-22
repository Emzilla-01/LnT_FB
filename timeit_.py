import timeit
from mock_sql_conn import *    

id_quality_data = get_sql_data()
heroboxes_data = [image_data_mock(image_id, score) for image_id, score in id_quality_data]
heroboxes_data = [hb.to_dict() for hb in heroboxes_data]

def t():
    return([process_hero_box_annotations(hb) for hb in heroboxes_data])

x=timeit.timeit(t, number=10_000)  
print(x)

