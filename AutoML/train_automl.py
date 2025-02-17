import boto3

sagemaker = boto3.client("sagemaker")

# Configuración del AutoML Job
automl_job_name = "spaceflight-news-trends"
input_data = "s3://spaceflight-data-pipeline/training-data/"
output_data = "s3://spaceflight-data-pipeline/models/"

response = sagemaker.create_auto_ml_job(
    AutoMLJobName=automl_job_name,
    InputDataConfig=[{
        "DataSource": {
            "S3DataSource": {"S3Uri": input_data, "S3DataType": "S3Prefix"}
        },
        "TargetAttributeName": "popularity_score"
    }],
    OutputDataConfig={"S3OutputPath": output_data},
    ProblemType="Regression",
    AutoMLJobObjective={"MetricName": "MSE"}
)

print("AutoML Job Iniciado:", response["AutoMLJobArn"])

