"""Tests for document converter."""

import pytest
from pathlib import Path

from storybook.document_converter import DocumentConverter


class TestDocumentConverter:
    """Tests for DocumentConverter class."""

    def test_detect_format_docx(self):
        """Test format detection for DOCX files."""
        format_type = DocumentConverter.detect_format(Path("test.docx"))
        assert format_type == "docx"

    def test_detect_format_pdf(self):
        """Test format detection for PDF files."""
        format_type = DocumentConverter.detect_format(Path("test.pdf"))
        assert format_type == "pdf"

    def test_detect_format_txt(self):
        """Test format detection for text files."""
        assert DocumentConverter.detect_format(Path("test.txt")) == "txt"
        assert DocumentConverter.detect_format(Path("test.md")) == "txt"
        assert DocumentConverter.detect_format(Path("test.markdown")) == "txt"

    def test_detect_format_unknown(self):
        """Test format detection for unknown files."""
        format_type = DocumentConverter.detect_format(Path("test.xyz"))
        assert format_type == "unknown"

    def test_import_from_text(self, temp_dir):
        """Test importing from text file."""
        # Create a text file
        text_file = temp_dir / "test.txt"
        text_file.write_text("# Chapter 1\n\nTest content here.")

        content = DocumentConverter.import_from_text(text_file)
        assert "Chapter 1" in content
        assert "Test content" in content

    def test_export_to_markdown(self, temp_dir):
        """Test exporting to Markdown."""
        output_file = temp_dir / "output.md"
        content = "# My Novel\n\n## Chapter 1\n\nContent here."

        DocumentConverter.export_to_markdown(content, output_file)

        assert output_file.exists()
        saved_content = output_file.read_text()
        assert saved_content == content

    def test_import_document_text(self, temp_dir):
        """Test import_document with text file."""
        text_file = temp_dir / "test.md"
        text_file.write_text("# Test\n\nContent")

        content = DocumentConverter.import_document(text_file)
        assert "Test" in content

    def test_import_document_unsupported(self, temp_dir):
        """Test import_document with unsupported format."""
        bad_file = temp_dir / "test.xyz"
        bad_file.write_text("Content")

        with pytest.raises(ValueError, match="Unsupported file format"):
            DocumentConverter.import_document(bad_file)

    def test_export_document_markdown(self, temp_dir):
        """Test export_document to Markdown."""
        output_file = temp_dir / "output.md"
        content = "# Novel\n\nChapter 1"

        DocumentConverter.export_document(content, output_file)

        assert output_file.exists()
        assert "Novel" in output_file.read_text()

    def test_export_document_unsupported(self, temp_dir):
        """Test export_document with unsupported format."""
        output_file = temp_dir / "output.xyz"
        content = "Content"

        with pytest.raises(ValueError, match="Unsupported export format"):
            DocumentConverter.export_document(content, output_file)

    @pytest.mark.skipif(
        not hasattr(DocumentConverter, "DOCX_AVAILABLE") or not DocumentConverter.DOCX_AVAILABLE,
        reason="python-docx not installed",
    )
    def test_export_to_docx(self, temp_dir):
        """Test exporting to DOCX format."""
        output_file = temp_dir / "output.docx"
        content = "# My Novel\n\n## Chapter 1\n\nTest content."

        try:
            DocumentConverter.export_to_docx(content, output_file, title="My Novel")
            assert output_file.exists()
        except ImportError:
            pytest.skip("python-docx not available")

    def test_import_export_roundtrip(self, temp_dir):
        """Test import and export roundtrip."""
        original_content = "# Test Novel\n\n## Chapter 1\n\nOnce upon a time."

        # Export to file
        export_file = temp_dir / "test.md"
        DocumentConverter.export_to_markdown(original_content, export_file)

        # Import it back
        imported = DocumentConverter.import_from_text(export_file)

        assert imported == original_content
