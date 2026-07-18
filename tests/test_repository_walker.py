# pyrefly: ignore [missing-import]
from parser.repository_walker import RepositoryWalker


def test_get_python_files():
    walker = RepositoryWalker()

    files = walker.get_python_files("sample_repo")

    assert len(files) > 0
