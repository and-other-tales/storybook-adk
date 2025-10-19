"""Rich console UI for Storybook."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from .models import Project


class StorybookUI:
    """Rich console interface for Storybook."""

    def __init__(self):
        """Initialize the UI."""
        self.console = Console()

    def show_banner(self) -> None:
        """Display the application banner."""
        banner = """
  ____  _                  _                 _
 / ___|| |_ ___  _ __ _  _| |__   ___   ___ | | __
 \\___ \\| __/ _ \\| '__| || | '_ \\ / _ \\ / _ \\| |/ /
  ___) | || (_) | |  | || | |_) | (_) | (_) |   <
 |____/ \\__\\___/|_|   \\__, |_.__/ \\___/ \\___/|_|\\_\\
                      |___/
        AI-Powered Manuscript Editor
        """
        self.console.print(banner, style="bold cyan")
        self.console.print()

    def show_main_menu(self) -> str:
        """Display the main menu and get user choice.

        Returns:
            User's menu choice
        """
        self.console.print("\n[bold cyan]Main Menu[/bold cyan]")
        self.console.print("━" * 50)
        self.console.print("1. New Project")
        self.console.print("2. Open Project")
        self.console.print("3. Import Project")
        self.console.print("4. Delete Project")
        self.console.print("5. Exit")
        self.console.print("━" * 50)

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
        return choice

    def show_project_menu(self, project: Project) -> str:
        """Display the project menu.

        Args:
            project: Current project

        Returns:
            User's menu choice
        """
        self.console.print(f"\n[bold cyan]Project: {project.name}[/bold cyan]")
        self.console.print("━" * 50)
        self.console.print(f"Title: {project.metadata.title}")
        self.console.print(f"Genre: {project.metadata.genre}")
        self.console.print(f"Word Count: {project.metadata.word_count:,}")
        self.console.print(f"Last Edited: {project.last_edited.strftime('%Y-%m-%d %H:%M')}")
        self.console.print("━" * 50)
        self.console.print("1. Chat with Editor")
        self.console.print("2. Run Automated Review")
        self.console.print("3. View Characters")
        self.console.print("4. View Plot Events")
        self.console.print("5. Export Manuscript")
        self.console.print("6. Project Settings")
        self.console.print("7. Back to Main Menu")
        self.console.print("━" * 50)

        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7"])
        return choice

    def list_projects(self, projects: list[Project]) -> None:
        """Display a list of projects.

        Args:
            projects: List of projects to display
        """
        if not projects:
            self.console.print("[yellow]No projects found.[/yellow]")
            return

        table = Table(title="Your Projects")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Name", style="magenta")
        table.add_column("Title", style="green")
        table.add_column("Words", justify="right", style="blue")
        table.add_column("Last Edited", style="yellow")

        for project in projects:
            table.add_row(
                project.id[:8],
                project.name,
                project.metadata.title,
                f"{project.metadata.word_count:,}",
                project.last_edited.strftime("%Y-%m-%d"),
            )

        self.console.print(table)

    def show_characters(self, project: Project) -> None:
        """Display tracked characters.

        Args:
            project: Current project
        """
        if not project.characters:
            self.console.print("[yellow]No characters tracked yet.[/yellow]")
            return

        table = Table(title="Characters")
        table.add_column("Name", style="cyan")
        table.add_column("Aliases", style="magenta")
        table.add_column("Description", style="green")
        table.add_column("Traits", style="blue")

        for char in project.characters:
            table.add_row(
                char.name,
                ", ".join(char.aliases) if char.aliases else "—",
                char.description[:50] + "..." if len(char.description) > 50 else char.description,
                ", ".join(char.traits[:3]) if char.traits else "—",
            )

        self.console.print(table)

    def show_plot_events(self, project: Project) -> None:
        """Display tracked plot events.

        Args:
            project: Current project
        """
        if not project.plot_events:
            self.console.print("[yellow]No plot events tracked yet.[/yellow]")
            return

        table = Table(title="Plot Events")
        table.add_column("Title", style="cyan")
        table.add_column("Chapter", style="magenta")
        table.add_column("Characters", style="green")
        table.add_column("Importance", style="yellow")

        for event in project.plot_events:
            table.add_row(
                event.title,
                event.chapter_reference or "—",
                ", ".join(event.characters_involved[:3]) if event.characters_involved else "—",
                event.importance,
            )

        self.console.print(table)

    def prompt_project_name(self) -> str:
        """Prompt for project name.

        Returns:
            Project name
        """
        return Prompt.ask("[cyan]Project name[/cyan]")

    def prompt_manuscript_title(self, default: str = "") -> str:
        """Prompt for manuscript title.

        Args:
            default: Default value

        Returns:
            Manuscript title
        """
        return Prompt.ask("[cyan]Manuscript title[/cyan]", default=default)

    def prompt_genre(self) -> str:
        """Prompt for genre.

        Returns:
            Genre
        """
        return Prompt.ask(
            "[cyan]Genre[/cyan]",
            default="Fiction",
            choices=[
                "Fiction",
                "Fantasy",
                "Science Fiction",
                "Mystery",
                "Thriller",
                "Romance",
                "Literary Fiction",
                "Horror",
                "Historical Fiction",
                "Other",
            ],
        )

    def prompt_file_path(self, prompt_text: str = "File path") -> str:
        """Prompt for a file path.

        Args:
            prompt_text: The prompt text

        Returns:
            File path
        """
        return Prompt.ask(f"[cyan]{prompt_text}[/cyan]")

    def confirm(self, message: str) -> bool:
        """Show a confirmation prompt.

        Args:
            message: Confirmation message

        Returns:
            True if confirmed, False otherwise
        """
        return Confirm.ask(f"[yellow]{message}[/yellow]")

    def show_message(self, message: str, style: str = "white") -> None:
        """Display a message.

        Args:
            message: Message to display
            style: Rich style string
        """
        self.console.print(f"[{style}]{message}[/{style}]")

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: Error message
        """
        self.console.print(f"[bold red]Error:[/bold red] {message}")

    def show_success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: Success message
        """
        self.console.print(f"[bold green]✓[/bold green] {message}")

    def show_markdown(self, content: str) -> None:
        """Display markdown content.

        Args:
            content: Markdown content
        """
        md = Markdown(content)
        self.console.print(md)

    def show_panel(self, content: str, title: str = "", style: str = "cyan") -> None:
        """Display content in a panel.

        Args:
            content: Panel content
            title: Panel title
            style: Panel style
        """
        panel = Panel(content, title=title, border_style=style)
        self.console.print(panel)

    def spinner(self, message: str = "Processing..."):
        """Create a progress spinner context.

        Args:
            message: Status message

        Returns:
            Progress context manager
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        )

    def input_multiline(self, prompt_text: str = "Enter your message (Ctrl+D to finish)") -> str:
        """Get multiline input from user.

        Args:
            prompt_text: Prompt message

        Returns:
            User input
        """
        self.console.print(f"[cyan]{prompt_text}[/cyan]")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        return "\n".join(lines)

    def clear(self) -> None:
        """Clear the console."""
        self.console.clear()

    def print_separator(self) -> None:
        """Print a separator line."""
        self.console.print("━" * 50, style="dim")
