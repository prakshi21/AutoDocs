from parser.python_parser import PythonParser

parser = PythonParser()

symbols = parser.parse("sample_repo/auth.py")

for symbol in symbols:
    print(symbol)
