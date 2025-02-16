# PruebaTecnicaAWS

Arquitectura General del Pipeline 🔄

1️⃣ Ingesta de Datos
Componentes:
AWS Lambda Function (spaceflight_ingestion_to_s3)
Extrae datos desde la API de SpaceFlight News.
Almacena los datos en el bucket S3 (spaceflight-data-pipeline/raw/) en formato JSON.
Publica un evento en Amazon EventBridge cuando el proceso de ingesta finaliza con éxito.

2️⃣ Procesamiento de Datos
Componentes:
Amazon EventBridge
Regla configurada para escuchar eventos del tipo SUCCEEDED emitidos por Lambda.
Desencadena el Glue Job (news-data-processing-job).
AWS Glue Job (news-data-processing-job)
Lee datos desde el bucket S3 (spaceflight-data-pipeline/raw/).
Procesa la información con PySpark:
Limpia los datos.
Extrae palabras clave.
Realiza análisis de tendencias por fecha.
Guarda los resultados en S3 (spaceflight-data-pipeline/processed/) en formato Parquet, particionado por published_date.

3️⃣ Almacenamiento de Resultados
Componentes:
Amazon S3 (spaceflight-data-pipeline)
raw/: Almacena los datos crudos extraídos por Lambda.
processed/: Almacena los resultados procesados por el Glue Job en formato Parquet.
logs/: Guarda los logs del Spark UI del Glue Job (si está habilitado).
AWS Glue Catalog
Crea las tablas para consultar los datos procesados:
dim_news_source: Fuentes de las noticias.
dim_topic: Temas asociados a los artículos.
fact_article: Datos detallados de los artículos, particionado por published_date.
4️⃣ Consulta y Visualización
Componentes:
Amazon Athena
Consulta las tablas del Glue Catalog para realizar análisis SQL:
Tendencias por mes
Fuentes más influyentes
Google Looker Studio
Visualización interactiva conectada a las consultas de Athena.
Crea dashboards para mostrar análisis de tendencias y las fuentes más influyentes.
