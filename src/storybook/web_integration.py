"""Web integration module for Storybook CLI.

This module provides functions that can be called from the Node.js backend
to interact with the Storybook CLI functionality.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from .project_manager import ProjectManager
from .models import Project, ManuscriptMetadata, Character, PlotEvent
from .document_converter import DocumentConverter


# Global project manager instance
pm = ProjectManager()


def list_projects() -> List[Dict[str, Any]]:
    """List all projects as JSON-serializable dicts."""
    projects = pm.list_projects()
    return [project.model_dump() for project in projects]


def load_project(project_id: str) -> Dict[str, Any]:
    """Load a project by ID."""
    project = pm.load_project(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")
    return project.model_dump()


def create_project(name: str, import_file: Optional[str] = None) -> Dict[str, Any]:
    """Create a new project.

    Args:
        name: Project name
        import_file: Optional path to file to import

    Returns:
        Project data as dict
    """
    if import_file:
        project = pm.import_project(name, Path(import_file))
    else:
        project = pm.create_project(name)
    return project.model_dump()


def delete_project(project_id: str) -> None:
    """Delete a project."""
    pm.delete_project(project_id)


def update_metadata(project_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Update project metadata.

    Args:
        project_id: Project ID
        metadata: Metadata fields to update

    Returns:
        Updated project data
    """
    project = pm.load_project(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")

    # Update metadata fields
    for key, value in metadata.items():
        if hasattr(project.metadata, key):
            setattr(project.metadata, key, value)

    pm._save_project(project)
    return project.model_dump()


def read_manuscript(project_id: str) -> str:
    """Read manuscript content.

    Args:
        project_id: Project ID

    Returns:
        Manuscript content as string
    """
    project = pm.load_project(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")

    manuscript_path = project.get_manuscript_path(pm.data_dir)
    if not manuscript_path.exists():
        return ""

    return manuscript_path.read_text()


def write_manuscript(project_id: str, content: str) -> None:
    """Write manuscript content.

    Args:
        project_id: Project ID
        content: New manuscript content
    """
    project = pm.load_project(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")

    manuscript_path = project.get_manuscript_path(pm.data_dir)
    manuscript_path.write_text(content)

    # Update word count
    project.update_word_count(pm.data_dir)
    pm._save_project(project)


def export_project(project_id: str, format: str) -> str:
    """Export project to specified format.

    Args:
        project_id: Project ID
        format: Export format (docx, pdf, markdown)

    Returns:
        Path to exported file
    """
    project = pm.load_project(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")

    manuscript_path = project.get_manuscript_path(pm.data_dir)
    project_dir = project.get_project_dir(pm.data_dir)

    converter = DocumentConverter()

    if format == "docx":
        output_path = project_dir / f"{project.name}.docx"
        converter.markdown_to_docx(manuscript_path, output_path)
        return str(output_path)

    elif format == "markdown":
        return str(manuscript_path)

    elif format == "pdf":
        # PDF export would require additional dependencies
        raise NotImplementedError("PDF export not yet implemented")

    else:
        raise ValueError(f"Unsupported format: {format}")


def import_document(project_id: str, file_path: str) -> None:
    """Import a document into an existing project.

    Args:
        project_id: Project ID
        file_path: Path to file to import
    """
    project = pm.load_project(project_id)
    if not project:
        raise ValueError(f"Project {project_id} not found")

    converter = DocumentConverter()
    project_dir = project.get_project_dir(pm.data_dir)
    manuscript_path = project_dir / "manuscript.md"

    input_path = Path(file_path)

    if input_path.suffix.lower() == '.docx':
        converter.docx_to_markdown(input_path, manuscript_path)
    elif input_path.suffix.lower() == '.pdf':
        converter.pdf_to_markdown(input_path, manuscript_path)
    elif input_path.suffix.lower() in ['.txt', '.md']:
        manuscript_path.write_text(input_path.read_text())
    else:
        raise ValueError(f"Unsupported file format: {input_path.suffix}")

    # Update word count
    project.update_word_count(pm.data_dir)
    pm._save_project(project)


# Expose functions for the python_runner
__all__ = [
    'list_projects',
    'load_project',
    'create_project',
    'delete_project',
    'update_metadata',
    'read_manuscript',
    'write_manuscript',
    'export_project',
    'import_document',
]
