from analyzer.repository_index import RepositoryIndex
from healing.documentation_mapper import DocumentationMapper
from healing.documentation_rewriter import DocumentationRewriter
from healing.markdown_patch_generator import MarkdownPatchGenerator
from healing.repository_change_detector import RepositoryChangeDetector
from models.document_chunk import DocumentChunk


class AutoDocsEngine:
    """
    Orchestrates the self-healing documentation pipeline.
    """

    def __init__(
        self,
        change_detector: RepositoryChangeDetector,
        documentation_mapper: DocumentationMapper,
        documentation_rewriter: DocumentationRewriter,
        patch_generator: MarkdownPatchGenerator,
    ):
        self._change_detector = change_detector
        self._documentation_mapper = documentation_mapper
        self._documentation_rewriter = documentation_rewriter
        self._patch_generator = patch_generator

    def heal(
        self,
        old_index: RepositoryIndex,
        new_index: RepositoryIndex,
    ) -> list[str]:

        changes = self._change_detector.detect(
            old_index,
            new_index,
        )

        patches = []

        for change in changes:

            documentation_chunks = self._documentation_mapper.map(change)

            #
            # TODO:
            # Retrieve latest code chunks.
            #
            code_chunks: list[DocumentChunk] = []

            updated_documentation = self._documentation_rewriter.rewrite(
                change,
                documentation_chunks,
                code_chunks,
            )

            #
            # Temporary implementation.
            # We'll improve this once we have file grouping.
            #
            original_documentation = "\n\n".join(
                chunk.content for chunk in documentation_chunks
            )

            patch = self._patch_generator.generate(
                original_documentation,
                updated_documentation,
                "documentation.md",
            )

            patches.append(patch)

        return patches
