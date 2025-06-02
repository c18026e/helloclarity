import boto3
import json
import uuid
import sys
import os 
import boto3
from colorama import  Fore, Style


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utility import * 

# Constants
KB_ID = get_knowledge_base_id("vulnerability")   #"5UEQ3KKO6K"
MODEL_ARN_CLAUDE = get_model_arn_by_type("claude")  # "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
MODEL_ARN_META = get_model_arn_by_type("Llama_3_8B_Instruct")  # "arn:aws:bedrock:us-east-1::foundation-model/meta.llama-3.2-70b-instruct-v1:0"
MODEL_ARN_MISTRAL = get_model_arn_by_type("Mistral_7B_Instruct")  # "arn:aws:bedrock:us-east-1::foundation-model/mistral.mistral-7b-instruct-v0:0"

print("The knoweldge base IS is : ", KB_ID)

#MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
REGION = "us-east-1"


from colorama import Fore, Style

def print_colored(text, color):
    """
    Print text in the specified color using colorama.
    'grey' is simulated using dim white.
    """
    color = color.upper()
    if color == "GREY":
        print(Style.DIM + Fore.WHITE + text + Style.RESET_ALL)
    else:
        color_code = getattr(Fore, color, Fore.WHITE)
        print(Style.BRIGHT + color_code + text + Style.RESET_ALL)





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

    def __init__(self, client, agent_client, kb_id, model_arn):
        self.client = client
        self.agent_client = agent_client
        self.kb_id = kb_id
        self.model_arn = model_arn

    def retrieve_and_generate_llama3(self, user_query):
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

import streamlit as st

# Streamlit UI
st.title("Hello Clarity - AI Model Interaction")
st.write("Select a model and ask your question. Type 'exit' to quit.")  

model_choice = st.selectbox("Choose your model type:", ["Claude", "Llama", "Mistral"])
text_prompt = st.text_input("Enter your question (type 'exit' to quit):")

if model_choice == "Claude":
    MODEL_ARN = MODEL_ARN_CLAUDE
    color = "blue"
elif model_choice == "Llama":
    MODEL_ARN = MODEL_ARN_META
    color = "green"
elif model_choice == "Mistral":
    MODEL_ARN = MODEL_ARN_MISTRAL
    color = "red"

if text_prompt:
    if text_prompt.lower() == "exit":
        st.warning("Exiting... Refresh the page to restart.")
    else:
        st.info("Generating response...")
        bedrock_client = BedrockClient()

        if bedrock_client.client and bedrock_client.agent_client:
            model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN)

            if model_choice == "Claude":
                result = model_invoker.retrieve_and_generate_claude(text_prompt)
            elif model_choice == "Llama":
                result = model_invoker.retrieve_and_generate_llama3(text_prompt)
            elif model_choice == "Mistral":
                result = model_invoker.retrieve_and_generate_mistral(text_prompt)

            if result:
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>Generated Response:</span>", unsafe_allow_html=True)
                st.write(result)
            else:
                st.error("No response generated.")
        else:
            st.error("Failed to initialize Bedrock clients.")
