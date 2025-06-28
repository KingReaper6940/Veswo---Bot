import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import re
import json
from typing import Dict, Any, List

class GPT2Assistant:
    def __init__(self):
        """Initialize GPT-2 model and tokenizer"""
        self.model_name = "gpt2"
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        
        # Set pad token
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Move to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        
        print(f"GPT-2 model loaded on {self.device}")
    
    def generate_response(self, prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
        """Generate a response using GPT-2"""
        try:
            # Encode the prompt
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=512)
            inputs = inputs.to(self.device)
            
            # Create attention mask
            attention_mask = torch.ones_like(inputs)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    attention_mask=attention_mask,
                    max_length=inputs.shape[1] + max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2
                )
            
            # Decode the response
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the original prompt from the response
            if full_response.startswith(prompt):
                response = full_response[len(prompt):].strip()
            else:
                response = full_response.strip()
            
            # Clean up the response
            response = response.replace("Assistant:", "").strip()
            response = re.sub(r'\n+', '\n', response)  # Remove multiple newlines
            
            return response if response else "I'm sorry, I couldn't generate a response."
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I encountered an error: {str(e)}"
    
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
            return "Hello! I'm Veswo Assistant, powered by GPT-2. I can help you with math problems, essays, code, and science questions. How can I assist you today?"
        elif "how are you" in message_lower:
            return "I'm functioning well! I'm here to help you with your studies. What would you like to work on?"
        elif "what can you do" in message_lower or "help" in message_lower:
            return "I can help you with:\n• Math problems and equations\n• Writing essays and papers\n• Code debugging and explanation\n• Science questions (physics, chemistry, biology)\n• General study assistance\n\nJust ask me anything!"
        
        # Return empty string if no fallback is available
        return ""
    
    def solve_math_problem(self, problem: str) -> Dict[str, Any]:
        """Solve math problems using GPT-2 with fallbacks"""
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
            
            # Use GPT-2 for more complex problems
            prompt = f"Math problem: {problem}\nStep-by-step solution:"
            response = self.generate_response(prompt, max_length=200, temperature=0.3)
            
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
                "method": "GPT-2 AI Model"
            }
            
        except Exception as e:
            return {
                "solution": f"Error solving problem: {str(e)}",
                "steps": [f"Error: {str(e)}"],
                "method": "GPT-2 AI Model"
            }
    
    def write_essay(self, topic: str, essay_type: str = "analytical", length: str = "medium") -> Dict[str, Any]:
        """Write essays using GPT-2"""
        try:
            prompt = f"Write a {essay_type} essay about {topic}:\n\n"
            response = self.generate_response(prompt, max_length=300, temperature=0.8)
            
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
                    "method": "GPT-2 AI Model"
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
                    "method": "GPT-2 AI Model"
                }
            }
    
    def analyze_image_content(self, image_description: str, question: str) -> str:
        """Analyze image content using GPT-2 (based on description)"""
        try:
            prompt = f"Based on this image description: '{image_description}', answer this question: {question}\n\nAnswer:"
            response = self.generate_response(prompt, max_length=250, temperature=0.6)
            return response if response else "I cannot analyze this image content."
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    def help_with_code(self, code: str, question: str) -> str:
        """Help with code using GPT-2"""
        try:
            prompt = f"Code: {code}\n\nQuestion: {question}\n\nAnswer:"
            response = self.generate_response(prompt, max_length=300, temperature=0.5)
            return response if response else "I cannot help with this code question."
        except Exception as e:
            return f"Error helping with code: {str(e)}"
    
    def science_help(self, subject: str, question: str) -> str:
        """Provide science help using GPT-2"""
        try:
            prompt = f"Science question about {subject}: {question}\n\nAnswer:"
            response = self.generate_response(prompt, max_length=250, temperature=0.6)
            return response if response else f"I cannot help with this {subject} question."
        except Exception as e:
            return f"Error providing science help: {str(e)}"
    
    def general_chat(self, message: str) -> str:
        """Handle general chat using GPT-2 with fallbacks"""
        try:
            # Check for fallback responses first
            fallback = self.get_fallback_response(message)
            if fallback:
                return fallback
            
            # Use GPT-2 for other responses
            prompt = f"Question: {message}\nAnswer:"
            response = self.generate_response(prompt, max_length=150, temperature=0.6)
            
            # Clean up and limit response length
            response = response.strip()
            if len(response) > 500:
                response = response[:500] + "..."
            
            return response if response else "I'm sorry, I couldn't understand your message."
            
        except Exception as e:
            return f"Error in chat: {str(e)}" 