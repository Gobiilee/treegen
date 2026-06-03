from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QTextEdit, 
                             QLineEdit, QListWidget)
from viewmodels.main_viewmodel import MainViewModel

class MainWindow(QMainWindow):
    """The graphical user interface for the application."""
    
    def __init__(self, view_model: MainViewModel) -> None:
        super().__init__()
        self.vm = view_model
        
        self.setWindowTitle("MVVM Skeleton Builder")
        self.resize(600, 500)
        
        self.tree_files: list[str] = []
        
        self._setup_ui()
        self._bind_view_model()

    def _setup_ui(self) -> None:
        """Instantiates and arranges all UI widgets."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Input Files Section
        layout.addWidget(QLabel("Select Tree Text Files:"))
        file_layout = QHBoxLayout()
        self.file_list = QListWidget()
        self.file_list.setMaximumHeight(30)
        file_btn = QPushButton("Browse Files")
        file_btn.clicked.connect(self._browse_files)
        file_layout.addWidget(self.file_list)
        file_layout.addWidget(file_btn)
        layout.addLayout(file_layout)

        # Output Directory Section
        dst_layout = QHBoxLayout()
        self.dst_input = QLineEdit()
        self.dst_input.setPlaceholderText("Select Destination Folder...")
        dst_btn = QPushButton("Browse Output")
        dst_btn.clicked.connect(self._browse_output)
        dst_layout.addWidget(QLabel("Output Root:"))
        dst_layout.addWidget(self.dst_input)
        dst_layout.addWidget(dst_btn)
        layout.addLayout(dst_layout)

        # Log Area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(QLabel("Execution Logs:"))
        layout.addWidget(self.log_area)

        # Control Buttons
        btn_layout = QHBoxLayout()
        self.build_btn = QPushButton("Build Structure")
        self.undo_btn = QPushButton("Undo Last Build")
        self.undo_btn.setStyleSheet("background-color: #ffcccc; color: black;")
        
        btn_layout.addWidget(self.build_btn)
        btn_layout.addWidget(self.undo_btn)
        layout.addLayout(btn_layout)

        # Connections
        self.build_btn.clicked.connect(self._on_build_clicked)
        self.undo_btn.clicked.connect(self.vm.undo_build)

    def _bind_view_model(self) -> None:
        """Connects ViewModel signals to UI updates."""
        self.vm.log_updated.connect(self.log_area.append)
        self.vm.ui_state_changed.connect(self._update_button_states)

    def _browse_files(self) -> None:
        """Opens a file dialog allowing multi-selection of .txt files."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Tree Files", "", "Text Files (*.txt);;All Files (*)"
        )
        if files:
            self.tree_files = files
            self.file_list.clear()
            self.file_list.addItems([f.split('/')[-1] for f in files]) # Show just filenames

    def _browse_output(self) -> None:
        """Opens a directory dialog for the output path."""
        folder = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if folder:
            self.dst_input.setText(folder)

    def _on_build_clicked(self) -> None:
        """Passes the UI data to the ViewModel to start the process."""
        self.log_area.clear()
        self.vm.start_build(self.tree_files, self.dst_input.text())

    def _update_button_states(self, is_busy: bool) -> None:
        """Disables the build button while a process is actively running."""
        self.build_btn.setEnabled(not is_busy)