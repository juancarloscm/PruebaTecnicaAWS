# 🛰️ Proyecto de Pipeline de Datos - SpaceFlight News API

## **Descripción General**
Este proyecto implementa un **pipeline de datos en AWS** para extraer, procesar y analizar artículos de noticias sobre vuelos espaciales desde la **API de SpaceFlight News**. El objetivo es proporcionar información clave sobre tendencias, palabras clave populares y las fuentes de noticias más influyentes. La visualización se realiza mediante **Google Looker Studio**, conectado a Amazon Athena.

---

## **Arquitectura del Pipeline** 🔧
El pipeline está compuesto por los siguientes componentes:

![Arquitectura del Pipeline](A_detailed_architectural_diagram_illustrating_a_da.png)

1. **AWS Lambda (`spaceflight_ingestion_to_s3`)**
   - Extrae datos desde la API de SpaceFlight News.
   - Almacena los datos crudos en **Amazon S3 (`spaceflight-data-pipeline/raw/`)** en formato JSON.
   - Al finalizar la ingesta, publica un evento en **Amazon EventBridge**.

2. **Amazon EventBridge**
   - Monitorea los eventos de éxito (`SUCCEEDED`) de la función Lambda.
   - Activa el **Glue Job (`news-data-processing-job`)** para procesar los datos.

3. **AWS Glue Job (`news-data-processing-job`)**
   - Procesa los datos crudos en S3 (`raw`) utilizando **PySpark**:
     - Limpia y deduplica los datos.
     - Extrae palabras clave.
     - Realiza un análisis de tendencias por fecha.
   - Guarda los resultados procesados en **S3 (`spaceflight-data-pipeline/processed/`)**, en formato Parquet particionado por `published_date`.

4. **AWS Glue Catalog**
   - Registra metadatos sobre los datos procesados.
   - Define las siguientes tablas:
     - `dim_news_source`: Información sobre las fuentes de noticias.
     - `dim_topic`: Temas y categorías asociadas.
     - `fact_article`: Datos detallados de los artículos, particionados por `published_date`.

5. **Amazon Athena**
   - Ejecuta consultas SQL sobre las tablas del Glue Catalog para realizar análisis de tendencias y ranking de fuentes.

6. **Google Looker Studio**
   - Visualiza datos en dashboards interactivos, conectados directamente a **Athena**.
   - Muestra las tendencias más recientes y los artículos más relevantes.

---

## **Estructura del Proyecto** 📂
```
/spaceflight-data-pipeline
    ├── raw/            # Datos crudos (JSON) extraídos por Lambda
    ├── processed/      # Datos procesados (Parquet) generados por el Glue Job
    └── logs/           # Logs del Glue Job y Spark UI
```
---

## **Pasos para la Implementación** 🚀

### **1️⃣ Preparación del Entorno**
- Crear dos buckets S3:  
  - **`spaceflight-data-pipeline`** para datos crudos y procesados.  
  - **`spaceflight-data-results`** para almacenar resultados de consultas de Athena.

### **2️⃣ Configuración de la Función Lambda (`spaceflight_ingestion_to_s3`)**
- Despliega la función Lambda para extraer datos de la **API de SpaceFlight News** y almacenarlos en el bucket S3 (`raw/`).  
- Publica un evento en **EventBridge** cuando el proceso finaliza con éxito.

### **3️⃣ Configuración de Amazon EventBridge**
- Crear una regla en EventBridge para activar el **Glue Job (`news-data-processing-job`)** al recibir un evento `SUCCEEDED` de Lambda.

### **4️⃣ Ejecución del Glue Job (`news-data-processing-job`)**
- Procesa los datos crudos almacenados en S3 (`raw/`) y genera resultados en formato **Parquet**, guardándolos en S3 (`processed/`).

### **5️⃣ Actualización del Glue Catalog**
- Ejecutar el **Glue Crawler** para actualizar las particiones y tablas en el catálogo (`spaceflight_catalog`).

### **6️⃣ Consultas SQL en Amazon Athena**
- Verifica y analiza los datos procesados.  

Ejemplos de consultas SQL:  
- **Análisis de palabras clave más frecuentes:**  
  ```sql
  SELECT keywords, COUNT(*) AS count
  FROM keywords
  GROUP BY keywords
  ORDER BY count DESC
  LIMIT 10;
  ```

- **Análisis de tendencias por fecha:**  
  ```sql
  SELECT published_date, COUNT(*) AS article_count
  FROM fact_article
  GROUP BY published_date
  ORDER BY published_date DESC;
  ```

- **Ranking de fuentes de noticias:**  
  ```sql
  SELECT name, COUNT(*) AS total_articles
  FROM dim_news_source
  JOIN fact_article ON dim_news_source.source_id = fact_article.source_id
  GROUP BY name
  ORDER BY total_articles DESC;
  ```

---

## **Visualización en Looker Studio** 📊
1. Conecta Looker Studio a **Amazon Athena** como fuente de datos.  
2. Crea dashboards para mostrar las tendencias de artículos, palabras clave más comunes y las fuentes de noticias más influyentes.  
3. Personaliza los gráficos y filtros para mejorar la interacción.

---

## **Optimización y Escalabilidad** 🔍
1. **Particionamiento Temporal:** Mejora el rendimiento de las consultas en Athena.  
2. **Índices en Campos Clave:** Optimiza las consultas más frecuentes.  
3. **Alertas en CloudWatch:** Monitoriza el pipeline y recibe notificaciones ante fallos.  
4. **Automatización con Airflow (opcional):** Programa y monitorea todo el pipeline de forma centralizada.

---

## **Siguientes Pasos**
1. Generar un Airflow DAG para automatizar el pipeline completo.  
2. Mejorar la configuración del Glue Job para procesar datos históricos y agregar nuevas funcionalidades de análisis.  
3. Extender la visualización en Looker Studio para incluir gráficos adicionales y alertas de tendencias.

---

¡Gracias por leer! 😊

