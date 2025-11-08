import subprocess, json

def chat_reply(user_text: str) -> str:
    """Use local Llama3 (via Ollama) for free chat responses."""
    try:
        print("[NLP] Using local Ollama model (free) …")
        result = subprocess.run(
            ["ollama", "run", "llama3", user_text],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error running local model: {e}"
