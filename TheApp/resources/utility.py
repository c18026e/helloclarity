import json 
import os 
from colorama import  Fore, Style
import boto3
from botocore.exceptions import ClientError
from colorama import Fore, Style
REGION = 'us-east-1'
EMAIL_TOPIC_ARN = "arn:aws:sns:us-east-1:266608018458:HelloClarity_Notifications"
import streamlit as st



def get_knowledge_base_id(kb_type):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'resources', 'models.json')

    
    with open(json_path, 'r') as file:
        data = json.load(file)

    for kb in data.get('knowledge_bases', []):
        if kb.get('type').lower() == kb_type.lower():
            entries = kb.get('entries', [])
            if entries:
                return entries[0].get('Knowledge_Base_ID')
    return None



def get_model_arn_by_type(model_type):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'resources', 'models.json')
    
    with open(json_path, 'r') as file:
        data = json.load(file)
        
    for model_group in data.get("foundation_models", []):
        if model_group.get("type").lower() == model_type.lower():
            entries = model_group.get("entries", [])
            if entries:
                return entries[0]["modelArn"]  # Return the first match as a plain string
    return None



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




def send_email_via_ses(sender, recipient, subject, body_text, region=REGION):
    ses_client = boto3.client('ses', region_name=region)

    try:
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body_text}}
            }
        )
        return response
    except ClientError as e:
        return f"Error: {e.response['Error']['Message']}"


def send_email_via_sns(message, email_topic_arn=EMAIL_TOPIC_ARN, region_name='us-east-1'):
    try:
        sns_client = boto3.client('sns', region_name=region_name)
        response = sns_client.publish(
            TopicArn=email_topic_arn,
            Message=message,
            Subject="Your Clarity AI Response"
        )
        return response
    except Exception as e:
        return str(e)



def handle_email_button(result,email_topic_arn=EMAIL_TOPIC_ARN):
    if st.button("Email Me"):

        if email_topic_arn:
            response = send_email_via_sns(result)
            if isinstance(response, dict):
                st.success("Email sent via SNS!")
            else:
                st.error(f"Error: {response}")
        else:
            st.warning("Please enter a valid SNS Topic ARN.")
