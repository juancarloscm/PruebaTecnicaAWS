SELECT 
    topic.name AS topic_name,
    CONCAT(fact_article.year, '-', fact_article.month) AS month,
    COUNT(*) AS total_articles
FROM spaceflight_catalog.fact_article fact_article
JOIN spaceflight_catalog.dim_topic topic 
  ON fact_article.topic_id = topic.topic_id
GROUP BY topic.name, fact_article.year, fact_article.month
ORDER BY month ASC, total_articles DESC;

