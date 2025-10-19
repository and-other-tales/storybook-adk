"""Tests for project manager."""

import pytest
from pathlib import Path

from storybook.project_manager import ProjectManager
from storybook.models import ManuscriptMetadata


class TestProjectManager:
    """Tests for ProjectManager class."""

    def test_init_creates_directory(self, temp_dir):
        """Test that initialization creates data directory."""
        pm = ProjectManager(temp_dir / "projects")
        assert (temp_dir / "projects").exists()

    def test_create_project(self, project_manager, sample_metadata):
        """Test creating a new project."""
        project = project_manager.create_project("my_novel", sample_metadata)

        assert project.name == "my_novel"
        assert project.metadata.title == "Test Novel"
        assert project.id != ""

        # Check project directory exists
        project_dir = project.get_project_dir(project_manager.data_dir)
        assert project_dir.exists()

        # Check manuscript file exists
        manuscript_path = project.get_manuscript_path(project_manager.data_dir)
        assert manuscript_path.exists()

    def test_create_project_with_defaults(self, project_manager):
        """Test creating project without metadata."""
        project = project_manager.create_project("simple_project")

        assert project.name == "simple_project"
        assert project.metadata.title == "simple_project"

    def test_save_and_load_project(self, project_manager, sample_project):
        """Test saving and loading a project."""
        project_manager.save_project(sample_project)

        loaded = project_manager.load_project(sample_project.id)
        assert loaded is not None
        assert loaded.name == sample_project.name
        assert loaded.id == sample_project.id

    def test_load_nonexistent_project(self, project_manager):
        """Test loading a project that doesn't exist."""
        project = project_manager.load_project("nonexistent")
        assert project is None

    def test_list_projects(self, project_manager):
        """Test listing all projects."""
        # Create several projects
        project_manager.create_project("project1")
        project_manager.create_project("project2")
        project_manager.create_project("project3")

        projects = project_manager.list_projects()
        assert len(projects) == 3
        assert all(p.name in ["project1", "project2", "project3"] for p in projects)

    def test_list_projects_empty(self, project_manager):
        """Test listing projects when none exist."""
        projects = project_manager.list_projects()
        assert projects == []

    def test_delete_project(self, project_manager, sample_project):
        """Test deleting a project."""
        project_id = sample_project.id
        project_dir = sample_project.get_project_dir(project_manager.data_dir)

        assert project_dir.exists()

        success = project_manager.delete_project(project_id)
        assert success is True
        assert not project_dir.exists()

    def test_delete_nonexistent_project(self, project_manager):
        """Test deleting a project that doesn't exist."""
        success = project_manager.delete_project("nonexistent")
        assert success is False

    def test_get_manuscript_content(self, project_manager, sample_project, sample_manuscript):
        """Test getting manuscript content."""
        # Save some content
        project_manager.save_manuscript_content(sample_project, sample_manuscript)

        # Get it back
        content = project_manager.get_manuscript_content(sample_project)
        assert "The Lost Key" in content
        assert "Chapter 1" in content

    def test_save_manuscript_content_updates_word_count(
        self, project_manager, sample_project, sample_manuscript
    ):
        """Test that saving content updates word count."""
        initial_count = sample_project.metadata.word_count

        project_manager.save_manuscript_content(sample_project, sample_manuscript)

        # Reload project
        project = project_manager.load_project(sample_project.id)
        assert project.metadata.word_count > initial_count
        assert project.metadata.word_count > 0

    def test_import_project(self, project_manager, temp_dir):
        """Test importing a project from file."""
        # Create a sample file
        manuscript_file = temp_dir / "test_manuscript.md"
        manuscript_file.write_text("# My Novel\n\nChapter 1 content here.")

        project = project_manager.import_project("imported_novel", manuscript_file)

        assert project.name == "imported_novel"
        assert project.metadata.word_count > 0

        # Check content was copied
        content = project_manager.get_manuscript_content(project)
        assert "My Novel" in content
        assert "Chapter 1" in content

    def test_project_persistence(self, project_manager, sample_character, sample_plot_event):
        """Test that project changes persist."""
        # Create project
        project = project_manager.create_project("test_persistence")

        # Add character and plot event
        project.add_character(sample_character)
        project.add_plot_event(sample_plot_event)
        project_manager.save_project(project)

        # Reload
        loaded = project_manager.load_project(project.id)
        assert len(loaded.characters) == 1
        assert len(loaded.plot_events) == 1
        assert loaded.characters[0].name == "Sarah"
        assert loaded.plot_events[0].id == "event_001"
