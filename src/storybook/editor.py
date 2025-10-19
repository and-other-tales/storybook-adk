"""Automated literary editor for fiction manuscripts."""

from typing import Any, AsyncIterator

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ResultMessage,
)

from .models import Project
from .project_manager import ProjectManager
from .tools import create_storybook_tools


class LiteraryEditor:
    """Automated literary editor powered by Claude."""

    FICTION_EDITOR_PROMPT = """You are an expert literary editor specializing in fiction.
Your role is to provide constructive, professional feedback on manuscripts to help authors
improve their work.

When reviewing fiction, focus on:

1. **Story & Plot**
   - Plot structure and pacing
   - Story arcs and tension
   - Plot holes or inconsistencies
   - Scene transitions

2. **Characters**
   - Character development and depth
   - Character voice consistency
   - Motivations and actions
   - Dialogue authenticity

3. **Prose & Style**
   - Sentence variety and flow
   - Word choice and imagery
   - Show vs. tell balance
   - Passive vs. active voice

4. **Technical Elements**
   - Grammar and punctuation
   - Spelling and typos
   - Paragraph structure
   - Point of view consistency

5. **Genre Conventions**
   - Genre-appropriate elements
   - Tropes and expectations
   - Target audience fit

Provide feedback that is:
- Specific and actionable
- Balanced (both strengths and areas for improvement)
- Encouraging and supportive
- Focused on helping the author's vision

When using tools:
- Use track_character for each significant character you identify
- Use track_plot_event for major plot points
- Use check_character_consistency to verify character names and descriptions
- Use analyze_prose_quality on representative samples
- Use detect_pacing_issues on each chapter

Always maintain a professional, supportive tone. Remember that you're helping
the author improve their craft, not rewriting their work."""

    def __init__(self, project_manager: ProjectManager):
        """Initialize the literary editor.

        Args:
            project_manager: Project manager instance
        """
        self.project_manager = project_manager
        self.tools = create_storybook_tools()

    async def review_manuscript(
        self, project: Project, focus_areas: list[str] | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """Perform a comprehensive review of the manuscript.

        Args:
            project: The project to review
            focus_areas: Optional list of specific areas to focus on
                        (e.g., ['plot', 'characters', 'prose'])

        Yields:
            Review progress messages
        """
        manuscript_path = project.get_manuscript_path(self.project_manager.data_dir)

        # Build the review prompt
        prompt = f"""Please perform a comprehensive editorial review of this manuscript.

Manuscript: {manuscript_path}
Title: {project.metadata.title}
Genre: {project.metadata.genre}
Word Count: {project.metadata.word_count:,}

"""

        if focus_areas:
            prompt += f"Focus particularly on: {', '.join(focus_areas)}\n\n"

        prompt += """Please:
1. Read the entire manuscript carefully
2. Track all major characters using the track_character tool
3. Track key plot events using the track_plot_event tool
4. Analyze prose quality in different sections
5. Check for pacing issues
6. Provide a detailed review covering:
   - Overall assessment
   - Key strengths
   - Areas for improvement
   - Specific, actionable suggestions
   - Character development notes
   - Plot and structure feedback

Structure your review as:
## Overall Assessment
## Strengths
## Areas for Improvement
## Detailed Feedback
### Plot & Structure
### Characters
### Prose & Style
### Technical Elements
## Recommendations
"""

        # Configure Claude with literary editor system prompt
        options = ClaudeAgentOptions(
            allowed_tools=[
                "Read",
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
            system_prompt=self.FICTION_EDITOR_PROMPT,
            mcp_servers={"storybook": self.tools},
            cwd=str(self.project_manager.data_dir),
            model="claude-sonnet-4-5",
            permission_mode="bypassPermissions",
        )

        async with ClaudeSDKClient(options) as client:
            yield {"type": "status", "message": "Starting manuscript review..."}

            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            yield {"type": "text", "content": block.text}
                        elif isinstance(block, ToolUseBlock):
                            yield {"type": "tool_use", "tool": block.name, "input": block.input}
                elif isinstance(message, ResultMessage):
                    yield {
                        "type": "complete",
                        "cost": message.total_cost_usd,
                        "turns": message.num_turns,
                    }

    async def quick_feedback(
        self, project: Project, question: str
    ) -> AsyncIterator[dict[str, Any]]:
        """Get quick feedback on a specific aspect of the manuscript.

        Args:
            project: The project
            question: The specific question or area of concern

        Yields:
            Feedback messages
        """
        manuscript_path = project.get_manuscript_path(self.project_manager.data_dir)

        prompt = f"""As a fiction editor, please address this question about the manuscript:

Manuscript: {manuscript_path}
Title: {project.metadata.title}

Question: {question}

Please provide specific, actionable feedback based on the manuscript content.
Use the available tools to analyze the text as needed.
"""

        options = ClaudeAgentOptions(
            allowed_tools=[
                "Read",
                "Grep",
                "mcp__storybook__track_character",
                "mcp__storybook__check_character_consistency",
                "mcp__storybook__analyze_plot_timeline",
                "mcp__storybook__analyze_prose_quality",
                "mcp__storybook__detect_pacing_issues",
            ],
            system_prompt=self.FICTION_EDITOR_PROMPT,
            mcp_servers={"storybook": self.tools},
            cwd=str(self.project_manager.data_dir),
            model="claude-sonnet-4-5",
            permission_mode="bypassPermissions",
        )

        async with ClaudeSDKClient(options) as client:
            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            yield {"type": "text", "content": block.text}
                        elif isinstance(block, ToolUseBlock):
                            yield {"type": "tool_use", "tool": block.name}
                elif isinstance(message, ResultMessage):
                    yield {"type": "complete", "cost": message.total_cost_usd}
