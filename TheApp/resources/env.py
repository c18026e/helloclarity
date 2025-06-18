from .bedrock_utils import *
from .utility import get_knowledge_base_id, get_model_arn_by_type


KB_ID = get_knowledge_base_id("vulnerability")   #"5UEQ3KKO6K"
MODEL_ARN_CLAUDE = get_model_arn_by_type("claude")  # "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
MODEL_ARN_META = get_model_arn_by_type("Llama_3_8B_Instruct")  # "arn:aws:bedrock:us-east-1::foundation-model/meta.llama-3.2-70b-instruct-v1:0"
MODEL_ARN_MISTRAL = get_model_arn_by_type("Mistral_7B_Instruct")  # "arn:aws:bedrock:us-east-1::foundation-model/mistral.mistral-7b-instruct-v0:0"
EMAIL_TOPIC_ARN = "arn:aws:sns:us-east-1:266608018458:HelloClarity_Notifications"
