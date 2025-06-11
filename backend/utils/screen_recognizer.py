import cv2
import numpy as np
import pytesseract
from PIL import Image
import pyautogui
from typing import Dict, Any, Optional, List, Tuple
import re

class ScreenRecognizer:
    def __init__(self):
        # Configure pytesseract path if needed
        # pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract'
        
        # Initialize screen capture settings
        self.screen_region = None  # (left, top, width, height)
        
        # Initialize OCR settings
        self.ocr_config = {
            'lang': 'eng',
            'config': '--psm 6'  # Assume uniform text block
        }
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Capture the screen or a region of the screen.
        
        Args:
            region: Optional tuple (left, top, width, height) defining screen region
            
        Returns:
            numpy array containing the screen capture
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            # Convert PIL Image to numpy array
            return np.array(screenshot)
            
        except Exception as e:
            raise Exception(f"Screen capture failed: {str(e)}")
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from an image using OCR.
        
        Args:
            image: numpy array containing the image
            
        Returns:
            Extracted text as string
        """
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image)
            
            # Perform OCR
            text = pytesseract.image_to_string(pil_image, **self.ocr_config)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Text extraction failed: {str(e)}")
    
    def find_text_on_screen(self, search_text: str, 
                           region: Optional[Tuple[int, int, int, int]] = None) -> List[Dict[str, Any]]:
        """
        Find specific text on the screen.
        
        Args:
            search_text: Text to search for
            region: Optional screen region to search in
            
        Returns:
            List of dictionaries containing found text locations and content
        """
        try:
            # Capture screen
            screen = self.capture_screen(region)
            
            # Extract text
            text = self.extract_text(screen)
            
            # Find matches
            matches = []
            for match in re.finditer(search_text, text, re.IGNORECASE):
                matches.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end()
                })
            
            return matches
            
        except Exception as e:
            raise Exception(f"Text search failed: {str(e)}")
    
    def analyze_screen_content(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Analyze screen content and return structured information.
        
        Args:
            region: Optional screen region to analyze
            
        Returns:
            Dictionary containing analyzed screen content
        """
        try:
            # Capture screen
            screen = self.capture_screen(region)
            
            # Extract text
            text = self.extract_text(screen)
            
            # Analyze content
            analysis = {
                'text_content': text,
                'word_count': len(text.split()),
                'line_count': len(text.splitlines()),
                'contains_numbers': bool(re.search(r'\d', text)),
                'contains_math': bool(re.search(r'[+\-*/=]', text)),
                'contains_urls': bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text))
            }
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Screen analysis failed: {str(e)}")
    
    def detect_math_equations(self, region: Optional[Tuple[int, int, int, int]] = None) -> List[Dict[str, Any]]:
        """
        Detect and extract mathematical equations from screen content.
        
        Args:
            region: Optional screen region to analyze
            
        Returns:
            List of dictionaries containing detected equations
        """
        try:
            # Capture screen
            screen = self.capture_screen(region)
            
            # Extract text
            text = self.extract_text(screen)
            
            # Find potential equations
            equations = []
            for line in text.splitlines():
                # Look for lines containing mathematical operators
                if re.search(r'[+\-*/=]', line):
                    equations.append({
                        'equation': line.strip(),
                        'type': self._classify_equation_type(line)
                    })
            
            return equations
            
        except Exception as e:
            raise Exception(f"Equation detection failed: {str(e)}")
    
    def _classify_equation_type(self, equation: str) -> str:
        """
        Classify the type of mathematical equation.
        
        Args:
            equation: The equation to classify
            
        Returns:
            String indicating equation type
        """
        if re.search(r'=', equation):
            if re.search(r'[<>≤≥]', equation):
                return 'inequality'
            return 'equation'
        elif re.search(r'[+\-*/]', equation):
            return 'expression'
        return 'unknown' 