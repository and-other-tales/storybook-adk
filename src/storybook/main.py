"""Main application entry point for Storybook."""

import asyncio
import sys
from pathlib import Path

from .ui import StorybookUI
from .project_manager import ProjectManager
from .document_converter import DocumentConverter
from .editor import LiteraryEditor
from .chat import ManuscriptChatSession
from .models import ManuscriptMetadata


class StorybookApp:
    """Main Storybook application."""

    def __init__(self):
        """Initialize the application."""
        self.ui = StorybookUI()
        self.project_manager = ProjectManager()
        self.editor = LiteraryEditor(self.project_manager)
        self.converter = DocumentConverter()
        self.current_project = None

    async def run(self) -> None:
        """Run the main application loop."""
        self.ui.show_banner()

        while True:
            try:
                choice = self.ui.show_main_menu()

                if choice == "1":
                    await self.create_project()
                elif choice == "2":
                    await self.open_project()
                elif choice == "3":
                    await self.import_project()
                elif choice == "4":
                    await self.delete_project()
                elif choice == "5":
                    self.ui.show_message("Goodbye!", "cyan")
                    break

            except KeyboardInterrupt:
                self.ui.show_message("\nOperation cancelled.", "yellow")
            except Exception as e:
                self.ui.show_error(f"An error occurred: {str(e)}")

    async def create_project(self) -> None:
        """Create a new project."""
        self.ui.show_message("\n[bold cyan]Create New Project[/bold cyan]", "white")
        self.ui.print_separator()

        name = self.ui.prompt_project_name()
        title = self.ui.prompt_manuscript_title(default=name)
        genre = self.ui.prompt_genre()

        metadata = ManuscriptMetadata(title=title, genre=genre)
        project = self.project_manager.create_project(name, metadata)

        self.ui.show_success(f"Project '{name}' created successfully!")

        if self.ui.confirm("Would you like to open this project now?"):
            self.current_project = project
            await self.project_menu()

    async def open_project(self) -> None:
        """Open an existing project."""
        projects = self.project_manager.list_projects()

        if not projects:
            self.ui.show_message("No projects found. Create a new project first.", "yellow")
            return

        self.ui.list_projects(projects)
        self.ui.print_separator()

        project_id = self.ui.prompt_file_path("Enter project ID (first 8 characters)")

        # Find project by partial ID
        project = None
        for p in projects:
            if p.id.startswith(project_id):
                project = p
                break

        if not project:
            self.ui.show_error("Project not found.")
            return

        self.current_project = project
        await self.project_menu()

    async def import_project(self) -> None:
        """Import a project from a file."""
        self.ui.show_message("\n[bold cyan]Import Project[/bold cyan]", "white")
        self.ui.print_separator()

        file_path = Path(self.ui.prompt_file_path("Path to manuscript file"))

        if not file_path.exists():
            self.ui.show_error("File not found.")
            return

        name = self.ui.prompt_project_name()
        title = self.ui.prompt_manuscript_title(default=name)
        genre = self.ui.prompt_genre()

        try:
            with self.ui.spinner("Importing manuscript...") as progress:
                progress.add_task("Importing...", total=None)

                # Convert document to markdown
                content = self.converter.import_document(file_path)

                # Create project with temporary file
                metadata = ManuscriptMetadata(title=title, genre=genre)
                project = self.project_manager.create_project(name, metadata)

                # Save the imported content
                self.project_manager.save_manuscript_content(project, content)

            self.ui.show_success(f"Project '{name}' imported successfully!")
            self.ui.show_message(f"Word count: {project.metadata.word_count:,}", "cyan")

            if self.ui.confirm("Would you like to open this project now?"):
                self.current_project = project
                await self.project_menu()

        except Exception as e:
            self.ui.show_error(f"Import failed: {str(e)}")

    async def delete_project(self) -> None:
        """Delete a project."""
        projects = self.project_manager.list_projects()

        if not projects:
            self.ui.show_message("No projects found.", "yellow")
            return

        self.ui.list_projects(projects)
        self.ui.print_separator()

        project_id = self.ui.prompt_file_path("Enter project ID to delete")

        # Find project by partial ID
        project = None
        for p in projects:
            if p.id.startswith(project_id):
                project = p
                break

        if not project:
            self.ui.show_error("Project not found.")
            return

        if self.ui.confirm(
            f"Are you sure you want to delete '{project.name}'? This cannot be undone."
        ):
            if self.project_manager.delete_project(project.id):
                self.ui.show_success("Project deleted successfully.")
            else:
                self.ui.show_error("Failed to delete project.")

    async def project_menu(self) -> None:
        """Show the project menu."""
        if not self.current_project:
            return

        while True:
            # Reload project to get latest data
            self.current_project = self.project_manager.load_project(self.current_project.id)
            if not self.current_project:
                self.ui.show_error("Project not found.")
                break

            try:
                choice = self.ui.show_project_menu(self.current_project)

                if choice == "1":
                    await self.chat_session()
                elif choice == "2":
                    await self.run_automated_review()
                elif choice == "3":
                    self.view_characters()
                elif choice == "4":
                    self.view_plot_events()
                elif choice == "5":
                    await self.export_manuscript()
                elif choice == "6":
                    await self.project_settings()
                elif choice == "7":
                    self.current_project = None
                    break

            except KeyboardInterrupt:
                self.ui.show_message("\nReturning to project menu...", "yellow")

    async def chat_session(self) -> None:
        """Start an interactive chat session."""
        self.ui.show_message("\n[bold cyan]Chat with Editor[/bold cyan]", "white")
        self.ui.print_separator()
        self.ui.show_message("Type your message and press Enter. Type 'quit' to exit.", "dim")
        self.ui.print_separator()

        session = ManuscriptChatSession(self.current_project, self.project_manager)

        try:
            await session.start()
            self.ui.show_success("Chat session started!")

            while True:
                # Get user input
                self.ui.console.print("\n[bold cyan]You:[/bold cyan] ", end="")
                try:
                    user_input = input().strip()
                except EOFError:
                    break

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "q"]:
                    break

                # Send message and display responses
                self.ui.console.print("\n[bold green]Editor:[/bold green]")

                async for event in session.send_message(user_input):
                    if event["type"] == "text":
                        self.ui.show_markdown(event["content"])
                    elif event["type"] == "thinking":
                        self.ui.show_message(f"[Thinking: {event['content'][:100]}...]", "dim")
                    elif event["type"] == "tool_use":
                        tool_name = event["tool"].replace("mcp__storybook__", "")
                        self.ui.show_message(f"Using tool: {tool_name}", "yellow")
                    elif event["type"] == "complete":
                        if event.get("cost"):
                            self.ui.show_message(f"\n[Cost: ${event['cost']:.4f}]", "dim")

        except Exception as e:
            self.ui.show_error(f"Chat error: {str(e)}")
        finally:
            await session.close()
            self.ui.show_message("\nChat session ended.", "cyan")

    async def run_automated_review(self) -> None:
        """Run an automated review of the manuscript."""
        self.ui.show_message("\n[bold cyan]Automated Literary Review[/bold cyan]", "white")
        self.ui.print_separator()

        focus_areas = []
        if self.ui.confirm("Focus on specific areas?"):
            self.ui.show_message("Select areas to focus on (press Enter to skip):", "cyan")
            areas = ["plot", "characters", "prose", "pacing", "dialogue"]
            for area in areas:
                if self.ui.confirm(f"  - {area.title()}?"):
                    focus_areas.append(area)

        self.ui.show_message("\nStarting review... This may take a few minutes.", "yellow")
        self.ui.print_separator()

        try:
            review_text = []

            async for event in self.editor.review_manuscript(self.current_project, focus_areas):
                if event["type"] == "text":
                    content = event["content"]
                    review_text.append(content)
                    self.ui.show_markdown(content)
                    self.ui.print_separator()
                elif event["type"] == "tool_use":
                    tool_name = event["tool"].replace("mcp__storybook__", "")
                    self.ui.show_message(f"Analyzing: {tool_name}", "dim")
                elif event["type"] == "complete":
                    self.ui.show_success("Review complete!")
                    if event.get("cost"):
                        self.ui.show_message(f"Cost: ${event['cost']:.4f}", "dim")

            # Save review to project directory
            if review_text:
                review_file = (
                    self.current_project.get_project_dir(self.project_manager.data_dir)
                    / "latest_review.md"
                )
                review_file.write_text("\n\n".join(review_text))
                self.ui.show_message(f"\nReview saved to: {review_file}", "green")

        except Exception as e:
            self.ui.show_error(f"Review failed: {str(e)}")

    def view_characters(self) -> None:
        """View tracked characters."""
        self.ui.show_message("\n[bold cyan]Character Tracker[/bold cyan]", "white")
        self.ui.print_separator()
        self.ui.show_characters(self.current_project)

    def view_plot_events(self) -> None:
        """View tracked plot events."""
        self.ui.show_message("\n[bold cyan]Plot Events[/bold cyan]", "white")
        self.ui.print_separator()
        self.ui.show_plot_events(self.current_project)

    async def export_manuscript(self) -> None:
        """Export the manuscript."""
        self.ui.show_message("\n[bold cyan]Export Manuscript[/bold cyan]", "white")
        self.ui.print_separator()

        export_path = Path(self.ui.prompt_file_path("Export path (e.g., output.docx)"))
        format_type = self.converter.detect_format(export_path)

        if format_type == "unknown":
            self.ui.show_error("Unsupported format. Use .docx, .pdf, or .md")
            return

        try:
            with self.ui.spinner("Exporting...") as progress:
                progress.add_task("Exporting...", total=None)

                content = self.project_manager.get_manuscript_content(self.current_project)
                self.converter.export_document(
                    content, export_path, title=self.current_project.metadata.title
                )

            self.ui.show_success(f"Manuscript exported to: {export_path}")

        except Exception as e:
            self.ui.show_error(f"Export failed: {str(e)}")

    async def project_settings(self) -> None:
        """Edit project settings."""
        self.ui.show_message("\n[bold cyan]Project Settings[/bold cyan]", "white")
        self.ui.print_separator()

        if self.ui.confirm("Update title?"):
            new_title = self.ui.prompt_manuscript_title(default=self.current_project.metadata.title)
            self.current_project.metadata.title = new_title

        if self.ui.confirm("Update genre?"):
            new_genre = self.ui.prompt_genre()
            self.current_project.metadata.genre = new_genre

        if self.ui.confirm("Update author?"):
            new_author = self.ui.prompt_file_path("Author name")
            self.current_project.metadata.author = new_author

        self.project_manager.save_project(self.current_project)
        self.ui.show_success("Settings updated!")


def main() -> None:
    """Main entry point."""
    app = StorybookApp()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
