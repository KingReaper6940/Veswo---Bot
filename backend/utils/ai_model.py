import requests

class GemmaAssistant:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model="gemma"):
        self.ollama_url = ollama_url
        self.model = model
        print(f"Gemma AI backend initialized using Ollama at {self.ollama_url} with model '{self.model}'")

    def chat(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.ollama_url, json=payload)
        response.raise_for_status()
        return response.json()["response"]

    # You can add more methods for essay, code, etc., if needed, using the same pattern. 