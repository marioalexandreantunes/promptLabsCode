import os
import re

from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # Load environment variables from .env file

# Function to enhance prompts using Groq API
# The function name remains in Portuguese as per requirements
def re_prompt(pergunta : str) -> str:     
    # Initialize Groq client with API key from environment variables
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    # Create a chat completion request with system and user messages
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                    Promise:
                    "As a prompt expert, I will analyze the provided prompt and enhance it to maximize its effectiveness and clarity."
                    Goal:
                    "The goal is to refine the user's prompt so that the output from the language model is more accurate, clear, and actionable."
                    Output Format:
                    "Output should be a revised version of the original prompt, written clearly and concisely with actionable instructions for better model responses."
                    Warnings:
                    "Ensure that the revised prompt does not lose its original intent. Do not complicate the prompt unnecessarily. Keep the focus on improving clarity and specificity."
                    Context Dump:
                    "User will submit a prompt for you to refine. Your task is to improve this prompt so that the language model provides responses that are more aligned with user expectations."
                """
            },
            {
                "role": "user",
                "content": pergunta,
            }
        ],
        model="qwen-qwq-32b",
        temperature=0.3,
        top_p=0.75,     
    )
    
    # Clean the response by removing any <think> tags and return the enhanced prompt
    return re.sub(r"<think>.*?</think>", "", str(chat_completion.choices[0].message.content), flags=re.DOTALL).strip()
    #return chat_completion.choices[0].message.content