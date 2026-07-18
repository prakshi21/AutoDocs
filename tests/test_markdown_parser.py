from parser.markdown_parser import MarkdownParser


def test_markdown_parser_parses_sections():
    parser = MarkdownParser()

    sections = parser.parse("sample_repo/README.md")

    assert len(sections) == 6


def test_heading_levels():
    parser = MarkdownParser()

    sections = parser.parse("sample_repo/README.md")

    installation = next(s for s in sections if s.title == "Installation")
    usage = next(s for s in sections if s.title == "Usage")
    authentication = next(s for s in sections if s.title == "Authentication")

    assert installation.level == 1
    assert usage.level == 2
    assert authentication.level == 3


def test_root_section_exists():
    parser = MarkdownParser()

    sections = parser.parse("sample_repo/README.md")

    assert sections[0].title == "ROOT"


def test_code_blocks_are_preserved():
    parser = MarkdownParser()

    sections = parser.parse("sample_repo/README.md")

    installation = next(s for s in sections if s.title == "Installation")

    assert "```bash" in installation.content
    assert "pip install -r requirements.txt" in installation.content


def test_file_without_headings(tmp_path):
    markdown = tmp_path / "notes.md"

    markdown.write_text(
        "Hello\n\nThis is a markdown file without headings.",
        encoding="utf-8",
    )

    parser = MarkdownParser()

    sections = parser.parse(str(markdown))

    assert len(sections) == 1
    assert sections[0].title == "ROOT"
    assert "Hello" in sections[0].content
