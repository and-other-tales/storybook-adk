"""Tests for data models."""

import pytest
from datetime import datetime

from storybook.models import (
    Character,
    PlotEvent,
    ManuscriptMetadata,
    Project,
    ReviewSuggestion,
    EditorReview,
)


class TestCharacter:
    """Tests for Character model."""

    def test_create_character(self, sample_character):
        """Test creating a character."""
        assert sample_character.name == "Sarah"
        assert "curious" in sample_character.traits
        assert sample_character.aliases == ["S", "Sarah J."]

    def test_character_defaults(self):
        """Test character default values."""
        char = Character(name="John")
        assert char.aliases == []
        assert char.traits == []
        assert char.description == ""

    def test_character_serialization(self, sample_character):
        """Test character can be serialized to dict."""
        data = sample_character.model_dump()
        assert data["name"] == "Sarah"
        assert len(data["traits"]) == 3


class TestPlotEvent:
    """Tests for PlotEvent model."""

    def test_create_plot_event(self, sample_plot_event):
        """Test creating a plot event."""
        assert sample_plot_event.id == "event_001"
        assert sample_plot_event.title == "Discovery of the Key"
        assert sample_plot_event.importance == "high"

    def test_plot_event_defaults(self):
        """Test plot event default values."""
        event = PlotEvent(id="test", title="Test", description="Test desc")
        assert event.characters_involved == []
        assert event.importance == "medium"
        assert event.chapter_reference == ""

    def test_plot_event_characters(self):
        """Test plot event with multiple characters."""
        event = PlotEvent(
            id="e1",
            title="Meeting",
            description="Characters meet",
            characters_involved=["Sarah", "Dr. Chen", "Old Man"],
        )
        assert len(event.characters_involved) == 3


class TestManuscriptMetadata:
    """Tests for ManuscriptMetadata model."""

    def test_create_metadata(self, sample_metadata):
        """Test creating manuscript metadata."""
        assert sample_metadata.title == "Test Novel"
        assert sample_metadata.author == "Test Author"
        assert sample_metadata.genre == "Fiction"

    def test_metadata_defaults(self):
        """Test metadata default values."""
        meta = ManuscriptMetadata()
        assert meta.title == "Untitled Manuscript"
        assert meta.author == ""
        assert meta.genre == "Fiction"
        assert meta.word_count == 0
        assert isinstance(meta.created_at, datetime)

    def test_metadata_word_count(self):
        """Test word count tracking."""
        meta = ManuscriptMetadata()
        assert meta.word_count == 0
        meta.word_count = 5000
        assert meta.word_count == 5000


class TestProject:
    """Tests for Project model."""

    def test_create_project(self, sample_project):
        """Test creating a project."""
        assert sample_project.name == "test_project"
        assert sample_project.metadata.title == "Test Novel"
        assert len(sample_project.characters) == 0
        assert len(sample_project.plot_events) == 0

    def test_add_character(self, sample_project, sample_character):
        """Test adding a character to project."""
        sample_project.add_character(sample_character)
        assert len(sample_project.characters) == 1
        assert sample_project.characters[0].name == "Sarah"

    def test_add_duplicate_character(self, sample_project):
        """Test adding duplicate character updates existing."""
        char1 = Character(name="Sarah", description="First version")
        char2 = Character(name="Sarah", description="Updated version")

        sample_project.add_character(char1)
        assert len(sample_project.characters) == 1
        assert sample_project.characters[0].description == "First version"

        sample_project.add_character(char2)
        assert len(sample_project.characters) == 1
        assert sample_project.characters[0].description == "Updated version"

    def test_get_character(self, sample_project, sample_character):
        """Test retrieving a character."""
        sample_project.add_character(sample_character)

        # Get by exact name
        char = sample_project.get_character("Sarah")
        assert char is not None
        assert char.name == "Sarah"

        # Get by alias
        char = sample_project.get_character("S")
        assert char is not None
        assert char.name == "Sarah"

        # Get non-existent
        char = sample_project.get_character("Unknown")
        assert char is None

    def test_add_plot_event(self, sample_project, sample_plot_event):
        """Test adding a plot event."""
        sample_project.add_plot_event(sample_plot_event)
        assert len(sample_project.plot_events) == 1
        assert sample_project.plot_events[0].id == "event_001"

    def test_add_duplicate_plot_event(self, sample_project):
        """Test adding duplicate plot event updates existing."""
        event1 = PlotEvent(id="e1", title="First", description="First version")
        event2 = PlotEvent(id="e1", title="Updated", description="Updated version")

        sample_project.add_plot_event(event1)
        assert len(sample_project.plot_events) == 1

        sample_project.add_plot_event(event2)
        assert len(sample_project.plot_events) == 1
        assert sample_project.plot_events[0].title == "Updated"


class TestReviewSuggestion:
    """Tests for ReviewSuggestion model."""

    def test_create_suggestion(self):
        """Test creating a review suggestion."""
        suggestion = ReviewSuggestion(
            type="grammar",
            severity="minor",
            location="Chapter 1, Page 3",
            issue="Incorrect verb tense",
            suggestion="Use past tense",
        )
        assert suggestion.type == "grammar"
        assert suggestion.severity == "minor"

    def test_suggestion_with_example(self):
        """Test suggestion with example."""
        suggestion = ReviewSuggestion(
            type="style",
            severity="info",
            location="Chapter 2",
            issue="Repetitive word usage",
            suggestion="Vary vocabulary",
            example="Use 'walked' instead of 'went' repeatedly",
        )
        assert suggestion.example != ""


class TestEditorReview:
    """Tests for EditorReview model."""

    def test_create_review(self):
        """Test creating an editor review."""
        review = EditorReview(
            overall_assessment="Good manuscript with minor issues",
            strengths=["Strong characters", "Engaging plot"],
            weaknesses=["Some pacing issues"],
        )
        assert len(review.strengths) == 2
        assert len(review.weaknesses) == 1
        assert isinstance(review.timestamp, datetime)

    def test_review_with_suggestions(self):
        """Test review with suggestions."""
        suggestion = ReviewSuggestion(
            type="plot",
            severity="major",
            location="Chapter 3",
            issue="Plot hole",
            suggestion="Explain character motivation",
        )
        review = EditorReview(suggestions=[suggestion])
        assert len(review.suggestions) == 1
        assert review.suggestions[0].type == "plot"
