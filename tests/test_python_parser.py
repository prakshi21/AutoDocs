from parser.python_parser import PythonParser


def test_python_parser_parses_symbols():
    parser = PythonParser()

    symbols = parser.parse("sample_repo/auth.py")

    assert len(symbols) == 4


def test_detects_function_class_and_methods():
    parser = PythonParser()

    symbols = parser.parse("sample_repo/auth.py")

    types = [symbol.symbol_type.value for symbol in symbols]

    assert "function" in types
    assert "class" in types
    assert types.count("method") == 2


def test_function_signature():
    parser = PythonParser()

    symbols = parser.parse("sample_repo/auth.py")

    add = next(symbol for symbol in symbols if symbol.name == "add")

    assert add.signature == "add(a, b)"


def test_class_docstring():
    parser = PythonParser()

    symbols = parser.parse("sample_repo/auth.py")

    user = next(symbol for symbol in symbols if symbol.name == "User")

    assert user.docstring == "User class"


def test_method_docstring():
    parser = PythonParser()

    symbols = parser.parse("sample_repo/auth.py")

    login = next(symbol for symbol in symbols if symbol.name == "User.login")

    assert login.docstring == "Login user"
