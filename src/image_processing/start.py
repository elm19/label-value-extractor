from paddleocr import PaddleOCR

def init_ocr():
    """
    Initialize the OCR engine.
    """
    lang = ["fr", "ar"]  
    try:
        ocrs = []
        # Initialize PaddleOCR
        for lang_code in lang:
            ocr = PaddleOCR(
                lang=lang_code,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False
            )  # Set language to English
            ocrs.append(ocr)
        return ocrs
    
    except Exception as e:
        print(f"Error initializing OCR: {e}")
        return None