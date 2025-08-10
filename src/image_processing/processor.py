import os

import arabic_reshaper
from bidi.algorithm import get_display


def process_arabic_text(text):
    """Process Arabic text for proper display (right-to-left)"""
    try:
      parts = text.split()

      fixed_parts = []
      for part in parts:
          # Reverse Arabic-like parts only (heuristic: check if contains Arabic letters)
          if any('\u0600' <= c <= '\u06FF' for c in part):
              part = part[::-1]  # Reverse characters in the part
          fixed_parts.append(part)

      fixed_text = " ".join(fixed_parts)
      # Reshape Arabic text for proper display
      reshaped_text = arabic_reshaper.reshape(fixed_text)
      # Apply bidirectional algorithm
      display_text = get_display(reshaped_text)
      return display_text
    except:
        # If reshaping fails, return original text
        print("failed")
        return text

def process_image(image_path, ocr):
    """
    Process the image using PaddleOCR to extract text.
    """
    try:
        # Perform OCR
        
        result = ocr.predict(image_path)
        
        # Save the image with bounding boxes
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # It seems that predict returns a list of results, one for each page.
        # We will assume there is only one page.
        res = result[0]
        
        # img_path = os.path.join(output_dir, "processed_image.jpg")
        res.save_to_img(output_dir)
        # res.save_to_json(output_dir)
        
        # Process Arabic text
        extracted_text = ""
        for i, line in enumerate(res["rec_texts"]):
            res["rec_texts"][i] = process_arabic_text(line)
            extracted_text += res["rec_texts"][i] + "\n"
            print(f"Line {i}: {res['rec_texts'][i]}")

        res.save_to_json(output_dir)
        
        return "output/temp_image_0_ocr_res_img.png", extracted_text
            
    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return None, None
