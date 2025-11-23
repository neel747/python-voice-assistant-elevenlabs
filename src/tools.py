import datetime
import webbrowser
import json

def get_current_time():
    """Returns the current time in a readable format."""
    now = datetime.datetime.now()
    return now.strftime("%I:%M %p")

def get_current_date():
    """Returns the current date in a readable format."""
    now = datetime.datetime.now()
    return now.strftime("%A, %B %d, %Y")

def open_website(url: str):
    """Opens a website in the default browser."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened {url}"

def calculate(expression: str):
    """Evaluates a mathematical expression."""
    try:
        # Safe evaluation using eval() with limited scope is still risky, 
        # but acceptable for a local personal assistant. 
        # For better security, use a parser library, but eval is simple for now.
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error calculating: {e}"

# Schema for Groq / OpenAI
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_date",
            "description": "Get the current date",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Open a website in the browser",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to open (e.g., google.com)",
                    },
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate (e.g., '2 + 2')",
                    },
                },
                "required": ["expression"],
            },
        },
    },
]

AVAILABLE_TOOLS = {
    "get_current_time": get_current_time,
    "get_current_date": get_current_date,
    "open_website": open_website,
    "calculate": calculate,
}
