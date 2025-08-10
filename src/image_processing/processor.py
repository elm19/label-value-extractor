import cv2
import os

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
        
        # Extract the text
        extracted_text = ""
        for line in result[0]["rec_texts"]:
            extracted_text += line + "\n"
            

        return "output/1.png", extracted_text
            
    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return None, None
