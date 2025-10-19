# Storybook - AI-Powered Manuscript Editor

A sophisticated console application for fiction authors to edit and refine their manuscripts using Claude AI.

## Features

- **Project Management**: Create, import, edit, and delete manuscript projects
- **Document Import**: Support for DOCX, PDF, and plain text files
- **Interactive Chat**: Natural conversation interface for manuscript editing
- **Automated Literary Review**: Fiction-focused editorial feedback
- **Character Continuity**: Track and maintain character consistency
- **Event/Plot Tracking**: Monitor plot points and story progression
- **Export Options**: Export to DOCX, PDF, or Markdown

## Installation

```bash
# Install from source
cd storybook
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

## Quick Start

```bash
# Launch Storybook
storybook

# Follow the menu to:
# 1. Create a new project
# 2. Import an existing manuscript
# 3. Start editing with AI assistance
```

## Usage

### Creating a New Project

1. Select "New Project" from the main menu
2. Enter a project name
3. Optionally import an existing manuscript file
4. Start editing through the chat interface

### Editing Your Manuscript

Once in a project, you can:
- Ask Claude to review specific chapters
- Request grammar and style improvements
- Get character consistency checks
- Analyze plot structure
- Apply automated literary editor suggestions

### Character Tracking

Storybook automatically tracks:
- Character names and aliases
- Physical descriptions
- Personality traits
- Character arcs

### Export Your Work

Export your edited manuscript in multiple formats:
- DOCX (Microsoft Word)
- PDF (portable document)
- Markdown (plain text with formatting)

## Examples

See the `examples/` directory for sample manuscripts and editing workflows.

## Requirements

- Python 3.10+
- Claude Code CLI (install from https://claude.com/claude-code)
- Anthropic API key (set as `ANTHROPIC_API_KEY` environment variable)

## License

MIT
