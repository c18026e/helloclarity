import json 
import os 
from colorama import  Fore, Style


def get_knowledge_base_id(kb_type):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(base_dir, 'resources', 'models.json')

    
    with open(json_path, 'r') as file:
        data = json.load(file)

    for kb in data.get('knowledge_bases', []):
        if kb.get('type') == kb_type:
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

## Test the functions ## 

# Example usage

#kb_id = get_knowledge_base_id("jira")
#print("Knowledge Base ID:", kb_id)

#fm = get_model_arn_by_type("claude")
#print("fm:", fm)
