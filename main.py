import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.ui.main_window import ImageUploadWindow


def main():
    # Set Qt platform plugin explicitly for Linux
    os.environ.setdefault('QT_QPA_PLATFORM', 'xcb')
    
    # Create application
    app = QApplication(sys.argv)
    
    # Enable high DPI scaling (PyQt6 compatible)
    try:
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    except AttributeError:
        # PyQt6 handles DPI scaling automatically, these attributes were removed
        pass
    
    # Create and show main window
    window = ImageUploadWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
