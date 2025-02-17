import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

@pytest.fixture(scope="session")
def spark():
    """Inicializa una sesión de Spark para pruebas"""
    return SparkSession.builder.master("local[*]").appName("TestNewsProcessing").getOrCreate()

@pytest.fixture
def sample_data(spark):
    """Crea un DataFrame de muestra similar a los datos JSON"""
    data = [
        (29287, "Firefly's Blue Ghost lands on the Moon", "Moon landing success", "2025-02-16T14:12:14Z", "Spaceflight Now", "https://example.com/article1"),
        (29288, "SpaceX Falcon 9 launch", "Successful launch of Falcon 9", "2025-02-14T10:30:00Z", "NASA", "https://example.com/article2"),
    ]
    schema = ["id", "title", "summary", "published_at", "news_site", "url"]
    return spark.createDataFrame(data, schema)

def test_data_loading(sample_data):
    """Verifica que los datos se cargan correctamente"""
    assert sample_data.count() == 2  # Se deben cargar 2 registros
    assert "title" in sample_data.columns  # La columna "title" debe existir

def test_cleaning_transformation(spark, sample_data):
    """Verifica la transformación de limpieza y normalización"""
    cleaned_df = sample_data.withColumn("published_date", col("published_at").substr(1, 10))
    assert "published_date" in cleaned_df.columns
    assert cleaned_df.select("published_date").distinct().count() > 0  # Debe haber fechas únicas

def test_fact_article_creation(spark, sample_data):
    """Verifica la generación de la tabla fact_article"""
    fact_article_df = sample_data.withColumn("article_id", col("id"))
    assert fact_article_df.count() == 2
    assert "article_id" in fact_article_df.columns

def test_dim_news_source(spark, sample_data):
    """Verifica la creación de la tabla dim_news_source"""
    dim_news_source_df = sample_data.select("news_site").distinct().withColumn("source_id", col("news_site"))
    assert dim_news_source_df.count() == 2  # 2 fuentes de noticias únicas
    assert "source_id" in dim_news_source_df.columns

