"""Quick start example for Storybook.

This example demonstrates how to use the Storybook API programmatically.
"""

import asyncio
from pathlib import Path

from storybook.project_manager import ProjectManager
from storybook.models import ManuscriptMetadata
from storybook.document_converter import DocumentConverter
from storybook.editor import LiteraryEditor
from storybook.chat import ManuscriptChatSession


async def create_and_edit_project():
    """Example: Create a project and perform edits."""

    # Initialize the project manager
    pm = ProjectManager("./my_manuscripts")

    # Create a new project
    metadata = ManuscriptMetadata(
        title="The Lost Key",
        genre="Mystery",
        author="John Doe",
    )

    project = pm.create_project(name="mystery_novel", metadata=metadata)
    print(f"Created project: {project.name} (ID: {project.id[:8]})")

    # Add some initial content
    initial_content = """# The Lost Key

## Chapter 1: The Discovery

The morning fog clung to the cobblestones like a desperate memory.
Sarah hurried down the street, already late for her archaeology seminar.

As she rounded the corner, something caught her eye—a glint of gold in the gutter.
The object was an ancient key, covered in mysterious symbols.
"""

    pm.save_manuscript_content(project, initial_content)
    print(f"Initial word count: {project.metadata.word_count}")

    # Start a chat session
    session = ManuscriptChatSession(project, pm)
    await session.start()

    # Ask for feedback
    print("\n--- Asking for feedback ---")
    async for event in session.send_message(
        "Please read the opening and suggest improvements to make it more engaging."
    ):
        if event["type"] == "text":
            print(f"\nEditor: {event['content']}")
        elif event["type"] == "tool_use":
            print(f"[Using tool: {event['tool']}]")

    await session.close()


async def import_and_review():
    """Example: Import a manuscript and run automated review."""

    pm = ProjectManager("./my_manuscripts")

    # Import from a file
    manuscript_file = Path("examples/sample_chapter.md")

    if manuscript_file.exists():
        metadata = ManuscriptMetadata(
            title="The Lost Key",
            genre="Mystery",
        )

        project = pm.import_project(
            name="imported_mystery", manuscript_path=manuscript_file, metadata=metadata
        )

        print(f"Imported project: {project.name}")
        print(f"Word count: {project.metadata.word_count:,}")

        # Run automated review
        editor = LiteraryEditor(pm)

        print("\n--- Running automated review ---")
        async for event in editor.review_manuscript(project, focus_areas=["plot", "characters"]):
            if event["type"] == "text":
                print(f"\n{event['content']}")
            elif event["type"] == "complete":
                print(f"\nReview complete! Cost: ${event['cost']:.4f}")


async def batch_processing():
    """Example: Process multiple manuscripts in batch."""

    pm = ProjectManager("./my_manuscripts")
    editor = LiteraryEditor(pm)

    # List all projects
    projects = pm.list_projects()

    for project in projects:
        print(f"\nProcessing: {project.name}")

        # Quick prose analysis
        async for event in editor.quick_feedback(
            project, "Analyze the opening paragraph for prose quality and pacing."
        ):
            if event["type"] == "text":
                print(event["content"])
                break  # Just get the first response


async def export_example():
    """Example: Export manuscripts to different formats."""

    pm = ProjectManager("./my_manuscripts")
    converter = DocumentConverter()

    projects = pm.list_projects()

    if projects:
        project = projects[0]  # Get the first project
        content = pm.get_manuscript_content(project)

        # Export to DOCX
        output_docx = Path(f"{project.name}.docx")
        try:
            converter.export_to_docx(content, output_docx, title=project.metadata.title)
            print(f"Exported to: {output_docx}")
        except ImportError:
            print("python-docx not installed, skipping DOCX export")

        # Export to Markdown
        output_md = Path(f"{project.name}.md")
        converter.export_to_markdown(content, output_md)
        print(f"Exported to: {output_md}")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("Storybook Quick Start Examples")
    print("=" * 60)

    # Example 1: Create and edit
    print("\n[Example 1: Create and Edit Project]")
    # await create_and_edit_project()

    # Example 2: Import and review
    print("\n[Example 2: Import and Review]")
    await import_and_review()

    # Example 3: Batch processing
    # print("\n[Example 3: Batch Processing]")
    # await batch_processing()

    # Example 4: Export
    # print("\n[Example 4: Export Manuscripts]")
    # await export_example()


if __name__ == "__main__":
    asyncio.run(main())
