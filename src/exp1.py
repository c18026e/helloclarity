import boto3

client = boto3.client('opensearchserverless',region_name='us-east-1')

response = client.create_collection(
    name='vulnerabilitykb-collection',
    type='VECTORSEARCH',
    description='Collection for FAISS vector search'
)

print("Full response:", response)

#print("Collection created successfully:", response['collection']['name'])
