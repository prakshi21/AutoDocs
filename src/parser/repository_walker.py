from pathlib import Path


class RepositoryWalker:
    IGNORE_DIRS = {
        ".git",
        "venv",
        ".venv",
        "__pycache__",
        "node_modules",
        ".vscode",
        ".idea",
        "build",
        "dist",
    }

    def get_python_files(self, root_path: str) -> list[str]:
        python_files: list[str] = []

        root = Path(root_path)

        for file in root.rglob("*.py"):
            if any(part in self.IGNORE_DIRS for part in file.parts):
                continue

            python_files.append(str(file))

        return python_files
