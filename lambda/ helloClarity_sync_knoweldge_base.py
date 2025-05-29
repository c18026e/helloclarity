import boto3
import json
import urllib.parse
import os

bedrock_agent = boto3.client('bedrock-agent')
sns = boto3.client('sns')

KNOWLEDGE_BASE_ID = os.environ.get('KNOWLEDGE_BASE_ID')
DATA_SOURCE_ID = os.environ.get('DATA_SOURCE_ID')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')  # Add this env variable

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])
        s3_uri = f"s3://{bucket}/{key}"

        try:
            response = bedrock_agent.start_ingestion_job(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                dataSourceId=DATA_SOURCE_ID
            )

            # Send success email
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Knowledge Base Sync Successful",
                Message=f"The file {s3_uri} was successfully synced with knowledge base {KNOWLEDGE_BASE_ID}."
            )

            return {
                'statusCode': 200,
                'body': f"Successfully triggered sync for file: {s3_uri}"
            }

        except Exception as e:
            print("Error syncing knowledge base:", str(e))
            return {
                'statusCode': 500,
                'body': f"Failed to sync knowledge base: {str(e)}"
            }
