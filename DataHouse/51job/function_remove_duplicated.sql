CREATE FUNCTION preprocess(str VARCHAR(255))
RETURNS VARCHAR(10)
reads sql data
RETURN REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(str,'0',''),'1',''),'2',''),'3',''),'4',''),'5',''),'6',''),'7',''),'8',''),'9',''),'.',''),'-','')
