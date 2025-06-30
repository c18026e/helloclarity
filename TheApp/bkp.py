import boto3
import json
import uuid
import sys
import os 
from botocore.exceptions import ClientError
from colorama import Fore, Style
import streamlit as st

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from resources.env import *

# System prompt
system_prompt = ( 
    "You are a helpful assistant that can answer questions based on the provided knowledge base. "
    "Use the search results to generate accurate and relevant responses to user queries. "
    "If possible provide bullet points as well as a summary of the answer and use some bold fonts for highlighting important points. "
    "Please start your answer as 'Dear Clarity User ,' and end with 'Thank you for using Clarity.'"
)   

# Streamlit UI
st.title("Hello Clarity - AI Model Interaction")
st.write("Select a model and ask your question. Type 'exit' to quit.")  

model_choice = st.selectbox("Choose your model type:", ["Claude", "Llama", "Mistral"])
prompt = st.text_area("Enter your question (type 'exit' to quit):", height=150)
submit = st.button("ENTER", use_container_width=True)

if submit:
    if prompt.lower() == "exit":
        st.warning("Exiting... Refresh the page to restart.")
    else:
        st.info("Generating response...")
        text_prompt = system_prompt + "\n\n" + prompt
        # Set model ARN and color
        if model_choice == "Claude":
            MODEL_ARN = MODEL_ARN_CLAUDE
            color = "blue"
        elif model_choice == "Llama":
            MODEL_ARN = MODEL_ARN_META
            color = "green"
        elif model_choice == "Mistral":
            MODEL_ARN = MODEL_ARN_MISTRAL
            color = "red"

        # Initialize Bedrock client
        bedrock_client = BedrockClient()

        if bedrock_client.client and bedrock_client.agent_client:
            model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN)

            if model_choice == "Claude":
                result = model_invoker.retrieve_and_generate_claude(text_prompt)
            elif model_choice == "Llama":
                result = model_invoker.retrieve_and_generate_llama_3_70b_instruct(text_prompt)
            elif model_choice == "Mistral":
                result = model_invoker.retrieve_and_generate_mistral(text_prompt)

            if result:
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>Generated Response:</span>", unsafe_allow_html=True)
                st.write(result)

                formatted_prompt = f"<b><span style='color:green'>{prompt}</span></b>"
                combined_message = f"{formatted_prompt}<br><br>{result}"

                result = prompt.upper() + "\n\n" + result
                handle_email_button(result)
            else:
                st.error("No response generated.")
        else:
            st.error("Failed to initialize Bedrock clients.")
