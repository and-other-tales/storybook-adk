"""Project management for Storybook."""

import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from .models import Project, ManuscriptMetadata


class ProjectManager:
    """Manages manuscript projects."""

    def __init__(self, data_dir: str | Path = "~/.storybook/projects"):
        """Initialize the project manager.

        Args:
            data_dir: Directory to store project data
        """
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def create_project(self, name: str, metadata: ManuscriptMetadata | None = None) -> Project:
        """Create a new project.

        Args:
            name: Project name
            metadata: Optional manuscript metadata

        Returns:
            The created project
        """
        project_id = str(uuid.uuid4())
        project = Project(
            id=project_id,
            name=name,
            metadata=metadata or ManuscriptMetadata(title=name),
        )

        # Create project directory
        project_dir = project.get_project_dir(self.data_dir)
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create empty manuscript file
        manuscript_path = project.get_manuscript_path(self.data_dir)
        manuscript_path.write_text(f"# {name}\n\n")

        # Save project metadata
        self._save_project(project)

        return project

    def import_project(
        self, name: str, manuscript_path: Path, metadata: ManuscriptMetadata | None = None
    ) -> Project:
        """Import a project from an existing manuscript file.

        Args:
            name: Project name
            manuscript_path: Path to the manuscript file
            metadata: Optional manuscript metadata

        Returns:
            The imported project
        """
        # Create the project
        project = self.create_project(name, metadata)
        project_dir = project.get_project_dir(self.data_dir)

        # Copy the manuscript file
        dest_path = project_dir / "manuscript.md"
        shutil.copy(manuscript_path, dest_path)

        # Update word count
        project.update_word_count(self.data_dir)

        # Save project
        self._save_project(project)

        return project

    def list_projects(self) -> list[Project]:
        """List all projects.

        Returns:
            List of all projects
        """
        projects = []
        for project_dir in self.data_dir.iterdir():
            if project_dir.is_dir():
                metadata_file = project_dir / "project.json"
                if metadata_file.exists():
                    try:
                        project = self.load_project(project_dir.name)
                        if project:
                            projects.append(project)
                    except Exception:
                        # Skip invalid projects
                        continue

        # Sort by last edited
        projects.sort(key=lambda p: p.last_edited, reverse=True)
        return projects

    def load_project(self, project_id: str) -> Project | None:
        """Load a project by ID.

        Args:
            project_id: Project ID

        Returns:
            The loaded project, or None if not found
        """
        project_dir = self.data_dir / project_id
        metadata_file = project_dir / "project.json"

        if not metadata_file.exists():
            return None

        try:
            data = json.loads(metadata_file.read_text())
            return Project(**data)
        except Exception:
            return None

    def save_project(self, project: Project) -> None:
        """Save a project.

        Args:
            project: Project to save
        """
        project.last_edited = datetime.now()
        self._save_project(project)

    def _save_project(self, project: Project) -> None:
        """Internal method to save project metadata."""
        project_dir = project.get_project_dir(self.data_dir)
        metadata_file = project_dir / "project.json"
        metadata_file.write_text(project.model_dump_json(indent=2))

    def delete_project(self, project_id: str) -> bool:
        """Delete a project.

        Args:
            project_id: Project ID

        Returns:
            True if deleted, False if not found
        """
        project_dir = self.data_dir / project_id
        if project_dir.exists():
            shutil.rmtree(project_dir)
            return True
        return False

    def get_manuscript_content(self, project: Project) -> str:
        """Get the manuscript content.

        Args:
            project: The project

        Returns:
            Manuscript content
        """
        manuscript_path = project.get_manuscript_path(self.data_dir)
        if manuscript_path.exists():
            return manuscript_path.read_text()
        return ""

    def save_manuscript_content(self, project: Project, content: str) -> None:
        """Save manuscript content.

        Args:
            project: The project
            content: Manuscript content
        """
        manuscript_path = project.get_manuscript_path(self.data_dir)
        manuscript_path.write_text(content)
        project.update_word_count(self.data_dir)
        self.save_project(project)

    def export_project(self, project: Project, export_path: Path, format: str = "md") -> None:
        """Export a project to a file.

        Args:
            project: The project
            export_path: Destination path
            format: Export format (md, docx, pdf)
        """
        manuscript_content = self.get_manuscript_content(project)

        if format == "md":
            export_path.write_text(manuscript_content)
        elif format == "docx":
            # Will be implemented in the document converter
            pass
        elif format == "pdf":
            # Will be implemented in the document converter
            pass
