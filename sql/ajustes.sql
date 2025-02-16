-- ok
SELECT * FROM dim_news_source LIMIT 10;
-- ok
SELECT * FROM dim_topic LIMIT 10;
-- no hay datos
SELECT * FROM fact_article LIMIT 10;

MSCK REPAIR TABLE fact_article;

DROP TABLE fact_article;

CREATE EXTERNAL TABLE IF NOT EXISTS fact_article (
  article_id INT,
  source_id INT,
  topic_id INT,
  published_at TIMESTAMP
)
PARTITIONED BY (published_date STRING)
STORED AS PARQUET
LOCATION 's3://spaceflight-data-pipeline/processed/fact_article/';

MSCK REPAIR TABLE fact_article;

fact_article fact_article 

CREATE EXTERNAL TABLE IF NOT EXISTS spaceflight_catalog.fact_article (
  article_id BIGINT,
  source_id BIGINT,
  topic_id BIGINT,
  published_at TIMESTAMP
)
PARTITIONED BY (published_date STRING)
STORED AS PARQUET
LOCATION 's3://spaceflight-data-pipeline/processed/fact_article/';

MSCK REPAIR TABLE fact_article;


MSCK REPAIR TABLE fact_article;

SELECT * 
FROM fact_article 
LIMIT 10

CREATE TABLE temp_fact_article AS 
SELECT * 
FROM "s3://spaceflight-data-pipeline/processed/fact_article/"
LIMIT 10;

ALTER TABLE fact_article ADD PARTITION (published_date='2025-02-15') 
LOCATION 's3://spaceflight-data-pipeline/processed/fact_article/published_date=2025-02-15/';


SELECT * FROM "s3://spaceflight-data-pipeline/processed/fact_article/published_date=2025-02-15/part-00001-3f4bfbef-b0d8-4324-ba9e-e9e7145bd0ef.c000.snappy.parquet" LIMIT 10;


SHOW PARTITIONS fact_article;

SELECT * FROM fact_article WHERE published_date = '2025-02-15' LIMIT 10;

