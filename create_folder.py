from pathlib import Path
import sys
import subprocess

FILE_TEMPLATES = {
    "__init__.py": "",

    "run.bat": """\
@echo off
call .venv\\Scripts\\activate
python -m app.main
pause
""",

    ".gitignore": """\
# ===== Python =====
__pycache__/
*.pyc

# ===== Virtual Env =====
.venv/
.env

# ===== IDE =====
.vscode/

# ===== OS =====
Thumbs.db
""",

    "requirements.txt": """\
PyQt6
""",

    ".env": """\
PYTHONPATH=.
""",

    "README.md": """\
How to setup running env in PowerShell
1. Open PowerShell as Administrator
2. Set the execution policy to allow script running by executing:
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
3. Change Interpreter to Python
   * In VSCode, press Ctrl + Shift + P
   * Type "Python: Select Interpreter"
   * Choose the appropriate Python environment for your project. (e.g., (.venv))
4. Close terminal (kill terminal not hide) and reopen it to apply changes.
""",

    "settings.json": """\
{
    // ===== Python Settings =====
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
    "python.envFile": "${workspaceFolder}/.env",
    
    "python.analysis.typeCheckingMode": "standard",
    "python.analysis.autoSearchPaths": true,
    "python.analysis.useLibraryCodeForTypes": true,

    // ===== Diagnostic Severity Overrides =====
    "python.analysis.diagnosticSeverityOverrides": {
        "reportMissingImports": "none",
        "reportMissingTypeStubs": "none"
    },

    // ===== Extra Paths =====
    "python.analysis.extraPaths": [
        "${workspaceFolder}",
        "${workspaceFolder}/app"
    ],

    // ===== Exclude Settings =====
    "files.exclude": {
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    },

    "search.exclude": {
        "**/.venv": true,
        "**/__pycache__": true
    },

    // ===== Terminal Settings =====
    "terminal.integrated.defaultProfile.windows": "PowerShell",
    "terminal.integrated.cwd": "${workspaceFolder}"
}
"""
    , "launch.json": """\
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run App (main.py)",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/app/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}",
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
"""
}

STRUCTURE = {
    "app": {
        "controllers": {
            "__files__": ["__init__.py"]
        },
        "models": {
            "__files__": ["__init__.py"]
        },
        "ui": {
            "__files__": ["__init__.py"]
        },
        "utils": {
            "__files__": ["__init__.py"]
        },
        "__files__": ["main.py"]
    },
    "assets": {},
    "scripts": {
        "__files__": ["run.bat"]
    },
    "tests": {},
    "__files__": [".gitignore", "requirements.txt", ".env", "README.md"],
    ".vscode": {
        "__files__": ["settings.json", "launch.json"]
    }
}


def create_structure(base: Path, tree: dict):
    for name, content in tree.items():
        if name == "__files__":
            for file in content:
                file_path = base / file
                if not file_path.exists():
                    text = FILE_TEMPLATES.get(file, "")
                    file_path.write_text(text, encoding="utf-8")
        else:
            folder = base / name
            folder.mkdir(parents=True, exist_ok=True)
            if isinstance(content, dict):
                create_structure(folder, content)

def create_venv(base: Path):
    venv_path = base / "venv"
    if venv_path.exists():
        print("ℹ️ venv already exists")
        return

    print("🐍 Creating virtual environment...")
    subprocess.check_call([
        sys.executable, "-m", "venv", ".venv"
    ])

def install_requirements(base: Path):
    pip_path = base / ".venv" / "Scripts" / "pip.exe"
    req_file = base / "requirements.txt"

    if not req_file.exists():
        print("⚠️ requirements.txt not found")
        return

    print("📦 Installing requirements...")
    subprocess.check_call([
        str(pip_path), "install", "-r", str(req_file)
    ])

def main():
    CURRENT_DIR = Path(__file__).parent

    create_structure(CURRENT_DIR, STRUCTURE)
    create_venv(CURRENT_DIR)
    install_requirements(CURRENT_DIR)

    print(f"✅ Project '{CURRENT_DIR.name}' created successfully!")

    script_path = Path(__file__)
    if script_path.exists():
        script_path.unlink()
        print(f"🗑️ Deleted setup script '{script_path.name}'")

if __name__ == "__main__":
    main()
