import boto3
import json

client = boto3.client('opensearchserverless', region_name='us-east-1')

response = client.create_security_policy(
    name='vulnerabilitykb-security-policy',
    type='encryption',
    policy=json.dumps({
        "Rules": [
            {
                "ResourceType": "collection",
                "Resource": ["collection/vulnerabilitykb-collection"],
            }
        ],
        "AWSOwnedKey": True
    })
)

print("Security policy created:", response)



# Example output:
#(venv) [ec2-user@ip-10-91-176-75 hello_clarity]$ python3 src/securitypolicy.py
#Security policy created: {'securityPolicyDetail': {'type': 'encryption', 'name': 'vulnerabilitykb-security-policy', 'policyVersion': 'MTc0ODM0MDQ0NDk1MF8x', 'policy': {'Rules': [{'Resource': ['collection/vulnerabilitykb-collection'], 'ResourceType': 'collection'}], 'AWSOwnedKey': True}, 'createdDate': 1748340444950, 'lastModifiedDate': 1748340444950}, 'ResponseMetadata': {'RequestId': '5b5d3b02-f17b-4d3f-972b-8de6cf3d7954', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '5b5d3b02-f17b-4d3f-972b-8de6cf3d7954', 'date': 'Tue, 27 May 2025 10:07:24 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '310', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
#(venv) [ec2-user@ip-10-91-176-75 hello_clarity]$ 

# The above code creates a security policy for an OpenSearch Serverless collection named 'vulnerabilitykb-collection'.  