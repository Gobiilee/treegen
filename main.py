import sys
from PyQt6.QtWidgets import QApplication
from viewmodels.main_viewmodel import MainViewModel
from views.main_window import MainWindow

def main() -> None:
    """Entry point for the application."""
    app = QApplication(sys.argv)
    
    # Instantiate MVVM layers
    view_model = MainViewModel()
    window = MainWindow(view_model)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()