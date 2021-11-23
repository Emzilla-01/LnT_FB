from random import randint
import re

from hero_box import filter_falsy_lists, min_max_coords, process_hero_box_annotations

################################################################################
class image_data_mock():
    def __init__(self, image_id, score, *args, **kwargs):
        self.image_id=image_id
        self.score=score
        self.n_boxes=randint(1,4)
        self.boxes=list()
        for n in range(self.n_boxes):
            x0=randint(0,1920)
            x1=randint(x0,1920)
            y0=randint(0,1920)
            y1=randint(y0,1920)        
            self.boxes.append((x0, x1, y0, y1))
    def to_dict(self):
        return({self.image_id:self.boxes})
        

################################################################################
def get_sql_data(connection="MOCK", static_path=r"fb_data_sql.sql"):
    if connection=="MOCK":
        with open(static_path, 'rt') as f_:
            data=f_.read()
        m = re.findall(r"INSERT INTO unlabeled_image_predictions [(]image_id, score[)] VALUES\n([\d', ().\n]+);", data)
        data_str = m[0]
        data_str = data_str.replace("\n", "").replace(" ", "")
        data_lst = list(eval(data_str.replace('"', '')))
        assert len(data_lst) == 50
    return(data_lst)

################################################################################
# quick validation on randint bounds
recs = [image_data_mock(i, i)  for i in range(100)]
recs[1].boxes

for r in recs:
    if r.boxes:
        for b in r.boxes:
            assert b[0] <= b[1], f"{r.image_id} failed x0<=x1"
            assert b[2] <= b[3], f"{r.image_id} failed y0<=y1"
del recs

################################################################################

if __name__ == '__main__':
    id_quality_data = get_sql_data()
    heroboxes_data = [image_data_mock(image_id, score) for image_id, score in id_quality_data]
    heroboxes_data = [hb.to_dict() for hb in heroboxes_data]
    main_result=[process_hero_box_annotations(hb) for hb in heroboxes_data]
    print(main_result)