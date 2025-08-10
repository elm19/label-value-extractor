# Key-Value Extractor from Images

This project is a desktop application that uses Optical Character Recognition (OCR) to extract key-value pairs from images.

## Project Structure

```
key-value-extractor/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── image_processing/
│   │   ├── __init__.py
│   │   └── processor.py
│   └── ui/
│       ├── __init__.py
│       └── main_window.py
├── notebooks/
│   └── ocr_exp1.ipynb
├── reports/
│   └── phase1:ocr.pdf
├── tests/
│   ├── __init__.py
│   ├── test_image_processing.py
│   └── test_ui.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python3 -m src.main
    ```
