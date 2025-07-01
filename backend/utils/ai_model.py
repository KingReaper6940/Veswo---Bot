import torch
from transformers.pipelines import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
import json
from typing import Dict, Any, List

class Llama3Assistant:
    def __init__(self, model_name="meta-llama/Meta-Llama-3-7B-Instruct", device=None):
        print("Loading Llama 3 7B model... (this may take a while on first run)")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, device_map="auto")
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, max_new_tokens=512, do_sample=True, temperature=0.7)
        print("Llama 3 7B loaded!")

    def chat(self, messages):
        # messages: list of dicts with 'role' and 'content'
        prompt = self._format_prompt(messages)
        outputs = self.generator(prompt, return_full_text=False)
        if isinstance(outputs, list) and outputs and isinstance(outputs[0], dict) and "generated_text" in outputs[0]:
            response = outputs[0]["generated_text"]
        else:
            response = ""
        if isinstance(response, str):
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            return response.strip()
        return str(response)

    def _format_prompt(self, messages):
        # Format as ChatML for Llama 3 instruct
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"<|system|> {msg['content']}\n"
            elif msg["role"] == "user":
                prompt += f"<|user|> {msg['content']}\n"
            elif msg["role"] == "assistant":
                prompt += f"<|assistant|> {msg['content']}\n"
        prompt += "<|assistant|> "
        return prompt

    def get_fallback_response(self, message: str) -> str:
        """Get fallback responses for common educational queries"""
        message_lower = message.lower()
        
        # Math responses
        if "2+2" in message_lower or "what is 2+2" in message_lower:
            return "2 + 2 = 4. This is a basic addition problem."
        elif "1+1" in message_lower:
            return "1 + 1 = 2. This is the most basic addition."
        elif "5+5" in message_lower:
            return "5 + 5 = 10. This is addition of two equal numbers."
        
        # General knowledge
        elif "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm Veswo Assistant, powered by Llama 3 7B. I can help you with math problems, essays, code, and science questions. How can I assist you today?"
        elif "how are you" in message_lower:
            return "I'm functioning well! I'm here to help you with your studies. What would you like to work on?"
        elif "what can you do" in message_lower or "help" in message_lower:
            return "I can help you with:\n• Math problems and equations\n• Writing essays and papers\n• Code debugging and explanation\n• Science questions (physics, chemistry, biology)\n• General study assistance\n\nJust ask me anything!"
        
        # Return empty string if no fallback is available
        return ""
    
    def solve_math_problem(self, problem: str) -> Dict[str, Any]:
        """Solve math problems using Llama 3 7B with fallbacks"""
        try:
            # Check for simple arithmetic first
            try:
                # Try to evaluate simple expressions
                import ast
                tree = ast.parse(problem, mode='eval')
                result = eval(compile(tree, '<string>', 'eval'))
                return {
                    "solution": f"The answer is: {result}",
                    "steps": [f"Evaluated: {problem} = {result}"],
                    "method": "Direct Evaluation"
                }
            except:
                pass
            
            # Use Llama 3 7B for more complex problems
            prompt = f"Math problem: {problem}\nStep-by-step solution:"
            response = self.chat([{"role": "user", "content": prompt}])
            
            # Extract steps from the response
            steps = []
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Step-by-step solution:'):
                    steps.append(line)
            
            return {
                "solution": response,
                "steps": steps if steps else [response],
                "method": "Llama 3 7B AI Model"
            }
            
        except Exception as e:
            return {
                "solution": f"Error solving problem: {str(e)}",
                "steps": [f"Error: {str(e)}"],
                "method": "Llama 3 7B AI Model"
            }
    
    def write_essay(self, topic: str, essay_type: str = "analytical", length: str = "medium") -> Dict[str, Any]:
        """Write essays using Llama 3 7B"""
        try:
            prompt = f"Write a {essay_type} essay about {topic}:\n\n"
            response = self.chat([{"role": "user", "content": prompt}])
            
            # Clean up the response
            response = response.strip()
            
            # Estimate word count
            word_count = len(response.split())
            
            return {
                "content": response,
                "metadata": {
                    "type": essay_type,
                    "tone": "formal",
                    "length": length,
                    "word_count": word_count,
                    "method": "Llama 3 7B AI Model"
                }
            }
            
        except Exception as e:
            return {
                "content": f"Error writing essay: {str(e)}",
                "metadata": {
                    "type": essay_type,
                    "tone": "formal",
                    "length": length,
                    "word_count": 0,
                    "method": "Llama 3 7B AI Model"
                }
            }
    
    def analyze_image_content(self, image_description: str, question: str) -> str:
        """Analyze image content using Llama 3 7B (based on description)"""
        try:
            prompt = f"Based on this image description: '{image_description}', answer this question: {question}\n\nAnswer:"
            response = self.chat([{"role": "user", "content": prompt}])
            return response if response else "I cannot analyze this image content."
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def help_with_code(self, code: str, question: str) -> str:
        """Help with code using Llama 3 7B"""
        try:
            prompt = f"Code: {code}\n\nQuestion: {question}\n\nAnswer:"
            response = self.chat([{"role": "user", "content": prompt}])
            return response if response else "I cannot help with this code question."
        except Exception as e:
            return f"Error helping with code: {str(e)}"
    
    def science_help(self, subject: str, question: str) -> str:
        """Provide science help using Llama 3 7B"""
        try:
            prompt = f"Science question about {subject}: {question}\n\nAnswer:"
            response = self.chat([{"role": "user", "content": prompt}])
            return response if response else f"I cannot help with this {subject} question."
        except Exception as e:
            return f"Error providing science help: {str(e)}"
    
    def general_chat(self, message: str) -> str:
        """Handle general chat using Llama 3 7B with fallbacks"""
        try:
            # Check for fallback responses first
            fallback = self.get_fallback_response(message)
            if fallback:
                return fallback
            
            # Use Llama 3 7B for other responses
            prompt = f"Question: {message}\nAnswer:"
            response = self.chat([{"role": "user", "content": prompt}])
            
            # Clean up and limit response length
            response = response.strip()
            if len(response) > 500:
                response = response[:500] + "..."
            
            return response if response else "I'm sorry, I couldn't understand your message."
            
        except Exception as e:
            return f"Error in chat: {str(e)}" 