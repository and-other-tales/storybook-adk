"""Interactive chat interface for manuscript editing."""

from typing import AsyncIterator, Any

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
    ThinkingBlock,
)

from .models import Project
from .project_manager import ProjectManager
from .tools import create_storybook_tools


class ManuscriptChatSession:
    """Interactive chat session for manuscript editing."""

    def __init__(self, project: Project, project_manager: ProjectManager):
        """Initialize the chat session.

        Args:
            project: Current project
            project_manager: Project manager instance
        """
        self.project = project
        self.project_manager = project_manager
        self.tools = create_storybook_tools()
        self.client: ClaudeSDKClient | None = None

    async def start(self) -> None:
        """Start the chat session."""
        manuscript_path = self.project.get_manuscript_path(self.project_manager.data_dir)

        system_prompt = f"""You are an expert manuscript editor working with an author on their fiction manuscript.

Current Project:
- Title: {self.project.metadata.title}
- Genre: {self.project.metadata.genre}
- Manuscript: {manuscript_path}

Your role is to help the author improve their manuscript through:
1. Answering questions about the story, characters, or writing
2. Making specific edits to the text
3. Providing constructive feedback
4. Tracking characters and plot events
5. Analyzing prose quality and pacing

Tools available:
- File tools (Read, Write, Edit) - to read and modify the manuscript
- track_character - to track character information
- check_character_consistency - to verify character consistency
- track_plot_event - to track plot events
- analyze_plot_timeline - to check timeline consistency
- analyze_prose_quality - to analyze prose and style
- detect_pacing_issues - to identify pacing problems

Guidelines:
- Be supportive and encouraging
- Provide specific, actionable feedback
- Respect the author's creative vision
- Make edits only when requested
- Track important characters and events automatically
- Use tools proactively to provide better assistance

When making edits:
- Always read the relevant section first
- Make precise, targeted changes
- Explain what you changed and why
- Preserve the author's voice and style

Remember: You're a collaborative partner in the creative process, not just an automated tool.
"""

        options = ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Write",
                "Edit",
                "Grep",
                "mcp__storybook__track_character",
                "mcp__storybook__list_characters",
                "mcp__storybook__check_character_consistency",
                "mcp__storybook__track_plot_event",
                "mcp__storybook__list_plot_events",
                "mcp__storybook__analyze_plot_timeline",
                "mcp__storybook__analyze_prose_quality",
                "mcp__storybook__detect_pacing_issues",
            ],
            system_prompt=system_prompt,
            mcp_servers={"storybook": self.tools},
            cwd=str(self.project_manager.data_dir),
            model="claude-sonnet-4-5",
            permission_mode="default",  # Ask for permission on edits
            continue_conversation=True,
        )

        self.client = ClaudeSDKClient(options)
        await self.client.__aenter__()

    async def send_message(self, message: str) -> AsyncIterator[dict[str, Any]]:
        """Send a message and receive responses.

        Args:
            message: User message

        Yields:
            Response events
        """
        if not self.client:
            raise RuntimeError("Chat session not started")

        await self.client.query(message)

        async for msg in self.client.receive_response():
            if isinstance(msg, AssistantMessage):
                for block in msg.content:
                    if isinstance(block, TextBlock):
                        yield {"type": "text", "content": block.text}
                    elif isinstance(block, ThinkingBlock):
                        yield {"type": "thinking", "content": block.thinking}
                    elif isinstance(block, ToolUseBlock):
                        yield {
                            "type": "tool_use",
                            "tool": block.name,
                            "input": block.input,
                            "id": block.id,
                        }
            elif isinstance(msg, ResultMessage):
                yield {
                    "type": "complete",
                    "cost": msg.total_cost_usd,
                    "turns": msg.num_turns,
                    "session_id": msg.session_id,
                }

    async def close(self) -> None:
        """Close the chat session."""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None


class ChatInterface:
    """High-level chat interface."""

    def __init__(self, project: Project, project_manager: ProjectManager):
        """Initialize the chat interface.

        Args:
            project: Current project
            project_manager: Project manager instance
        """
        self.project = project
        self.project_manager = project_manager

    async def interactive_session(self) -> AsyncIterator[dict[str, Any]]:
        """Run an interactive chat session.

        Yields:
            Chat events and prompts
        """
        session = ManuscriptChatSession(self.project, self.project_manager)

        try:
            await session.start()
            yield {"type": "ready", "message": "Chat session started. Type 'quit' to exit."}

            while True:
                # Signal that we need user input
                yield {"type": "prompt", "message": "You"}

                # This will be handled by the main loop
                # The user input will be sent back via send_message
                break

        except Exception as e:
            yield {"type": "error", "message": str(e)}
        finally:
            await session.close()

    async def quick_edit(self, instruction: str) -> AsyncIterator[dict[str, Any]]:
        """Perform a quick edit based on an instruction.

        Args:
            instruction: Edit instruction

        Yields:
            Edit progress events
        """
        session = ManuscriptChatSession(self.project, self.project_manager)

        try:
            await session.start()

            async for event in session.send_message(instruction):
                yield event

        finally:
            await session.close()
