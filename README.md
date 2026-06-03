# TreeGen: MVVM Skeleton Builder

A robust, multi-threaded PyQt6 desktop application designed to parse visual tree-structure text files and automatically generate the corresponding directories and blank files on your local machine. 

Built with a strict **Model-View-ViewModel (MVVM)** architecture, TreeGen ensures complete separation of business logic from the user interface, making the codebase highly maintainable, testable, and scalable.

## ✨ Core Features

- **Advanced Visual Parsing:** Uses intelligent regex to capture visual prefixes (spaces, tabs, and box-drawing characters like `├──` and `└──`). It accurately calculates hierarchy depth regardless of hidden characters (like web non-breaking spaces) or mixed formatting.
- **Strict Parent/Child Tracking:** Instead of fragile stack arrays, the engine maps exact dictionary relationships for every depth level, ensuring files are always created in their exact intended directories.
- **Safe Undo History:** Tracks every individual directory and file created during a build session. The "Undo" function strictly targets these specific paths and only deletes directories if they remain empty, preventing accidental data loss of pre-existing folders.
- **Asynchronous Execution:** Heavy I/O operations are delegated to background `QThread` workers, ensuring the PyQt6 user interface remains completely responsive during large batch generations.

## 📂 Architecture & Project Structure

The codebase is strictly modularized to support future expansion (such as moving parsing logic into dedicated services).

```text
treegen/
│
├── main.py                     # Application entry point and dependency injection
├── requirements.txt            # Project dependencies
│
├── models/
│   ├── __init__.py
│   └── tree_creator.py         # Core parsing, parent-child mapping, and I/O logic
│
├── viewmodels/
│   ├── __init__.py
│   └── main_viewmodel.py       # State broker; handles QThreads and UI signaling
│
├── views/
│   ├── __init__.py
│   └── main_window.py          # Declarative PyQt6 desktop window layout
│
├── utils/                      
│   ├── __init__.py
│   └── logger.py               
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py          # Pytest suite for regex parsing logic
│   └── test_creator.py         # Pytest suite for file generation and undo states
│
└── resources/
    └── icons/                  # Application assets

```

## 🚀 Installation & Usage

### Prerequisites

* Python 3.10 or higher
* Windows OS (Cross-platform compatible with minor path adjustments)

### 1. Environment Setup

Clone the repository and create an isolated virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt

```

### 3. Run the Application

Execute the main entry point to launch the GUI:

```powershell
python main.py

```

## 🧪 Testing

To run the automated test suite, ensure `pytest` is installed, then execute it from the root directory:

```powershell
pytest

```

## 🛠️ Building a Standalone Executable

To compile TreeGen into a single, portable `.exe` file that can run on systems without Python installed, use PyInstaller:

```powershell
pyinstaller --noconsole --onefile --name "TreeGen" main.py

```

The compiled executable will be located in the newly generated `dist/` directory.

---

*Developed as a showcase of clean MVVM architecture, robust regex parsing, and secure file I/O operations in Python.*
