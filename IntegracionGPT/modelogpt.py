import boto3
import openai
import json

# Configurar clientes de AWS
sagemaker_runtime = boto3.client('sagemaker-runtime')
openai.api_key = "API-OPENAI"

def lambda_handler(event, context):
    # Recibir pregunta del usuario
    user_question = event['queryStringParameters']['question']

    # Obtener predicción de AutoML (SageMaker)
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName="nombre-del-endpoint",
        ContentType="application/json",
        Body=json.dumps({"input": user_question})
    )
    prediction = json.loads(response['Body'].read().decode())

    # Pasar predicción a GPT
    prompt = f"Basado en este análisis: {prediction}, ¿qué recomendarías?"
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"respuesta": gpt_response['choices'][0]['message']['content']})
    }

