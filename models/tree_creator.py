import re
from pathlib import Path
from dataclasses import dataclass

@dataclass
class BuildResult:
    """Output data structure for the build operation."""
    success: bool
    message: str
    created_count: int = 0

class SkeletonBuilder:
    """Core business logic for parsing tree files and building directories."""
    
    def __init__(self) -> None:
        """Initializes the builder and the history tracker for the undo function."""
        self._history: list[Path] = []

    def parse_and_build(self, tree_files: list[str], output_dir: str) -> BuildResult:
        """Reads complex tree structures and builds the hierarchy accurately."""
        out_path = Path(output_dir)
        if not out_path.exists():
            return BuildResult(False, f"Error: Output directory does not exist -> {output_dir}")

        self._history.clear()
        total_created = 0

        for tree_file in tree_files:
            file_path = Path(tree_file)
            if not file_path.exists():
                continue

            lines = file_path.read_text(encoding="utf-8").splitlines()
            
            # Dictionary tracking the current "father" directory at every depth level.
            # Level -1 represents the base output folder.
            folder_hierarchy: dict[int, Path] = {-1: out_path}

            for line in lines:
                # 1. Standardize hidden characters 
                # (Converts Tabs to 4 spaces, and web non-breaking spaces to standard spaces)
                line = line.replace('\t', '    ').replace('\xa0', ' ')
                
                if not line.strip():
                    continue

                # 2. Match the entire visual prefix (spaces + tree characters)
                # Regex looks at the start of the line (^) for any combination of these characters
                prefix_match = re.match(r'^[\s│├└─]*', line)
                prefix = prefix_match.group(0) if prefix_match else ""
                
                # 3. Extract the actual folder/file name (everything after the prefix)
                name = line[len(prefix):].strip()
                
                # Skip lines that are just structural lines (e.g., a line with only "│")
                if not name:
                    continue

                # 4. Calculate depth based on the total visual length of the prefix
                # Standard tree formats use blocks of 4 characters per depth level
                depth = len(prefix) // 4

                if name.endswith("/"):
                    # IT IS A FOLDER
                    folder_name = name[:-1]
                    
                    # Find its father (the folder stored at depth - 1)
                    # If for some reason the father is missing, fallback to the root output path
                    parent_path = folder_hierarchy.get(depth - 1, out_path)
                    
                    current_path = parent_path / folder_name
                    self._safe_create_dir(current_path)
                    
                    # Register this new folder as the father for the current depth level
                    folder_hierarchy[depth] = current_path
                    total_created += 1
                    
                else:
                    # IT IS A FILE
                    # Find its father (the folder stored at depth - 1)
                    parent_path = folder_hierarchy.get(depth - 1, out_path)
                    
                    file_target = parent_path / name
                    self._safe_create_file(file_target)
                    total_created += 1

        return BuildResult(True, "Build completed successfully.", total_created)

    def undo_last_build(self) -> BuildResult:
        """Deletes all files and folders created during the last successful build."""
        if not self._history:
            return BuildResult(False, "Nothing to undo. History is empty.")

        removed_count = 0
        
        # Iterate in reverse: deletes files and deepest folders first
        for path in reversed(self._history):
            if path.is_file():
                try:
                    path.unlink()
                    removed_count += 1
                except Exception:
                    pass
            elif path.is_dir():
                try:
                    path.rmdir() # Only deletes if empty
                    removed_count += 1
                except OSError:
                    pass 

        self._history.clear()
        return BuildResult(True, f"Undo complete. Removed {removed_count} items.", removed_count)

    def _safe_create_dir(self, target: Path) -> None:
        """Creates a directory and records it for the undo history."""
        to_create = []
        curr = target
        
        while not curr.exists() and curr.parent != curr:
            to_create.append(curr)
            curr = curr.parent
            
        target.mkdir(parents=True, exist_ok=True)
        self._history.extend(reversed(to_create))

    def _safe_create_file(self, target: Path) -> None:
        """Creates a file and records it for the undo history."""
        if not target.exists():
            self._safe_create_dir(target.parent)
            target.touch()
            self._history.append(target)