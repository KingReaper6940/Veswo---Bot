from typing import Dict, Any, Optional
import re

class TaskRouter:
    def __init__(self):
        self.math_patterns = [
            r'solve\s+.*equation',
            r'calculate\s+.*',
            r'what\s+is\s+.*\?',
            r'find\s+.*',
        ]
        
        self.essay_patterns = [
            r'write\s+.*essay',
            r'help\s+me\s+write',
            r'create\s+.*about',
        ]
        
        self.image_patterns = [
            r'what\s+is\s+in\s+this\s+image',
            r'describe\s+this\s+image',
            r'analyze\s+this\s+picture',
        ]

    def route_task(self, content: str, task_type: str = "text") -> Dict[str, Any]:
        """
        Route the task to the appropriate handler based on content and type.
        Returns a dictionary with the task type and any additional metadata.
        """
        if task_type == "image":
            return {
                "type": "image_analysis",
                "handler": "image_analyzer",
                "metadata": {}
            }
        
        # Check for math-related queries
        for pattern in self.math_patterns:
            if re.search(pattern, content.lower()):
                return {
                    "type": "math_solver",
                    "handler": "math_solver",
                    "metadata": {"query": content}
                }
        
        # Check for essay-related queries
        for pattern in self.essay_patterns:
            if re.search(pattern, content.lower()):
                return {
                    "type": "essay_writer",
                    "handler": "essay_writer",
                    "metadata": {"topic": content}
                }
        
        # Default to general chat
        return {
            "type": "general_chat",
            "handler": "chat_handler",
            "metadata": {"query": content}
        }

    def get_handler(self, task_info: Dict[str, Any]) -> str:
        """
        Get the appropriate handler function name for the task.
        """
        return task_info["handler"] 