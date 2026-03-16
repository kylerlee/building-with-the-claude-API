from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field


def binary_document_to_markdown(
    binary_data: bytes = Field(description="Raw binary content of the document file"),
    file_type: str = Field(description="File extension indicating format, e.g. 'pdf' or 'docx'"),
) -> str:
    """Convert binary document data to markdown-formatted text.

    Reads a document from raw bytes and uses markitdown to extract and convert
    its content to markdown. Supports DOCX and PDF formats via the file_type hint.

    When to use:
    - When you have binary document data and need its text content as markdown
    - When processing uploaded DOCX or PDF files for downstream text analysis

    When NOT to use:
    - When you already have a file path — read the file first and pass its bytes
    - When the document format is not supported by markitdown (e.g. XLS, PPT)

    Examples:
    >>> with open("report.pdf", "rb") as f:
    ...     md = binary_document_to_markdown(f.read(), "pdf")
    >>> with open("notes.docx", "rb") as f:
    ...     md = binary_document_to_markdown(f.read(), "docx")
    """
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to the document file to convert"),
) -> str:
    """Convert a document at a file path to markdown-formatted text.

    Reads the file from disk and delegates to binary_document_to_markdown,
    inferring the format from the file extension (case-insensitive).

    When to use:
    - When you have a file path and need the document's text content as markdown
    - When processing local DOCX or PDF files for text analysis

    When NOT to use:
    - When you already have the binary data — use binary_document_to_markdown directly
    - When the file extension is not supported by markitdown (e.g. .xyz, .xls)

    Examples:
    >>> md = document_path_to_markdown("/reports/annual.pdf")
    >>> md = document_path_to_markdown("/docs/notes.docx")
    """
    SUPPORTED_EXTENSIONS = {"pdf", "docx"}

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    extension = path.suffix.lstrip(".").lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension '.{extension}'. "
            f"Supported extensions: {sorted(SUPPORTED_EXTENSIONS)}"
        )
    with open(path, "rb") as f:
        binary_data = f.read()
    return binary_document_to_markdown(binary_data, extension)
