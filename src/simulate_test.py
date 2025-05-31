import boto3
import json
import uuid
import sys
import os 
import boto3
from colorama import  Fore, Style
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.utility import * 
from utils.bedrock_utils import * 


def main():

    while(1):
        
        color = 'WHITE'
        models = {
                    "1": ("Claude", MODEL_ARN_CLAUDE, "BLUE"),
                    "2": ("Llama", MODEL_ARN_META, "GREEN"),
                    "3": ("Mistral", MODEL_ARN_MISTRAL, "RED"),
                    "4": ("Command_R", MODEL_ARN_COMMANDR, "YELLOW"),
                    "5": ("Llama_3_70B_Instruct", MODEL_ARN_LLAMA3_70B, "CYAN"),
                    "6": ("Mixtral_8X7B", MODEL_ARN_MISTRAL_8X7B, "MAGENTA"),
                }

        print("Choose your model type:")
        for key, (name, _, _) in models.items():
            print(f"{key}. {name}")

        model_choice = input("Enter your choice (1/2/3/4/5/6): ")

        if model_choice in models:
            model_name, MODEL_ARN, color = models[model_choice]
            print(f"You selected model: {model_name} with ARN: {MODEL_ARN}")
        else:
            print("Invalid choice. Exiting...")
            sys.exit(1)

        print(f"You selected model: {model_choice} with ARN: {MODEL_ARN}")
        # Exit condition

        print(Fore.GREEN + Style.BRIGHT + "\nEnter your question ... or (type exit for EXIT)" + Style.RESET_ALL)
        text_prompt = input("> ")

        #text_prompt = input("\nEnter your question ... or (type exit for EXIT)\n")
        if text_prompt.lower() == "exit":
            print("Exiting...")
            break
        # Check for empty input         
        if text_prompt == "exit":   
            print("Exiting...")
            break
        elif text_prompt == "":
            print("Please enter a valid question.")
            continue
        print("Generating response...") 
        
        # Initialize Bedrock clients
        
        # Main Logic here , calling Bedrock clients and invoking the model

        bedrock_client = BedrockClient() 
        
        if bedrock_client.client and bedrock_client.agent_client:
            model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN)
            # Call the appropriate method based on the model choice
            if model_choice == "1":
                result = model_invoker.retrieve_and_generate_claude(text_prompt)
            elif model_choice == "2":
                result = model_invoker.retrieve_and_generate_llama3(text_prompt)
            elif model_choice == "3":
                result = model_invoker.retrieve_and_generate_mistral(text_prompt)
            elif model_choice == "4":
                result = model_invoker.retrieve_and_generate_cohere(text_prompt)
            elif model_choice == "5":
                result = model_invoker.retrieve_and_generate_Llama_3_70B_Instruct(text_prompt)

            elif model_choice == "6":
                together = ""
                print("Executing all Models and capturing the output in a single note  ")
                bedrock_client = BedrockClient() 
                model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_CLAUDE)
                together +=  f"Client : {MODEL_ARN_CLAUDE}\n" 
                together +=  model_invoker.retrieve_and_generate_claude(text_prompt)
               
                bedrock_client = BedrockClient()
                model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_META) 
                together +=  f"Client : {MODEL_ARN_META}\n" 
                together += "\n\n" + model_invoker.retrieve_and_generate_llama3(text_prompt)
               
                bedrock_client = BedrockClient() 
                model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_MISTRAL)
                together +=  f"Client : {MODEL_ARN_MISTRAL}\n" 
                together += "\n\n" + model_invoker.retrieve_and_generate_mistral(text_prompt)
               
                bedrock_client = BedrockClient() 
                model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_COMMANDR)
                together +=  f"Client : {MODEL_ARN_COMMANDR}\n" 
                together += "\n\n" + model_invoker.retrieve_and_generate_cohere(text_prompt)
               
                bedrock_client = BedrockClient() 
                model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_LLAMA3_70B)
                together +=  f"Client : {MODEL_ARN_LLAMA3_70B}\n" 
                together += "\n\n" + model_invoker.retrieve_and_generate_Llama_3_70B_Instruct(text_prompt)
                
                #print(together)

            # Uncomment the following lines if you want to add more models in the future
            #elif model_choice == "6":
             #   result = model_invoker.retrieve_and_generate_Mixtral_8x7B_Instruct(text_prompt)    
            else:
                print("Invalid choice. Defaulting to Claude.")          
            #result = model_invoker.retrieve_and_generate_claude(text_prompt)
            
            prompt = f"Question: {text_prompt}\n . There are multiple answers fetched from various models as {together} . Please provide a concise answer to the question based on the information provided."
            
            bedrock_client = BedrockClient()
            model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_CLAUDE)
            result = model_invoker.retrieve_and_generate_claude(prompt)

            if result:
                print("Generated Response:\n")
                print_colored(result, color)
            else:
                print_colored("No response generated.",'RED')
        else:
            print_colored("Failed to initialize Bedrock clients.","RED")


if __name__ == "__main__":
    main()
