"""Tests for UI components."""

import pytest
from io import StringIO

from storybook.ui import StorybookUI
from storybook.models import Project, ManuscriptMetadata, Character, PlotEvent


class TestStorybookUI:
    """Tests for StorybookUI class."""

    def test_init(self):
        """Test UI initialization."""
        ui = StorybookUI()
        assert ui.console is not None

    def test_show_banner(self, capsys):
        """Test showing banner."""
        ui = StorybookUI()
        ui.show_banner()
        # Just verify it doesn't crash
        # Actual output verification is complex due to Rich formatting

    def test_show_message(self, capsys):
        """Test showing message."""
        ui = StorybookUI()
        ui.show_message("Test message", "white")
        # Verify it doesn't crash

    def test_show_error(self):
        """Test showing error message."""
        ui = StorybookUI()
        ui.show_error("Test error")
        # Verify it doesn't crash

    def test_show_success(self):
        """Test showing success message."""
        ui = StorybookUI()
        ui.show_success("Test success")
        # Verify it doesn't crash

    def test_show_markdown(self):
        """Test showing markdown content."""
        ui = StorybookUI()
        ui.show_markdown("# Test\n\nMarkdown content")
        # Verify it doesn't crash

    def test_show_panel(self):
        """Test showing panel."""
        ui = StorybookUI()
        ui.show_panel("Content", title="Title", style="cyan")
        # Verify it doesn't crash

    def test_list_projects_empty(self):
        """Test listing empty projects."""
        ui = StorybookUI()
        ui.list_projects([])
        # Verify it doesn't crash

    def test_list_projects(self, sample_project):
        """Test listing projects."""
        ui = StorybookUI()
        projects = [sample_project]
        ui.list_projects(projects)
        # Verify it doesn't crash

    def test_show_characters_empty(self, sample_project):
        """Test showing characters when none exist."""
        ui = StorybookUI()
        ui.show_characters(sample_project)
        # Verify it doesn't crash

    def test_show_characters(self, sample_project, sample_character):
        """Test showing characters."""
        ui = StorybookUI()
        sample_project.add_character(sample_character)
        ui.show_characters(sample_project)
        # Verify it doesn't crash

    def test_show_plot_events_empty(self, sample_project):
        """Test showing plot events when none exist."""
        ui = StorybookUI()
        ui.show_plot_events(sample_project)
        # Verify it doesn't crash

    def test_show_plot_events(self, sample_project, sample_plot_event):
        """Test showing plot events."""
        ui = StorybookUI()
        sample_project.add_plot_event(sample_plot_event)
        ui.show_plot_events(sample_project)
        # Verify it doesn't crash

    def test_spinner_context(self):
        """Test spinner context manager."""
        ui = StorybookUI()
        spinner = ui.spinner("Processing...")
        assert spinner is not None
        # Verify it can be created

    def test_print_separator(self):
        """Test printing separator."""
        ui = StorybookUI()
        ui.print_separator()
        # Verify it doesn't crash
