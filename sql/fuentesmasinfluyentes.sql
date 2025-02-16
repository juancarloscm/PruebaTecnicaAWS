SELECT 
    source.name AS source_name,
    COUNT(*) AS total_articles,
    AVG(source.reliability_score) AS avg_reliability_score
FROM spaceflight_catalog.fact_article fact_article
JOIN spaceflight_catalog.dim_news_source source 
  ON fact_article.source_id = source.source_id
GROUP BY source.name
ORDER BY total_articles DESC
LIMIT 10;

