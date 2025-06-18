import boto3
import json
import uuid
import sys
import os 
import boto3
from .utility import * 

# -------------------------------------------------------------------------------------- #
# Add the parent directory to the system path to import utility functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# -------------------------------------------------------------------------------------- #

# RETRIVE KNOWELDGE BASE ID   ------------------------------------- #

KB_ID = get_knowledge_base_id("vulnerability") 

# RETRIVE MODEL ARN BY TYPE ------------------------------------- #

MODEL_ARN_CLAUDE = get_model_arn_by_type("claude") 
MODEL_ARN_META = get_model_arn_by_type("Llama_3_8B_Instruct") 
MODEL_ARN_MISTRAL = get_model_arn_by_type("Mistral_7B_Instruct")

MODEL_ARN_COMMANDR = get_model_arn_by_type("cohere")  
MODEL_ARN_LLAMA3_70B = get_model_arn_by_type("Llama_3_70B_Instruct") 
MODEL_ARN_MISTRAL_8X7B = get_model_arn_by_type("Mixtral_8x7B_Instruct") 


REGION = "us-east-1"
print("The knoweldge base selected is : ", KB_ID)

# -------------------------------------------------------------------------------------- #

# Initialize the Bedrock client and agent client
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

# Invoker class to handle model interactions 
class ModelInvoker:

    def __init__(self, client, agent_client, kb_id, model_arn):
        self.client = client
        self.agent_client = agent_client
        self.kb_id = kb_id
        self.model_arn = model_arn

    def retrieve_and_generate_llama(self, user_query):
        kb_id = self.kb_id 
        model_arn = self.model_arn  # Should point to Llama 3 8B Instruct model
        if not self.client or not self.agent_client:
            print("Bedrock clients are not initialized.")
            return None
        if not user_query:  
            print("User query is empty.")
            return None
        if not kb_id or not model_arn:  
            print("Knowledge Base ID or Model ARN is not set.")
            return None
        #print(Fore.GREEN + f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}")   
        print_colored(f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}", 'GREY')

        try:
            response = self.agent_client.retrieve_and_generate(
                input={"text": user_query},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": kb_id,
                        "modelArn": model_arn,
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {
                                "numberOfResults": 5
                            }
                        },
                        "orchestrationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "Conversation history:\n$conversation_history$\n\n"
                                    "User query:\n$query$\n\n"
                                    "$output_format_instructions$"
                                )
                            }
                        },
                        "generationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "You are a helpful assistant. Use the following search results to answer the user's question.\n\n"
                                    "Search Results:\n$search_results$\n\n"
                                    "User Question:\n$query$\n\n"
                                    "Answer:"
                                )
                            }
                        }
                    }
                }
            )
            return response["output"]["text"]
        except Exception as e:
            print(f"Error during retrieval and generation: {e}")
            return None

    def retrieve_and_generate_mistral(self, user_query):
        kb_id = self.kb_id 
        model_arn = self.model_arn
        if not self.client or not self.agent_client:
            print("Bedrock clients are not initialized.")
            return None
        if not user_query:  
            print("User query is empty.")
            return None
        if not kb_id or not model_arn:  
            print("Knowledge Base ID or Model ARN is not set.")
            return None
        print_colored(f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}", 'GREY')

        try:
            response = self.agent_client.retrieve_and_generate(
                input={"text": user_query},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": kb_id,
                        "modelArn": model_arn,
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {
                                "numberOfResults": 5
                            }
                        },
                        "orchestrationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "Conversation history:\n$conversation_history$\n\n"
                                    "User query:\n$query$\n\n"
                                    "$output_format_instructions$"
                                )
                            }
                        },
                        "generationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "You are a helpful assistant. Use the following search results to answer the user's question.\n\n"
                                    "Search Results:\n$search_results$\n\n"
                                    "User Question:\n$query$\n\n"
                                    "Answer:"
                                )
                            }
                        }
                    }
                }
            )
            return response["output"]["text"]
        except Exception as e:
            print(f"Error during retrieval and generation: {e}")
            return None

    def retrieve_and_generate_claude(self, user_query):
        kb_id = self.kb_id 
        model_arn = self.model_arn
        if not self.client or not self.agent_client:
            print("Bedrock clients are not initialized.")
            return None
        if not user_query:  
            print("User query is empty.")
            return None
        if not kb_id or not model_arn:  
            print("Knowledge Base ID or Model ARN is not set.")
            return None
        print_colored(f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}", 'GREY')
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

    def retrieve_and_generate_command_r(self, user_query):
        kb_id = self.kb_id
        model_arn = self.model_arn  # Should be the ARN for Cohere Command R+
        
        print("kb_id", kb_id)
        print("model_arn", model_arn)

        if not self.client or not self.agent_client:
            print("Bedrock clients are not initialized.")
            return None
        if not user_query:
            print("User query is empty.")
            return None
        if not kb_id or not model_arn:
            print("Knowledge Base ID or Model ARN is not set.")
            return None

        print_colored(f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}", 'GREY')

        try:
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
                                    "You are a helpful assistant. "
                                    "Use the following knowledge base search results to answer the user's question. "
                                    "Search Results: $search_results$"
                                )
                            }
                        }
                    }
                }
            )
            return response["output"]["text"]
        except Exception as e:
            print(f"Error during retrieval and generation: {e}")
            return None

    def retrieve_and_generate_llama_3_70b_instruct(self, user_query):
        kb_id = self.kb_id
        model_arn = self.model_arn  # Should be the ARN for LLaMA 3 7B Instruct

        if not self.client or not self.agent_client:
            print("Bedrock clients are not initialized.")
            return None
        if not user_query:
            print("User query is empty.")
            return None
        if not kb_id or not model_arn:
            print("Knowledge Base ID or Model ARN is not set.")
            return None

        print_colored(f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}", 'GREY')

        try:
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
                                    "You are a helpful assistant. "
                                    "Use the following knowledge base search results to answer the user's question clearly and concisely. "
                                    "Search Results: $search_results$"
                                )
                            }
                        }
                    }
                }
            )
            return response["output"]["text"]
        except Exception as e:
            print(f"Error during retrieval and generation: {e}")
            return None
        
    def retrieve_and_generate_mixtral_8x7b(self, user_query):
        
        # Not working 
        kb_id = self.kb_id
        model_arn = "arn:aws:bedrock:us-east-1::foundation-model/mistral.mixtral-8x7b-instruct-v0:1"

        if not self.client or not self.agent_client:
            print("Bedrock clients are not initialized.")
            return None
        if not user_query:
            print("User query is empty.")
            return None
        if not kb_id or not model_arn:
            print("Knowledge Base ID or Model ARN is not set.")
            return None

        print_colored(f"Using Knowledge Base ID: {kb_id} and Model ARN: {model_arn}", 'GREY')

        try:
            response = self.agent_client.retrieve_and_generate(
                input={"text": user_query},
                retrieveAndGenerateConfiguration={
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "knowledgeBaseId": kb_id,
                        "modelArn": model_arn,
                        "orchestrationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "<s>[INST] $conversation_history$\n\n"
                                    "Please retrieve relevant documents from the knowledge base to help answer the user's question below.\n\n"
                                    "User Query:\n$user_input$\n\n"
                                    "$output_format_instructions$ [/INST]"
                                )
                            }
                        },
                        "generationConfiguration": {
                            "promptTemplate": {
                                "textPromptTemplate": (
                                    "<s>[INST] $conversation_history$\n\n"
                                    "Use the following search results to answer the user's question.\n\n"
                                    "Search Results:\n$search_results$\n\n"
                                    "User Question:\n$user_input$\n\n"
                                    "$output_format_instructions$ [/INST]"
                                )
                            }
                        }
                    }
                }
            )
            return response["output"]["text"]
        except Exception as e:
            print(f"Error during retrieval and generation: {e}")
            return None
