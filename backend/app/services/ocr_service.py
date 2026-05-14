"""
OCR Service - Document Text Extraction

Handles document processing with:
- Tesseract OCR (fast, free)
- Ollama Vision Model fallback (accurate for handwritten/unclear docs)
- PDF to image conversion
- Multi-page document support

PHASE 4 IMPLEMENTATION
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from PIL import Image
import cv2
import numpy as np
from app.config import get_settings

settings = get_settings()

logger = logging.getLogger(__name__)


class OCRService:
    """
    Service for optical character recognition and document processing.
    """
    
    def __init__(self):
        """Initialize OCR service with dependencies."""
        self.enable_ocr = settings.ENABLE_OCR if hasattr(settings, 'ENABLE_OCR') else True
        self._init_tesseract()
    
    def _init_tesseract(self):
        """Initialize Tesseract OCR."""
        try:
            import pytesseract
            if settings.TESSERACT_PATH:
                pytesseract.pytesseract.pytesseract_cmd = settings.TESSERACT_PATH
            self.pytesseract = pytesseract
            logger.info("Tesseract OCR initialized successfully")
        except ImportError:
            logger.warning("Tesseract not available, vision fallback will be used")
            self.pytesseract = None
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document and extract text.
        
        Args:
            file_path: Path to document file (PDF, PNG, JPG, DOC, DOCX)
        
        Returns:
            Dict with extracted text, status, confidence, pages
        """
        try:
            file_ext = Path(file_path).suffix.lower()
            
            # Convert PDF to images
            if file_ext == ".pdf":
                images = self._convert_pdf_to_images(file_path)
            else:
                images = [Image.open(file_path)]
            
            # Process each page
            all_text = ""
            confidence_scores = []
            page_results = []
            
            for page_num, image in enumerate(images, 1):
                # Preprocess image
                processed_image = self._preprocess_image(image)
                
                # Extract text
                page_text, confidence = self._extract_text_with_ocr(processed_image)
                all_text += f"\n--- Page {page_num} ---\n{page_text}"
                confidence_scores.append(confidence)
                
                page_results.append({
                    "page_number": page_num,
                    "text": page_text,
                    "confidence": confidence
                })
            
            avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
            
            return {
                "status": "success" if avg_confidence > 0.5 else "partial",
                "full_text": all_text,
                "pages": page_results,
                "average_confidence": float(avg_confidence),
                "page_count": len(images),
                "recommendation": self._get_recommendation(avg_confidence)
            }
            
        except Exception as e:
            logger.error(f"OCR processing error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "full_text": "",
                "pages": [],
                "average_confidence": 0.0
            }
    
    def _convert_pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Convert PDF to list of PIL Images."""
        try:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path)
            logger.info(f"Converted PDF to {len(images)} images")
            return images
        except Exception as e:
            logger.error(f"PDF conversion error: {e}")
            raise
    
    def _preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy.
        
        Applies:
        - Grayscale conversion
        - Noise removal
        - Thresholding
        - Dilation/Erosion
        """
        # Convert PIL to CV2
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(gray, h=10)
        
        # Thresholding
        _, thresh = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)
        
        # Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return processed
    
    def _extract_text_with_ocr(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Extract text from image using Tesseract.
        Falls back to vision model if Tesseract unavailable.
        
        Returns:
            Tuple of (text, confidence_score)
        """
        # Try Tesseract first
        if self.pytesseract:
            try:
                # Convert numpy array to PIL for Tesseract
                pil_image = Image.fromarray(image)
                text = self.pytesseract.image_to_string(
                    pil_image,
                    lang=settings.OCR_LANGUAGE
                )
                
                # Get confidence data
                data = self.pytesseract.image_to_data(pil_image, output_type='dict')
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = (np.mean(confidences) / 100) if confidences else 0.5
                
                return text.strip(), float(avg_confidence)
                
            except Exception as e:
                logger.warning(f"Tesseract error, trying vision model: {e}")
        
        # Fallback to vision model
        return self._extract_text_with_vision(image)
    
    def _extract_text_with_vision(self, image: np.ndarray) -> Tuple[str, float]:
        """
        Extract text using Ollama vision model as fallback.
        For complex/handwritten documents.
        Uses Ollama /api/chat with proper multimodal format (images array).
        """
        try:
            pil_image = Image.fromarray(image)
            import base64
            import io
            import httpx

            buffered = io.BytesIO()
            pil_image.save(buffered, format="PNG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

            # Call Ollama /api/chat with vision model using proper multimodal format
            response = httpx.post(
                f"{settings.OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": settings.OLLAMA_VISION_MODEL,
                    "messages": [{
                        "role": "user",
                        "content": "Extract ALL text from this document image. Return only the extracted text, nothing else.",
                        "images": [img_b64],
                    }],
                    "stream": False,
                    "options": {"temperature": 0.0},
                },
                timeout=120.0,
            )
            response.raise_for_status()
            data = response.json()
            text = data.get("message", {}).get("content", "").strip()
            return text, 0.7

        except httpx.HTTPStatusError as e:
            if "does not support image input" in str(e):
                logger.warning(
                    f"Model '{settings.OLLAMA_VISION_MODEL}' does not support vision. "
                    f"Install a vision model (e.g., 'ollama pull llama3.2-vision') or set OLLAMA_VISION_MODEL to one that supports images."
                )
            else:
                logger.error(f"Vision model HTTP error: {e}")
            return "", 0.0
        except Exception as e:
            logger.error(f"Vision model error: {e}")
            return "", 0.0
    
    def _get_recommendation(self, confidence: float) -> str:
        """Get recommendation based on confidence score."""
        if confidence >= 0.85:
            return "APPROVED - High confidence in document quality"
        elif confidence >= 0.65:
            return "APPROVED_WITH_REVIEW - Medium confidence, manual review recommended"
        elif confidence >= 0.40:
            return "REJECTED_UNCLEAR - Document too unclear, ask for resubmission"
        else:
            return "REJECTED_UNREADABLE - Cannot extract text, resubmit clear document"
    
    def validate_document_format(self, file_path: str) -> Tuple[bool, str]:
        """
        Validate if file is acceptable document format.
        
        Returns:
            Tuple of (is_valid, message)
        """
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext not in [f".{ext}" for ext in settings.ALLOWED_FILE_TYPES]:
            return False, f"File type {file_ext} not allowed. Allowed: {settings.ALLOWED_FILE_TYPES}"
        
        file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
        if file_size_mb > settings.MAX_UPLOAD_SIZE_MB:
            return False, f"File too large ({file_size_mb:.1f}MB). Max: {settings.MAX_UPLOAD_SIZE_MB}MB"
        
        return True, "Document format valid"
    
    def extract_key_fields(self, text: str) -> Dict[str, Any]:
        """
        Extract key information from document text.
        
        Looks for:
        - Student name
        - Roll number / ID
        - College name
        - Marks/Grades
        - Date of issue
        """
        import re
        
        extracted = {
            "name": self._extract_name(text),
            "roll_number": self._extract_roll_number(text),
            "dates": self._extract_dates(text),
            "numbers": self._extract_important_numbers(text),
            "college_name": self._extract_college_name(text),
        }
        
        return extracted
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract student name from text."""
        # Simple pattern - name usually near beginning
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            if len(line) > 5 and len(line) < 50 and line.isupper():
                return line.strip()
        return None
    
    def _extract_roll_number(self, text: str) -> Optional[str]:
        """Extract roll/ID number."""
        import re
        match = re.search(r'(Roll[#\s]?No?\.?|ID)[:\s]+(\d{2,}[A-Z]?\d*)', text, re.IGNORECASE)
        return match.group(2) if match else None
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from document."""
        import re
        date_pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        return re.findall(date_pattern, text)
    
    def _extract_important_numbers(self, text: str) -> List[str]:
        """Extract important numbers (marks, etc)."""
        import re
        numbers = re.findall(r'\b\d{2,3}(?:\.\d+)?\b', text)
        return list(set(numbers))  # Unique
    
    def _extract_college_name(self, text: str) -> Optional[str]:
        """Extract college/institution name."""
        import re
        pattern = r'(Institute|University|College|School|Academy)[^,.]+'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(0).strip() if match else None


# Create module-level service instance
ocr_service = OCRService()
