--------------------------------------------------------------------------------
-- Schema SQL
--------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS unlabeled_image_predictions (
image_id int,
score float
);
INSERT INTO unlabeled_image_predictions (image_id, score) VALUES
('828','0.3149'), ('705','0.9892'), ('46','0.5616'), ('594','0.7670'), ('232','0.1598'), ('524','0.9876'), ('306','0.6487'),
('132','0.8823'), ('906','0.8394'), ('272','0.9778'), ('616','0.1003'), ('161','0.7113'), ('715','0.8921'), ('109','0.1151'),
('424','0.7790'), ('609','0.5241'), ('63','0.2552'), ('276','0.2672'), ('701','0.0758'), ('554','0.4418'), ('998','0.0379'),
('809','0.1058'), ('219','0.7143'), ('402','0.7655'), ('363','0.2661'), ('624','0.8270'), ('640','0.8790'), ('913','0.2421'),
('439','0.3387'), ('464','0.3674'), ('405','0.6929'), ('986','0.8931'), ('344','0.3761'), ('847','0.4889'), ('482','0.5023'),
('823','0.3361'), ('617','0.0218'), ('47','0.0072'), ('867','0.4050'), ('96','0.4498'), ('126','0.3564'), ('943','0.0452'),
('115','0.5309'), ('417','0.7168'), ('706','0.9649'), ('166','0.2507'), ('991','0.4191'), ('465','0.0895'), ('53','0.8169'),
('971','0.9871');

alter table unlabeled_image_predictions add column weak_label int default null;
update unlabeled_image_predictions set weak_label = ROUND(CAST(score AS numeric), 0); 
-- Emy tried other assignments in the DDL dialogue at https://www.db-fiddle.com/f/4Fy9rAgzr3f6ex1n3W2WZ5/4 but only got those to work in DQL
alter table unlabeled_image_predictions add column row_number_asc int default null;
alter table unlabeled_image_predictions add column row_number_desc int default null;
alter table unlabeled_image_predictions add column subsample_desc int default null;
alter table unlabeled_image_predictions add column subsample_asc int default null;

--------------------------------------------------------------------------------
/*Our sampling strategy is to order the images in decreasing order of scores and sample every
3rd image starting with the first from the beginning until we get 10k positive samples. 
And we would like to do the same in the other direction, starting from the end to get 10k negative
samples.*/
--------------------------------------------------------------------------------
-- Query SQL
--------------------------------------------------------------------------------

-- assign row_number_desc
WITH view_sample AS
(SELECT ROW_NUMBER () OVER (order by score desc) as row_number, image_id
    FROM unlabeled_image_predictions order by score desc) 
UPDATE unlabeled_image_predictions set row_number_desc = view_sample.row_number
FROM view_sample
WHERE unlabeled_image_predictions.image_id = view_sample.image_id;

-- assign row_number_asc
WITH view_sample AS
(SELECT ROW_NUMBER () OVER (order by score asc) as row_number, image_id
    FROM unlabeled_image_predictions order by score asc) 
UPDATE unlabeled_image_predictions set row_number_asc = view_sample.row_number
FROM view_sample
WHERE unlabeled_image_predictions.image_id = view_sample.image_id;

--assign subsample_asc
WITH view_sample AS
(SELECT MOD(row_number_asc, 3)-1 as subsample_asc, image_id
    FROM unlabeled_image_predictions order by row_number_asc asc)    
UPDATE unlabeled_image_predictions set subsample_asc = view_sample.subsample_asc
FROM view_sample
WHERE unlabeled_image_predictions.image_id = view_sample.image_id;

--assign subsample_desc
WITH view_sample AS
(SELECT MOD(row_number_desc, 3)-1 as subsample_desc, image_id
    FROM unlabeled_image_predictions order by row_number_desc asc)    
UPDATE unlabeled_image_predictions set subsample_desc = view_sample.subsample_desc
FROM view_sample
WHERE unlabeled_image_predictions.image_id = view_sample.image_id;

create temp view vw_hi_5 as 
    select * from unlabeled_image_predictions 
    where (weak_label = 1 and subsample_desc = 0) order by score desc limit 5 ;
create temp view vw_lo_5 as 
    select * from unlabeled_image_predictions
    where (weak_label = 0 and subsample_asc = 0) order by score asc limit 5 ;


select image_id, weak_label from vw_hi_5 union
select image_id, weak_label from vw_lo_5 order by image_id asc;

--------------------------------------------------------------------------------