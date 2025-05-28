## Authorization Error 
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

region = 'us-east-1'  # your region
service = 'aoss'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'si1q6q1aqm1e7k7nweub9.us-east-1.aoss.amazonaws.com'  # e.g., search-my-faiss-collection-xxxx.us-east-1.aoss.amazonaws.com


#sts = boto3.client('sts')
#print(sts.get_caller_identity())


client = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

index_name = 'vulnerability-faiss-index'

index_body = {
    "settings": {
        "index": {
            "knn": True
        }
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text"
            },
            "embedding": {
                "type": "knn_vector",
                "dimension": 1536,  # Titan embedding dimension
                "method": {
                    "name": "faiss",
                    "engine": "faiss",
                    "space_type": "l2",
                    "parameters": {
                        "ef_search": 512,
                        "ef_construction": 512,
                        "m": 16
                    }
                }
            }
        }
    }
}

try:
        response = client.indices.create(index=index_name, body=index_body)
        print("Index creation response:", response)
except Exception as e:
        print("Error creating index:", e)
        response = None

if response is None:
    print("Index creation failed!!  Please check the error message above.")
else:
    print("Index created successfully:", response)  


