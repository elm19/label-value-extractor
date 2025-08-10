import os
import tempfile
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFileDialog,
                            QMessageBox, QFrame, QTextEdit, QStackedWidget)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont
from paddleocr import PaddleOCR

from ..image_processing.processor import process_image

class Worker(QThread):
    """Worker thread for image processing"""
    finished = pyqtSignal(str, str)

    def __init__(self, image_path, ocr):
        super().__init__()
        self.image_path = image_path
        self.ocr = ocr

    def run(self):
        processed_image_path, extracted_text = process_image(self.image_path, self.ocr)
        self.finished.emit(processed_image_path, extracted_text)

class ImageUploadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_image_path = None
        self.ocr_fr = PaddleOCR(
            lang="ar",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )
        self.setup_ui()
        
    def setup_ui(self):
        # Set window properties
        self.setWindowTitle("OCR Label-Value Extraction Tool")
        self.setGeometry(100, 100, 1200, 700)
        self.setMinimumSize(1000, 600)
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create pages
        self.page1_upload = QWidget()
        self.page2_results = QWidget()

        self.create_page1_upload()
        self.create_page2_results()

        self.stacked_widget.addWidget(self.page1_upload)
        self.stacked_widget.addWidget(self.page2_results)

        # Apply styling
        self.apply_styling()

    def create_page1_upload(self):
        """Create the UI for the first page (uploading image)"""
        layout = QVBoxLayout(self.page1_upload)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        self.create_title(layout)
        
        # Buttons section
        self.create_buttons(layout)
        
        # Image display section
        self.create_image_display(layout)
        
        # Status label
        self.create_status_label(layout)

    def create_page2_results(self):
        """Create the UI for the second page (displaying results)"""
        main_layout = QVBoxLayout(self.page2_results)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("Processing Results")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Results container
        results_container = QFrame()
        results_container.setFrameStyle(QFrame.Shape.Box)
        results_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        main_layout.addWidget(results_container)

        results_layout = QHBoxLayout(results_container)
        results_layout.setSpacing(20)

        # Processed image display
        self.processed_image_label = QLabel()
        self.processed_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        results_layout.addWidget(self.processed_image_label, 1)

        # Extracted text display
        self.results_text_edit = QTextEdit()
        self.results_text_edit.setFont(QFont("Arial", 12))
        self.results_text_edit.setReadOnly(True)
        self.results_text_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        results_layout.addWidget(self.results_text_edit, 1)

        # Add button to go back to step 1 or upload new photo
        self.back_to_upload_btn = QPushButton("Back to Upload / New Photo")
        self.back_to_upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        self.back_to_upload_btn.clicked.connect(self._on_back_to_step1_or_upload_new_photo_clicked)
        main_layout.addWidget(self.back_to_upload_btn)

    def create_title(self, layout):
        """Create the title section"""
        title_label = QLabel("OCR Document Processing")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Style the title
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        
        layout.addWidget(title_label)
    
    def create_buttons(self, layout):
        """Create the button section"""
        # Create buttons container
        button_container = QFrame()
        button_container.setFrameStyle(QFrame.Shape.Box)
        button_container.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(30)
        
        # Take Picture button (disabled for now)
        self.take_picture_btn = QPushButton("📷 Take Picture")
        self.take_picture_btn.setEnabled(False)  # Disabled for now
        self.take_picture_btn.clicked.connect(self.take_picture)
        
        # Upload Picture button
        self.upload_btn = QPushButton("📁 Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        
        # Style buttons
        button_style = """
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 200px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #ffffff;
            }
        """
        
        self.take_picture_btn.setStyleSheet(button_style)
        self.upload_btn.setStyleSheet(button_style)
        
        # Add buttons to layout
        button_layout.addWidget(self.take_picture_btn)
        button_layout.addWidget(self.upload_btn)
        
        layout.addWidget(button_container)
    
    def create_image_display(self, layout):
        """Create the image display section"""
        # Image container
        image_container = QFrame()
        image_container.setFrameStyle(QFrame.Shape.Box)
        image_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px dashed #adb5bd;
                border-radius: 10px;
                min-height: 400px;
            }
        """)
        
        image_layout = QVBoxLayout(image_container)
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(600, 350)
        self.image_label.setStyleSheet("""
            QLabel {
                border: none;
                background-color: transparent;
                color: #6c757d;
                font-size: 18px;
            }
        """)
        self.image_label.setText("No image selected\n\nClick 'Upload Image' to select an image file")
        
        image_layout.addWidget(self.image_label)
        layout.addWidget(image_container)

    def create_status_label(self, layout):
        """Create status label"""
        self.status_label = QLabel("Ready to process images")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #28a745;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.status_label)
    
    def apply_styling(self):
        """Apply general styling to the window"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QWidget {
                background-color: #ffffff;
            }
        """)
    
    def take_picture(self):
        """Handle take picture button click - placeholder for now"""
        QMessageBox.information(
            self,
            "Feature Not Available",
            "Camera functionality will be implemented in a future update."
        )
    
    def upload_image(self):
        """Handle upload image button click"""
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff *.gif);;All Files (*)"
        )
        
        if file_path:
            # Save the image to a temporary file
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, "temp_image_0.png")
            pixmap = QPixmap(file_path)
            pixmap.save(temp_path, "PNG")
            self.current_image_path = temp_path

            # Display the original image
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.width() - 20,
                self.image_label.height() - 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

            # Start processing the image in a separate thread
            self.status_label.setText("Processing image...")
            self.worker = Worker(self.current_image_path, self.ocr_fr)
            self.worker.finished.connect(self.processing_finished)
            self.worker.start()

    def processing_finished(self, processed_image_path, extracted_text):
        """Handle the finished signal from the worker thread"""
        if processed_image_path and extracted_text:
            # Display the processed image
            pixmap = QPixmap(processed_image_path)
            self.processed_image_label.setPixmap(pixmap.scaled(
                self.processed_image_label.width() - 20,
                self.processed_image_label.height() - 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

            # Display the extracted text
            self.results_text_edit.setText(extracted_text)
            # print(f"Extracted Text: {extracted_text}")

            # Switch to the results page
            self.stacked_widget.setCurrentWidget(self.page2_results)
        else:
            self.show_error("Error", "Failed to process the image.")

    def show_error(self, title, message):
        """Show error message box"""
        QMessageBox.critical(self, title, message)
        self.status_label.setText("Error loading image")
        self.status_label.setStyleSheet(
            """"
           
            QLabel {
                color: #721c24;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 5px;
            }
             """
        )

    def _on_back_to_step1_or_upload_new_photo_clicked(self):
        """
        Handles the click event for the "Back to Upload / New Photo" button.
        Switches the view back to the image upload page (page1).
        """
        self.stacked_widget.setCurrentWidget(self.page1_upload)
        self.status_label.setText("Ready to process images")
        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #28a745;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
            }
            """
        )
        self.image_label.setText("No image selected\n\nClick 'Upload Image' to select an image file")
        self.image_label.setPixmap(QPixmap())
        self.results_text_edit.clear()
        self.processed_image_label.clear()