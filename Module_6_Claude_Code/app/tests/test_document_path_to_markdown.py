import os
import shutil
import pytest
from tools.document import document_path_to_markdown


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_with_docx(self):
        """Convert a DOCX file by path and verify markdown output."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_with_pdf(self):
        """Convert a PDF file by path and verify markdown output."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "#" in result or "-" in result or "*" in result

    def test_file_not_found(self):
        """Raise FileNotFoundError for a path that does not exist."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/nonexistent/path/file.pdf")

    def test_unsupported_extension(self, tmp_path: pytest.TempPathFactory):
        """Raise an exception for an unrecognised file extension."""
        fake_file = tmp_path / "document.xyz"
        fake_file.write_bytes(b"not a real document")
        with pytest.raises(Exception):
            document_path_to_markdown(str(fake_file))

    def test_extension_inference_is_case_insensitive(self, tmp_path: pytest.TempPathFactory):
        """Handle uppercase file extensions (.PDF, .DOCX) the same as lowercase."""
        upper_pdf = tmp_path / "mcp_docs.PDF"
        shutil.copy(self.PDF_FIXTURE, upper_pdf)
        result = document_path_to_markdown(str(upper_pdf))
        assert isinstance(result, str)
        assert len(result) > 0

        upper_docx = tmp_path / "mcp_docs.DOCX"
        shutil.copy(self.DOCX_FIXTURE, upper_docx)
        result = document_path_to_markdown(str(upper_docx))
        assert isinstance(result, str)
        assert len(result) > 0
