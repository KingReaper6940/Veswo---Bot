from typing import Dict, Any, Optional, List
import re
import random

class EssayWriter:
    def __init__(self):
        self.essay_types = {
            'persuasive': self._write_persuasive,
            'analytical': self._write_analytical,
            'descriptive': self._write_descriptive,
            'narrative': self._write_narrative
        }
        
        self.tone_options = {
            'formal': self._formal_tone,
            'casual': self._casual_tone,
            'academic': self._academic_tone
        }
        
        # Essay structure templates
        self.structure_templates = {
            'persuasive': [
                "Introduction with thesis statement",
                "First argument with supporting evidence",
                "Second argument with supporting evidence",
                "Third argument with supporting evidence",
                "Counterargument and rebuttal",
                "Conclusion with call to action"
            ],
            'analytical': [
                "Introduction with topic overview",
                "First point of analysis",
                "Second point of analysis",
                "Third point of analysis",
                "Synthesis of findings",
                "Conclusion with implications"
            ],
            'descriptive': [
                "Introduction setting the scene",
                "First major detail or aspect",
                "Second major detail or aspect",
                "Third major detail or aspect",
                "Sensory details and atmosphere",
                "Conclusion with reflection"
            ],
            'narrative': [
                "Introduction with setting",
                "Rising action",
                "Climax",
                "Falling action",
                "Character development",
                "Conclusion with resolution"
            ]
        }
    
    def generate_essay(self, topic: str, essay_type: str = 'analytical', 
                      tone: str = 'formal', length: str = 'medium') -> Dict[str, Any]:
        """
        Generate an essay based on the given parameters.
        
        Args:
            topic: The essay topic
            essay_type: Type of essay (persuasive, analytical, etc.)
            tone: Writing tone (formal, casual, academic)
            length: Essay length (short, medium, long)
            
        Returns:
            Dictionary containing the essay and metadata
        """
        try:
            if essay_type not in self.essay_types:
                raise ValueError(f"Unsupported essay type: {essay_type}")
            
            if tone not in self.tone_options:
                raise ValueError(f"Unsupported tone: {tone}")
            
            # Get the appropriate writer function
            writer_func = self.essay_types[essay_type]
            
            # Generate the essay
            essay = writer_func(topic, tone, length)
            
            # Apply the selected tone
            essay["content"] = self.tone_options[tone](essay["content"])
            
            return {
                "content": essay["content"],
                "outline": essay["outline"],
                "metadata": {
                    "type": essay_type,
                    "tone": tone,
                    "length": length,
                    "word_count": len(essay["content"].split())
                }
            }
            
        except Exception as e:
            raise Exception(f"Essay generation failed: {str(e)}")
    
    def _write_persuasive(self, topic: str, tone: str, length: str) -> Dict[str, Any]:
        """
        Generate a persuasive essay.
        """
        outline = self.structure_templates['persuasive']
        
        # Generate content based on outline
        content = f"# {topic}\n\n"
        content += "## Introduction\n"
        content += f"In today's world, {topic} has become increasingly important. "
        content += "This essay will argue that [thesis statement].\n\n"
        
        for section in outline[1:]:
            content += f"## {section}\n"
            content += self._generate_paragraph(section, topic)
            content += "\n\n"
        
        return {
            "content": content,
            "outline": outline
        }
    
    def _write_analytical(self, topic: str, tone: str, length: str) -> Dict[str, Any]:
        """
        Generate an analytical essay.
        """
        outline = self.structure_templates['analytical']
        
        content = f"# {topic}\n\n"
        content += "## Introduction\n"
        content += f"This analysis examines {topic} from multiple perspectives. "
        content += "Through careful examination, we will explore [main points].\n\n"
        
        for section in outline[1:]:
            content += f"## {section}\n"
            content += self._generate_paragraph(section, topic)
            content += "\n\n"
        
        return {
            "content": content,
            "outline": outline
        }
    
    def _write_descriptive(self, topic: str, tone: str, length: str) -> Dict[str, Any]:
        """
        Generate a descriptive essay.
        """
        outline = self.structure_templates['descriptive']
        
        content = f"# {topic}\n\n"
        content += "## Introduction\n"
        content += f"Let me take you on a journey through {topic}. "
        content += "Through vivid descriptions, we will explore [main aspects].\n\n"
        
        for section in outline[1:]:
            content += f"## {section}\n"
            content += self._generate_paragraph(section, topic)
            content += "\n\n"
        
        return {
            "content": content,
            "outline": outline
        }
    
    def _write_narrative(self, topic: str, tone: str, length: str) -> Dict[str, Any]:
        """
        Generate a narrative essay.
        """
        outline = self.structure_templates['narrative']
        
        content = f"# {topic}\n\n"
        content += "## Introduction\n"
        content += f"This story begins with {topic}. "
        content += "What follows is a journey through [main events].\n\n"
        
        for section in outline[1:]:
            content += f"## {section}\n"
            content += self._generate_paragraph(section, topic)
            content += "\n\n"
        
        return {
            "content": content,
            "outline": outline
        }
    
    def _generate_paragraph(self, section: str, topic: str) -> str:
        """
        Generate a paragraph for a given section.
        """
        # This is a placeholder. In a real implementation, this would use an LLM
        # to generate appropriate content based on the section and topic.
        return f"This section discusses {section.lower()} in relation to {topic}. "
    
    def _formal_tone(self, text: str) -> str:
        """
        Apply formal tone to text.
        """
        # Replace casual phrases with formal ones
        replacements = {
            "let's": "let us",
            "don't": "do not",
            "can't": "cannot",
            "won't": "will not",
            "it's": "it is",
            "that's": "that is"
        }
        
        for casual, formal in replacements.items():
            text = text.replace(casual, formal)
        
        return text
    
    def _casual_tone(self, text: str) -> str:
        """
        Apply casual tone to text.
        """
        # Replace formal phrases with casual ones
        replacements = {
            "let us": "let's",
            "do not": "don't",
            "cannot": "can't",
            "will not": "won't",
            "it is": "it's",
            "that is": "that's"
        }
        
        for formal, casual in replacements.items():
            text = text.replace(formal, casual)
        
        return text
    
    def _academic_tone(self, text: str) -> str:
        """
        Apply academic tone to text.
        """
        # Add academic phrases and structure
        text = self._formal_tone(text)
        
        # Add academic transitions
        transitions = [
            "Furthermore,",
            "Moreover,",
            "In addition,",
            "Consequently,",
            "Therefore,",
            "Thus,"
        ]
        
        # Add random academic transitions
        paragraphs = text.split("\n\n")
        for i in range(1, len(paragraphs)):
            if random.random() < 0.3:  # 30% chance to add transition
                paragraphs[i] = f"{random.choice(transitions)} {paragraphs[i]}"
        
        return "\n\n".join(paragraphs) 