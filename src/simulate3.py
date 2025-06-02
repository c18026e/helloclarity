import sys
import os
from colorama import Fore, Style

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.utility import print_colored
from utils.bedrock_utils import (
    BedrockClient,
    ModelInvoker,
    KB_ID,
    MODEL_ARN_CLAUDE,
    MODEL_ARN_META,
    MODEL_ARN_MISTRAL,
    MODEL_ARN_COMMANDR,
    MODEL_ARN_LLAMA3_70B,
    MODEL_ARN_MISTRAL_8X7B
)

# Model configuration
MODELS = {
    "1": ("Claude", MODEL_ARN_CLAUDE, "BLUE"),
    "2": ("Llama", MODEL_ARN_META, "GREEN"),
    "3": ("Mistral", MODEL_ARN_MISTRAL, "RED"),
    "4": ("Command_R", MODEL_ARN_COMMANDR, "YELLOW"),
    "5": ("Llama_3_70B_Instruct", MODEL_ARN_LLAMA3_70B, "CYAN"),
    #"6": ("Mixtral_8X7B", MODEL_ARN_MISTRAL_8X7B, "MAGENTA"),
    "7": ("Llama_3_70B_Instruct", MODEL_ARN_LLAMA3_70B, "MAGENTA"),
}


def select_model():
    print("Choose your model type:")
    for key, (name, _, _) in MODELS.items():
        print(f"{key}. {name}")
    choice = input("Enter your choice (1/2/3/4/5/6/7): ").strip()
    return MODELS.get(choice), choice


def get_user_input():
    print(Fore.GREEN + Style.BRIGHT + "\nEnter your question ... or (type exit for EXIT)" + Style.RESET_ALL)
    return input("> ").strip()


def invoke_model(model_invoker, model_name, prompt):
    method_name = f"retrieve_and_generate_{model_name.lower().replace('-', '_')}"
    print("should hit ", method_name)
    method = getattr(model_invoker, method_name, None)
    return method(prompt) if method else None


def run_all_models(prompt):
    combined_output = ""
    for key in ["1", "2", "3", "4", "5"]:
        name, arn, _ = MODELS[key]
        bedrock_client = BedrockClient()
        invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, arn)
        response = invoke_model(invoker, name, prompt)
        print(response)
        combined_output += f"\nClient: {arn}\n{response}\n"
        print_colored(combined_output, "MAGENTA")
    print("All models have been invoked. Combined output:")
    return combined_output


def summarize_combined_output(prompt, combined_output):
    summary_prompt = (
        f"Question: {prompt}\n\n"
        f"There are multiple answers fetched from various models:\n{combined_output}\n\n"
        "Please provide a concise answer to the question based on the information provided."
    )
    name = "Command_R"

    print("Summarizing with Command_R model...")
    print(f"Summary Prompt: {summary_prompt}")
    print(f"Knowledge Base ID: {KB_ID}")    

    bedrock_client = BedrockClient()
    invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, MODEL_ARN_COMMANDR)
    
    response =  invoke_model(invoker, name, summary_prompt)
    return response if response else "No summary generated."


def main():
    print(f"{os.getcwd()}\nThe knoweldge base selected is :  {KB_ID}")
    while True:
        model_info, model_choice = select_model()
        if not model_info:
            print("Invalid choice. Exiting...")
            break

        model_name, model_arn, color = model_info
        print(f"You selected model: {model_name} with ARN: {model_arn}")

        user_input = get_user_input()
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        if not user_input:
            print("Please enter a valid question.")
            continue

        print("Generating response...")

        bedrock_client = BedrockClient()
        if not bedrock_client.client or not bedrock_client.agent_client:
            print_colored("Failed to initialize Bedrock clients.", "RED")
            continue

        model_invoker = ModelInvoker(bedrock_client.client, bedrock_client.agent_client, KB_ID, model_arn)

        if model_choice == "7":
    
            print_colored("Running all models and summarizing...", "MAGENTA")       
            combined_output = run_all_models(user_input)
            print_colored("Combining outputs from all models...", "MAGENTA")
            print("Combined Output:\n", combined_output)    
            result = invoke_model(model_invoker, model_name, combined_output)
            #result = summarize_combined_output(user_input, combined_output)
        else:
            print("NOTE THIS: ", model_invoker,model_name,user_input)

            result = invoke_model(model_invoker, model_name, user_input)

        if result:
            print("Generated Response:\n")
            print_colored(result, color)
        else:
            print_colored("No response generated.", "RED")


if __name__ == "__main__":
    main()
