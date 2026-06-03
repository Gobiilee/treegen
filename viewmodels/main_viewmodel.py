from PyQt6.QtCore import QObject, pyqtSignal, QThread
from models.tree_creator import SkeletonBuilder, BuildResult

class BuildWorker(QThread):
    """Background thread to process the file I/O operations without freezing UI."""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(BuildResult)

    def __init__(self, builder: SkeletonBuilder, tree_files: list[str], output_dir: str):
        super().__init__()
        self.builder = builder
        self.tree_files = tree_files
        self.output_dir = output_dir

    def run(self) -> None:
        """Executes the build command in the background."""
        self.log_signal.emit(f"Starting build from {len(self.tree_files)} file(s)...")
        result = self.builder.parse_and_build(self.tree_files, self.output_dir)
        self.finished_signal.emit(result)


class MainViewModel(QObject):
    """Bridges the View and the Model, managing state and thread execution."""
    log_updated = pyqtSignal(str)
    ui_state_changed = pyqtSignal(bool) # True if busy, False if idle

    def __init__(self) -> None:
        super().__init__()
        self.builder = SkeletonBuilder()
        self._worker: BuildWorker | None = None

    def start_build(self, tree_files: list[str], output_dir: str) -> None:
        """
        Initiates the background folder creation process.
        
        Args:
            tree_files: List of file paths to process.
            output_dir: Target root directory.
        """
        if not tree_files or not output_dir:
            self.log_updated.emit("Error: Please select input files and an output directory.")
            return

        self.ui_state_changed.emit(True)
        self._worker = BuildWorker(self.builder, tree_files, output_dir)
        self._worker.log_signal.connect(self.log_updated.emit)
        self._worker.finished_signal.connect(self._on_build_finished)
        self._worker.start()

    def undo_build(self) -> None:
        """Reverts the changes made by the last build operation."""
        self.log_updated.emit("Attempting to undo last build...")
        result = self.builder.undo_last_build()
        
        if result.success:
            self.log_updated.emit(f"Success: {result.message}")
        else:
            self.log_updated.emit(f"Notice: {result.message}")

    def _on_build_finished(self, result: BuildResult) -> None:
        """Callback executed when the build thread completes."""
        if result.success:
            self.log_updated.emit(f"Success: Created {result.created_count} items.")
        else:
            self.log_updated.emit(f"Error: {result.message}")
            
        self.ui_state_changed.emit(False)