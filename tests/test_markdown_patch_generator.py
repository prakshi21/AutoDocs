from healing.markdown_patch_generator import MarkdownPatchGenerator


def test_generate_patch():

    generator = MarkdownPatchGenerator()

    original = """# API

login(email)
"""

    updated = """# API

login(email, password)
"""

    patch = generator.generate(
        original,
        updated,
        "README.md",
    )

    assert "login(email, password)" in patch

    assert "-login(email)" in patch

    assert "+login(email, password)" in patch


def test_generate_empty_patch_for_identical_content():

    generator = MarkdownPatchGenerator()

    markdown = """# API

login(email)
"""

    patch = generator.generate(
        markdown,
        markdown,
        "README.md",
    )

    assert patch == ""
