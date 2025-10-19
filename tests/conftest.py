"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path

import pytest

from storybook.project_manager import ProjectManager
from storybook.models import ManuscriptMetadata, Project, Character, PlotEvent


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def project_manager(temp_dir):
    """Create a project manager with temporary directory."""
    return ProjectManager(temp_dir / "projects")


@pytest.fixture
def sample_metadata():
    """Create sample manuscript metadata."""
    return ManuscriptMetadata(
        title="Test Novel",
        author="Test Author",
        genre="Fiction",
    )


@pytest.fixture
def sample_project(project_manager, sample_metadata):
    """Create a sample project."""
    return project_manager.create_project("test_project", sample_metadata)


@pytest.fixture
def sample_manuscript():
    """Get sample manuscript content."""
    return """# The Lost Key

## Chapter 1

The morning fog clung to the cobblestones. Sarah hurried down the street.

She found a mysterious key covered in strange symbols.

## Chapter 2

Dr. Chen examined the key carefully.

"This is impossible," she whispered.
"""


@pytest.fixture
def sample_character():
    """Create a sample character."""
    return Character(
        name="Sarah",
        aliases=["S", "Sarah J."],
        description="A young archaeologist",
        traits=["curious", "intelligent", "brave"],
        first_appearance="Chapter 1",
    )


@pytest.fixture
def sample_plot_event():
    """Create a sample plot event."""
    return PlotEvent(
        id="event_001",
        title="Discovery of the Key",
        description="Sarah finds a mysterious key",
        chapter_reference="Chapter 1",
        characters_involved=["Sarah"],
        importance="high",
    )
