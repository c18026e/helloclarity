import boto3
import json
import uuid
import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utility import * 

# Constants
KB_ID = get_knowledge_base_id("vulnerability")   #"5UEQ3KKO6K"
MODEL_ARN = get_model_arn_by_type("claude")  # "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
print("The knoweldge base IS is : ", KB_ID)

#MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
REGION = "us-east-1"


class BedrockClient:
    def __init__(self, region_name=REGION):
        self.client = self.initialize_client(region_name)
        self.agent_client = self.initialize_agent_client(region_name)

    def initialize_client(self, region_name):
        try:
            return boto3.client('bedrock-runtime', region_name=region_name)
        except Exception as e:
            print(f"Error initializing bedrock-runtime client: {e}")
            return None

    def initialize_agent_client(self, region_name):
        try:
            return boto3.client('bedrock-agent-runtime', region_name=region_name)
        except Exception as e:
            print(f"Error initializing bedrock-agent-runtime client: {e}")
            return None


class ModelInvoker:

    def __init__(self, client, agent_client):
        self.client = client
        self.agent_client = agent_client

    def retrieve_and_generate_claude(self, user_query, kb_id=KB_ID, model_arn=MODEL_ARN):
        try:
            #session_id = str(uuid.uuid4())  # Optional: use a consistent session ID for multi-turn
            response = self.agent_client.retrieve_and_generate(
                input={"text": user_query},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": kb_id,
                        "modelArn": model_arn,
                        "generationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "You are a question answering agent. "
                                    "Answer the user's question using the information from the knowledge base. "
                                    "Here are the search results: $search_results$"
                                )
                            }
                        }
                    }
                },
                #sessionId=session_id
            )
            return response["output"]["text"]
        except Exception as e:
            print(f"Error during retrieval and generation: {e}")
            return None


def main():

    while(1):
        text_prompt = input("\nEnter your question ... or (type exit for EXIT)\n")
        if text_prompt == "exit":
            print("Exiting...")
            break
        elif text_prompt == "":
            print("Please enter a valid question.")
            continue
        print("Generating response...") 
        
        # Initialize Bedrock clients
        bedrock_client = BedrockClient()
        
        if bedrock_client.client and bedrock_client.agent_client:
            model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client)
            result = model_invoker.retrieve_and_generate_claude(text_prompt)
            if result:
                print("Generated Response:\n", result)
            else:
                print("No response generated.")
        else:
            print("Failed to initialize Bedrock clients.")


if __name__ == "__main__":
    main()
