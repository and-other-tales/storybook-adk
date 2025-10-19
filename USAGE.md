# Storybook Usage Guide

This guide covers the main features and workflows for using Storybook.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating Projects](#creating-projects)
3. [Importing Manuscripts](#importing-manuscripts)
4. [Interactive Chat Editing](#interactive-chat-editing)
5. [Automated Review](#automated-review)
6. [Character & Plot Tracking](#character--plot-tracking)
7. [Exporting Your Work](#exporting-your-work)
8. [Advanced Features](#advanced-features)

## Getting Started

### Installation

```bash
cd storybook
pip install -e .
```

### Prerequisites

1. **Claude Code CLI**: Install from https://claude.com/claude-code
2. **API Key**: Set your Anthropic API key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   ```

### Launching Storybook

```bash
storybook
```

## Creating Projects

### From Scratch

1. Select **"New Project"** from the main menu
2. Enter a project name
3. Enter manuscript title
4. Select genre from the list
5. Start editing!

### Project Structure

Each project stores:
- `manuscript.md` - Your manuscript in Markdown format
- `project.json` - Project metadata, characters, and plot events
- `latest_review.md` - Most recent editorial review (if run)

## Importing Manuscripts

### Supported Formats

- **DOCX** - Microsoft Word documents
- **PDF** - Portable Document Format
- **TXT/MD** - Plain text and Markdown

### Import Process

1. Select **"Import Project"** from the main menu
2. Enter the path to your manuscript file
3. Provide project details (name, title, genre)
4. Storybook will convert the document to Markdown

### Import Notes

- **DOCX**: Preserves heading structure and basic formatting
- **PDF**: Extracts text content (formatting may be lost)
- **TXT/MD**: Imports as-is

## Interactive Chat Editing

The chat interface provides natural conversation with Claude for manuscript editing.

### Starting a Chat Session

1. Open a project
2. Select **"Chat with Editor"**
3. Type your requests and press Enter
4. Type `quit` to exit

### Example Conversations

#### Grammar and Style

```
You: Review the opening paragraph for grammar and style issues.

Editor: I've read the opening. Here are some suggestions:
1. Consider varying sentence structure...
2. The phrase "clung to the cobblestones" is vivid...
```

#### Character Development

```
You: Make Sarah's character more relatable in the opening scene.

Editor: I can enhance Sarah's relatability by adding internal thoughts...
[Uses Edit tool to modify the manuscript]
I've added a brief internal monologue that reveals her anxiety...
```

#### Plot Suggestions

```
You: What if the old man isn't what he seems? How could I foreshadow this?

Editor: Excellent idea! Here are some subtle ways to foreshadow:
1. Have Sarah notice something odd about his shadow...
2. The walking stick could have the same symbols as the key...
```

### Chat Features

- **Contextual awareness**: Claude remembers the conversation and manuscript content
- **Tool usage**: Claude can read, edit, and analyze your manuscript
- **Character tracking**: Automatically tracks characters as they're discussed
- **Permission system**: You'll be asked to approve edits before they're made

## Automated Review

Get comprehensive editorial feedback on your manuscript.

### Running a Review

1. Open a project
2. Select **"Run Automated Review"**
3. Optionally choose focus areas:
   - Plot
   - Characters
   - Prose
   - Pacing
   - Dialogue
4. Wait for the review (may take several minutes)

### Review Structure

The automated review covers:

1. **Overall Assessment**: High-level evaluation of the manuscript
2. **Strengths**: What's working well
3. **Areas for Improvement**: What needs attention
4. **Detailed Feedback**:
   - Plot & Structure
   - Character Development
   - Prose & Style
   - Technical Elements (grammar, punctuation)
5. **Recommendations**: Specific, actionable next steps

### Review Output

Reviews are:
- Displayed in the console with rich formatting
- Saved to `latest_review.md` in the project directory
- Accessible anytime for reference

## Character & Plot Tracking

Storybook automatically tracks characters and plot events as you work.

### Viewing Characters

1. Open a project
2. Select **"View Characters"**

The character tracker shows:
- Character names and aliases
- Physical descriptions
- Personality traits
- First appearance location

### Viewing Plot Events

1. Open a project
2. Select **"View Plot Events"**

The plot tracker shows:
- Event titles and descriptions
- Chapter references
- Characters involved
- Importance level (low, medium, high, critical)

### How Tracking Works

Characters and events are automatically tracked when:
- Running automated reviews
- Using specific chat commands
- Claude identifies them during editing

You can also manually track items by asking Claude:

```
You: Track a new character named Marcus, a mysterious stranger with a scar.

You: Track this plot event: Sarah discovers the key's true purpose in Chapter 5.
```

## Exporting Your Work

### Export Formats

- **Markdown (.md)**: Preserves all formatting
- **DOCX (.docx)**: For use in Microsoft Word
- **PDF (.pdf)**: For sharing and distribution

### Export Process

1. Open a project
2. Select **"Export Manuscript"**
3. Enter destination path with extension (e.g., `my_novel.docx`)
4. File is created with proper formatting

### Export Tips

- **DOCX**: Best for further editing in Word processors
- **MD**: Best for version control and plain text editing
- **PDF**: Best for sharing with beta readers or agents

## Advanced Features

### Project Settings

Update project metadata:
1. Open a project
2. Select **"Project Settings"**
3. Update title, genre, or author information

### Custom Tools

Claude has access to specialized manuscript tools:

- **track_character**: Store character information
- **check_character_consistency**: Verify character name/description consistency
- **track_plot_event**: Record plot points
- **analyze_plot_timeline**: Check timeline consistency
- **analyze_prose_quality**: Evaluate prose and style
- **detect_pacing_issues**: Identify pacing problems

These tools are used automatically during reviews and chat sessions.

### Multi-Turn Editing

The chat session maintains context across turns:

```
You: Review chapter 1.
[Claude provides feedback]

You: Now apply those suggestions.
[Claude remembers the feedback and makes edits]

You: How does the revised version compare?
[Claude analyzes the changes made]
```

### Permission System

When Claude wants to edit your manuscript, you'll see:
```
[Tool: Edit - Modify opening paragraph]
Allow this edit? (y/n)
```

You can:
- **Allow**: Apply the edit
- **Deny**: Skip this edit
- **Modify**: Suggest changes to the edit

## Tips for Best Results

### 1. Be Specific

Instead of:
```
You: Make it better.
```

Try:
```
You: Make the dialogue more natural and add more conflict between Sarah and Dr. Chen.
```

### 2. Iterate

Start with broad feedback, then drill down:
```
You: Review the overall plot structure.
[Review feedback]

You: Let's focus on improving the pacing in Chapter 2.
[Specific suggestions]

You: Apply the pacing improvements to the scene where Sarah finds the key.
[Edits applied]
```

### 3. Use Reviews Strategically

- **Full manuscript review**: After completing a draft
- **Chapter review**: After finishing each chapter
- **Quick feedback**: For specific questions or concerns

### 4. Track Early

Ask Claude to track characters and events early in the writing process:
```
You: As you read, please track all major characters and plot events.
```

This helps maintain consistency throughout the manuscript.

### 5. Save Often

After significant edits:
```
You: Please save the current version.
```

Or export to create backups:
```
You: Export the current manuscript to backup_v2.md.
```

## Troubleshooting

### Common Issues

**Import fails with "Unsupported format"**
- Ensure file has .docx, .pdf, .txt, or .md extension
- Check that required libraries are installed (`pip install python-docx pypdf`)

**Chat session costs too much**
- Use focused questions instead of "review everything"
- Export and review offline for planning
- Use quick feedback for specific questions

**Character tracking not working**
- Run an automated review to populate character data
- Explicitly ask Claude to track characters in chat

**Exports not formatting correctly**
- DOCX export requires `python-docx` library
- Ensure proper file extension (.docx, .pdf, .md)

## Next Steps

- Explore the examples in `examples/`
- Read the API documentation for programmatic use
- Join the community to share tips and workflows

Happy writing!
