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

            python_files.append(file.as_posix())

        return python_files

    def walk(self, root_path: str) -> list[str]:
        """
        Recursively walk the root_path, returning all files
        that do not belong to ignored directories.
        """
        files: list[str] = []

        root = Path(root_path)

        for file in root.rglob("*"):
            if file.is_file():
                if any(part in self.IGNORE_DIRS for part in file.parts):
                    continue

                files.append(file.as_posix())

        return files
