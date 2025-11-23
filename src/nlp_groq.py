import os
import requests
import json
from dotenv import load_dotenv
from .logger import logger
from .config import GROQ_API_KEY, SYSTEM_PROMPT
from .tools import TOOLS_SCHEMA, AVAILABLE_TOOLS

load_dotenv()


def chat_reply(user_text: str) -> str:
    """
    Sends user text to Groq (Llama 3) and returns the response.
    Handles function calling if the model requests it.
    """
    if not user_text:
        return ""

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text}
    ]

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "tools": TOOLS_SCHEMA,
        "tool_choice": "auto",
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        # 1. First API Call
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            logger.error(f"[NLP] Groq API Error: {response.status_code} - {response.text}")
            return f"Sorry, I encountered an error: {response.text}"

        data = response.json()
        
        message = data['choices'][0]['message']
        
        # 2. Check for tool calls
        if message.get('tool_calls'):
            tool_calls = message['tool_calls']
            logger.info(f"[NLP] Tool calls detected: {len(tool_calls)}")
            
            # Append assistant's tool request to history
            messages.append(message)

            for tool_call in tool_calls:
                function_name = tool_call['function']['name']
                function_args = json.loads(tool_call['function']['arguments'])
                
                logger.info(f"[NLP] Executing tool: {function_name} with {function_args}")
                
                function_to_call = AVAILABLE_TOOLS.get(function_name)
                if function_to_call:
                    try:
                        function_response = function_to_call(**function_args)
                    except Exception as e:
                        function_response = f"Error executing {function_name}: {e}"
                else:
                    function_response = f"Error: Tool {function_name} not found."
                
                # Append tool result to history
                messages.append({
                    "tool_call_id": tool_call['id'],
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                })

            # 3. Second API Call (Get final answer)
            payload['messages'] = messages
            # Remove tools from second call to force a text response (optional, but cleaner)
            del payload['tools']
            del payload['tool_choice']
            
            second_response = requests.post(url, headers=headers, json=payload)
            if second_response.status_code != 200:
                 logger.error(f"[NLP] Groq API Error (2nd call): {second_response.status_code} - {second_response.text}")
                 return "Sorry, I encountered an error processing the tool result."
            
            second_data = second_response.json()
            
            return second_data['choices'][0]['message']['content'].strip()

        else:
            # Normal text response
            return message['content'].strip()

    except Exception as e:
        logger.error(f"[NLP] Groq error: {e}")
        return "Sorry, I couldn’t reach Groq right now."
