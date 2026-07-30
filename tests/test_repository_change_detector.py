from healing.repository_change_detector import RepositoryChangeDetector
from models.code_symbol import CodeSymbol
from analyzer.repository_index import RepositoryIndex
from models.enums import SymbolType
from healing.change_type import ChangeType


def create_symbol(
    name: str,
    file_path: str,
    signature: str = "",
):
    """
    Helper function for creating test symbols.
    """

    return CodeSymbol(
        id=f"{file_path}::{name}",
        name=name,
        symbol_type=SymbolType.FUNCTION,
        signature=signature,
        docstring="",
        file_path=file_path,
        start_line=1,
        end_line=10,
    )


def create_repository_index(symbols: list[CodeSymbol] | None = None) -> RepositoryIndex:
    repository = RepositoryIndex()
    if symbols:
        for symbol in symbols:
            repository.add_symbol(symbol)
    return repository


def test_build_lookup_contains_all_symbols():
    detector = RepositoryChangeDetector()

    symbols = [
        create_symbol("login", "auth.py"),
        create_symbol("logout", "auth.py"),
        create_symbol("User", "user.py"),
    ]

    repository = create_repository_index(symbols)

    lookup = detector._build_lookup(repository)

    assert len(lookup) == 3


def test_build_lookup_creates_expected_keys():
    detector = RepositoryChangeDetector()

    repository = create_repository_index(
        [
            create_symbol("login", "auth.py"),
            create_symbol("logout", "auth.py"),
        ]
    )

    lookup = detector._build_lookup(repository)

    assert "auth.py::login" in lookup
    assert "auth.py::logout" in lookup


def test_build_lookup_values_are_symbols():
    detector = RepositoryChangeDetector()

    login = create_symbol("login", "auth.py")

    repository = create_repository_index([login])

    lookup = detector._build_lookup(repository)

    assert lookup["auth.py::login"] is login


def test_build_lookup_returns_empty_dictionary_for_empty_repository():
    detector = RepositoryChangeDetector()

    repository = create_repository_index()

    lookup = detector._build_lookup(repository)

    assert lookup == {}


def create_repository(symbols):
    return create_repository_index(symbols)


def test_detect_added_symbol():
    detector = RepositoryChangeDetector()

    old_repo = create_repository([])

    new_repo = create_repository(
        [
            create_symbol(
                name="login",
                file_path="auth.py",
                signature="login(email)",
            )
        ]
    )

    changes = detector.detect(old_repo, new_repo)

    assert len(changes) == 1

    change = changes[0]

    assert change.change_type == ChangeType.ADDED
    assert change.symbol_name == "login"


def test_detect_removed_symbol():
    detector = RepositoryChangeDetector()

    old_repo = create_repository(
        [
            create_symbol(
                name="login",
                file_path="auth.py",
                signature="login(email)",
            )
        ]
    )

    new_repo = create_repository([])

    changes = detector.detect(old_repo, new_repo)

    assert len(changes) == 1

    change = changes[0]

    assert change.change_type == ChangeType.REMOVED
    assert change.symbol_name == "login"


def test_detect_signature_change():
    detector = RepositoryChangeDetector()

    old_repo = create_repository(
        [
            create_symbol(
                name="login",
                file_path="auth.py",
                signature="login(email)",
            )
        ]
    )

    new_repo = create_repository(
        [
            create_symbol(
                name="login",
                file_path="auth.py",
                signature="login(email, password)",
            )
        ]
    )

    changes = detector.detect(old_repo, new_repo)

    assert len(changes) == 1

    change = changes[0]

    assert change.change_type == ChangeType.SIGNATURE_CHANGED

    assert change.old_signature == "login(email)"

    assert change.new_signature == "login(email, password)"


def test_detect_docstring_change():
    detector = RepositoryChangeDetector()

    old_symbol = create_symbol(
        "login",
        "auth.py",
        "login(email)",
    )
    old_symbol.docstring = "Old documentation"

    new_symbol = create_symbol(
        "login",
        "auth.py",
        "login(email)",
    )
    new_symbol.docstring = "New documentation"

    old_repo = create_repository([old_symbol])
    new_repo = create_repository([new_symbol])

    changes = detector.detect(old_repo, new_repo)

    assert len(changes) == 1

    assert changes[0].change_type == ChangeType.DOCSTRING_CHANGED


def test_detect_no_changes():
    detector = RepositoryChangeDetector()

    symbol = create_symbol(
        "login",
        "auth.py",
        "login(email)",
    )

    old_repo = create_repository([symbol])

    new_repo = create_repository(
        [
            create_symbol(
                "login",
                "auth.py",
                "login(email)",
            )
        ]
    )

    changes = detector.detect(old_repo, new_repo)

    assert changes == []
