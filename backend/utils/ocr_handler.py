import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
from typing import Dict, Any, Optional

class OCRHandler:
    def __init__(self):
        # Configure Tesseract parameters
        self.config = '--oem 3 --psm 6'  # Assume single uniform text block
        
    def process_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Process an image and extract text using OCR.
        
        Args:
            image_data: Raw bytes of the image
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to OpenCV format for preprocessing
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocess image
            processed_image = self._preprocess_image(cv_image)
            
            # Perform OCR
            text = pytesseract.image_to_string(processed_image, config=self.config)
            
            return {
                "text": text.strip(),
                "confidence": 1.0,  # TODO: Implement confidence scoring
                "metadata": {
                    "image_size": image.size,
                    "format": image.format
                }
            }
            
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess the image to improve OCR accuracy.
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to get a binary image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary)
        
        return denoised 