"""Data models for Storybook."""

from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field


class Character(BaseModel):
    """Represents a character in the manuscript."""

    name: str
    aliases: list[str] = Field(default_factory=list)
    description: str = ""
    traits: list[str] = Field(default_factory=list)
    first_appearance: str = ""  # Chapter/scene reference
    notes: str = ""


class PlotEvent(BaseModel):
    """Represents a plot event or story beat."""

    id: str
    title: str
    description: str
    chapter_reference: str = ""
    timestamp_in_story: str = ""  # e.g., "Day 3", "Chapter 5"
    characters_involved: list[str] = Field(default_factory=list)
    importance: str = "medium"  # low, medium, high, critical
    notes: str = ""


class ManuscriptMetadata(BaseModel):
    """Metadata about the manuscript."""

    title: str = "Untitled Manuscript"
    author: str = ""
    genre: str = "Fiction"
    word_count: int = 0
    chapter_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    last_edited: datetime = Field(default_factory=datetime.now)
    notes: str = ""


class Project(BaseModel):
    """Represents a manuscript project."""

    id: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    last_edited: datetime = Field(default_factory=datetime.now)
    metadata: ManuscriptMetadata = Field(default_factory=ManuscriptMetadata)
    characters: list[Character] = Field(default_factory=list)
    plot_events: list[PlotEvent] = Field(default_factory=list)
    manuscript_file: str = ""  # Path to the main manuscript file

    def get_project_dir(self, base_dir: Path) -> Path:
        """Get the directory for this project."""
        return base_dir / self.id

    def get_manuscript_path(self, base_dir: Path) -> Path:
        """Get the path to the manuscript file."""
        if self.manuscript_file:
            return self.get_project_dir(base_dir) / self.manuscript_file
        return self.get_project_dir(base_dir) / "manuscript.md"

    def update_word_count(self, base_dir: Path) -> None:
        """Update the word count from the manuscript file."""
        manuscript_path = self.get_manuscript_path(base_dir)
        if manuscript_path.exists():
            content = manuscript_path.read_text()
            self.metadata.word_count = len(content.split())
            self.metadata.last_edited = datetime.now()

    def add_character(self, character: Character) -> None:
        """Add a character to the project."""
        # Check if character already exists
        for i, char in enumerate(self.characters):
            if char.name.lower() == character.name.lower():
                self.characters[i] = character
                return
        self.characters.append(character)

    def add_plot_event(self, event: PlotEvent) -> None:
        """Add a plot event to the project."""
        # Check if event already exists
        for i, evt in enumerate(self.plot_events):
            if evt.id == event.id:
                self.plot_events[i] = event
                return
        self.plot_events.append(event)

    def get_character(self, name: str) -> Character | None:
        """Get a character by name."""
        name_lower = name.lower()
        for char in self.characters:
            if char.name.lower() == name_lower or name_lower in [a.lower() for a in char.aliases]:
                return char
        return None


class ReviewSuggestion(BaseModel):
    """Represents an editorial suggestion."""

    type: str  # grammar, style, plot, character, pacing, etc.
    severity: str  # info, minor, major, critical
    location: str  # Chapter/section reference
    issue: str
    suggestion: str
    example: str = ""


class EditorReview(BaseModel):
    """Represents a complete editorial review."""

    timestamp: datetime = Field(default_factory=datetime.now)
    overall_assessment: str = ""
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    suggestions: list[ReviewSuggestion] = Field(default_factory=list)
    character_notes: dict[str, str] = Field(default_factory=dict)
    plot_notes: list[str] = Field(default_factory=list)
