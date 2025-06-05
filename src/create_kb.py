import boto3
import json

# Set your AWS region
region = 'us-east-1'  # Change this to your preferred region

# Initialize boto3 clients
opensearch_client = boto3.client('opensearchserverless', region_name=region)
bedrock_client = boto3.client('bedrock-agent', region_name=region)

# Parameters
collection_name = 'helloclarity'
knowledge_base_name = 'vulnerabilitykb'
s3_bucket = 'hello-clarity-us-east-1'  # Replace with your actual bucket
s3_prefix = 'vulnerabilities'       # Replace with your actual prefix

role_arn = "arn:aws:iam::266608018458:role/helloClarityRole"
embedding_model_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
vector_index_name = "vulnerability-index"
collection_arn = "arn:aws:aoss:us-east-1:266608018458:collection/20raeih7go86q70enyge"


# Step 1: Create Encryption Policy
def create_encryption_policy(collection_name):
    policy = json.dumps({
        "Rules": [
            {
                "ResourceType": "collection",
                "Resource": [f"collection/{collection_name}"]
            }
        ],
        "AWSOwnedKey": True
    })
    try:
        response = opensearch_client.create_security_policy(
            name=f"{collection_name}-encryption-policy",
            type="encryption",
            policy=policy
        )
        print("Encryption policy created.")
        return response
    except opensearch_client.exceptions.ConflictException:
        print("Encryption policy already exists. Skipping.")
        return None

# Step 2: Create Network Policy
def create_network_policy(collection_name):
    vpce_id = 'vpce-xxxxxxxxxxxxxxxxx'  # Replace with your actual VPC endpoint ID

    policy = json.dumps([
        {
            "Rules": [
                {
                    "ResourceType": "collection",
                    "Resource": [f"collection/{collection_name}"]
                }
            ],
            "AllowFromPublic": False,
            "SourceVPCEs": [vpce_id],
            "SourceServices": ["aoss.amazonaws.com"]
        }
    ])
    try:
        response = opensearch_client.create_security_policy(
            name=f"{collection_name}-network-policy",
            type="network",
            policy=policy
        )
        print("Network policy created.")
        return response
    except opensearch_client.exceptions.ConflictException:
        print("Network policy already exists. Skipping.")
        return None

# Step 3: Create OpenSearch Serverless Collection
def create_opensearch_collection(name):
    try:
        response = opensearch_client.create_collection(
            name=name,
            type='SEARCH',
            description='Collection for vulnerability knowledge base'
        )
        print("Collection created.")
        return response
    except opensearch_client.exceptions.ConflictException:
        print("Collection already exists. Skipping.")
        # Corrected: name should be a string, not a list
        existing = opensearch_client.list_collections(
            collectionFilters={"name": name}
        )
        return existing['collectionSummaries'][0] if existing['collectionSummaries'] else None



# Step 4: Create Bedrock Knowledge Base


def create_knowledge_base(name, bucket, prefix, role_arn, collection_arn, embedding_model_arn, vector_index_name):
    # Step 1: Create the knowledge base
    kb_response = bedrock_client.create_knowledge_base(
        name=name,
        roleArn=role_arn,
        knowledgeBaseConfiguration={
            "type": "VECTOR",
            "vectorKnowledgeBaseConfiguration": {
                "embeddingModelArn": embedding_model_arn
            }
        },
        storageConfiguration={
            "type": "OPENSEARCH_SERVERLESS",
            "opensearchServerlessConfiguration": {
                "collectionArn": collection_arn,
                "vectorIndexName": vector_index_name,
                "fieldMapping": {
                    "vectorField": "embedding",
                    "textField": "text",
                    "metadataField": "metadata"
                }
            }
        }
    )

    knowledge_base_id = kb_response['knowledgeBase']['knowledgeBaseId']
    print(f"Knowledge base created with ID: {knowledge_base_id}")

    # Step 2: Create the data source
    data_source_response = bedrock_client.create_data_source(
        knowledgeBaseId=knowledge_base_id,
        name=f"{name}-data-source",
        dataSourceConfiguration={
            "s3": {
                "bucketArn": f"arn:aws:s3:::{bucket}",
                "inferenceConfig": {
                    "document": {
                        "s3Prefix": prefix
                    }
                }
            }
        }
    )

    print(f"Data source created: {data_source_response['dataSource']['dataSourceId']}")
    return kb_response, data_source_response


# Main execution
if __name__ == "__main__":
    print("Creating encryption policy...")
    encryption_policy_response = create_encryption_policy(collection_name)
    print("Encryption policy created:", encryption_policy_response)

    print("Creating network policy...")
    network_policy_response = create_network_policy(collection_name)
    print("Network policy created:", network_policy_response)

    print("Creating OpenSearch Serverless collection...")
    collection_response = create_opensearch_collection(collection_name)
    print("Collection created:", collection_response)

    print("Creating Bedrock Knowledge Base...")
    kb_response, ds_response = create_knowledge_base(
        name="my-kb",
        bucket="my-s3-bucket",
        prefix="documents/",
        role_arn="arn:aws:iam::123456789012:role/BedrockKnowledgeBaseRole",
        collection_arn="arn:aws:aoss:us-west-2:123456789012:collection/my-collection",
        embedding_model_arn="arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v1",
        vector_index_name="my-vector-index"
    )


    print("Knowledge Base created:", kb_response)
