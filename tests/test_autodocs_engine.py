from unittest.mock import MagicMock

from healing.autodocs_engine import AutoDocsEngine


def test_heal_runs_pipeline():

    detector = MagicMock()
    mapper = MagicMock()
    rewriter = MagicMock()
    patch_generator = MagicMock()

    detector.detect.return_value = ["change"]
    mapper.map.return_value = []
    rewriter.rewrite.return_value = "updated markdown"
    patch_generator.generate.return_value = "patch"

    engine = AutoDocsEngine(
        detector,
        mapper,
        rewriter,
        patch_generator,
    )

    patches = engine.heal(
        old_index=MagicMock(),
        new_index=MagicMock(),
    )

    detector.detect.assert_called_once()
    mapper.map.assert_called_once()
    rewriter.rewrite.assert_called_once()
    patch_generator.generate.assert_called_once()

    assert patches == ["patch"]
