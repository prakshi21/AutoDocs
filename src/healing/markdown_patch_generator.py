import difflib


class MarkdownPatchGenerator:
    """
    Generates a unified diff between the original
    and rewritten markdown.
    """

    def generate(
        self,
        original: str,
        updated: str,
        file_path: str,
    ) -> str:

        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            updated.splitlines(keepends=True),
            fromfile=f"{file_path} (original)",
            tofile=f"{file_path} (updated)",
        )

        return "".join(diff)
