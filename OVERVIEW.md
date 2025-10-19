# Storybook - AI-Powered Manuscript Editor

## 🎯 Project Overview

**Storybook** is a sophisticated console application built with the Claude Agent SDK that enables fiction authors to edit and refine their manuscripts using Claude AI. It provides an interactive chat interface, automated literary reviews, character/plot tracking, and multi-format document support.

## ✨ Key Features

### 1. **Full Project Management**
- Create new manuscript projects
- Import existing manuscripts (DOCX, PDF, TXT, Markdown)
- Edit project metadata (title, genre, author)
- Delete projects with confirmation
- Automatic word count tracking

### 2. **Interactive Chat Interface**
- Natural conversation with Claude for manuscript editing
- Contextual awareness across conversation turns
- Tool usage for reading, editing, and analyzing manuscripts
- Permission system for edit approval
- Thinking blocks to show Claude's reasoning

### 3. **Automated Literary Review**
- Comprehensive editorial feedback on manuscripts
- Fiction-specific analysis covering:
  - Plot structure and pacing
  - Character development
  - Prose quality and style
  - Technical elements (grammar, punctuation)
  - Genre conventions
- Customizable focus areas
- Detailed, actionable suggestions
- Review saved to project directory

### 4. **Character Continuity Tracking**
- Automatic character detection and tracking
- Store character names, aliases, descriptions, and traits
- Check character name consistency across manuscript
- View all tracked characters in table format

### 5. **Event/Plot Continuity Tracking**
- Track major plot events and story beats
- Record chapter references and character involvement
- Importance levels (low, medium, high, critical)
- Timeline consistency analysis
- View all plot events in organized table

### 6. **Document Import/Export**
- **Import formats**: DOCX, PDF, TXT, Markdown
- **Export formats**: DOCX, Markdown (PDF planned)
- Preserves structure and formatting where possible
- Automatic conversion to Markdown for editing

### 7. **Custom MCP Tools**
Eight specialized tools for manuscript analysis:
- `track_character` - Store character information
- `list_characters` - View all tracked characters
- `check_character_consistency` - Verify character consistency
- `track_plot_event` - Record plot points
- `list_plot_events` - View all plot events
- `analyze_plot_timeline` - Check timeline consistency
- `analyze_prose_quality` - Evaluate prose and style
- `detect_pacing_issues` - Identify pacing problems

### 8. **Rich Console UI**
- Beautiful terminal interface using Rich library
- Formatted tables for projects, characters, and plot events
- Progress indicators for long operations
- Markdown rendering for Claude's responses
- Color-coded messages and panels
- Clear navigation menus

## 📁 Project Structure

```
storybook/
├── src/storybook/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Main application and CLI entry point
│   ├── models.py            # Data models (Project, Character, PlotEvent, etc.)
│   ├── project_manager.py   # Project CRUD operations
│   ├── document_converter.py # Import/export for DOCX, PDF, TXT
│   ├── tools.py             # Custom MCP tools for manuscript analysis
│   ├── editor.py            # Automated literary editor
│   ├── chat.py              # Interactive chat session management
│   └── ui.py                # Rich console UI components
├── examples/
│   ├── sample_chapter.md    # Sample manuscript for testing
│   └── quick_start.py       # Programmatic API examples
├── tests/                   # Test suite (to be implemented)
├── data/                    # Default data directory (gitignored)
├── pyproject.toml           # Project configuration and dependencies
├── README.md                # Project overview
├── INSTALL.md               # Installation instructions
├── USAGE.md                 # Detailed usage guide
└── .gitignore               # Git ignore rules
```

## 🏗️ Architecture

### Technology Stack

- **Python 3.10+**: Core language
- **Claude Agent SDK**: AI agent framework
- **Rich**: Terminal UI library
- **Pydantic**: Data validation and models
- **python-docx**: DOCX import/export
- **pypdf**: PDF import
- **Prompt Toolkit**: Enhanced input handling

### Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Main Application                      │
│                      (main.py)                          │
└───────────────┬─────────────────────────────────────────┘
                │
        ┌───────┴───────┐
        │               │
┌───────▼──────┐  ┌────▼─────────────────────────────────┐
│   UI Layer   │  │   Business Logic Layer                │
│   (ui.py)    │  │                                       │
│              │  │  ┌─────────────────┐                  │
│  - Menus     │  │  │ Project Manager │                  │
│  - Tables    │  │  │ (project_mgr.py)│                  │
│  - Prompts   │  │  └────────┬────────┘                  │
│  - Markdown  │  │           │                           │
└──────────────┘  │  ┌────────▼────────┐                  │
                  │  │ Document Conv.  │                  │
                  │  │ (doc_conv.py)   │                  │
                  │  └────────┬────────┘                  │
                  │           │                           │
                  │  ┌────────▼────────┐                  │
                  │  │ Chat Session    │                  │
                  │  │ (chat.py)       │                  │
                  │  └────────┬────────┘                  │
                  │           │                           │
                  │  ┌────────▼────────┐                  │
                  │  │ Literary Editor │                  │
                  │  │ (editor.py)     │                  │
                  │  └────────┬────────┘                  │
                  │           │                           │
                  │  ┌────────▼────────┐                  │
                  │  │ Custom Tools    │                  │
                  │  │ (tools.py)      │                  │
                  │  └─────────────────┘                  │
                  └───────────────────────────────────────┘
                                │
                  ┌─────────────▼──────────────┐
                  │   Claude Agent SDK         │
                  │   (ClaudeSDKClient)        │
                  └─────────────┬──────────────┘
                                │
                  ┌─────────────▼──────────────┐
                  │   Claude API               │
                  │   (Sonnet 4.5)             │
                  └────────────────────────────┘
```

### Data Flow

1. **User Input** → UI Layer → Main Application
2. **Main Application** → Business Logic (Project Manager, Editor, Chat)
3. **Business Logic** → Claude Agent SDK (with custom tools)
4. **Claude Agent SDK** → Claude API
5. **Claude API** → Response → SDK → Business Logic
6. **Business Logic** → UI Layer → **User Output**

### Data Persistence

```
~/.storybook/projects/
├── {project-id-1}/
│   ├── project.json         # Project metadata, characters, plot events
│   ├── manuscript.md        # Main manuscript file
│   └── latest_review.md     # Most recent editorial review
├── {project-id-2}/
│   ├── project.json
│   ├── manuscript.md
│   └── latest_review.md
└── ...
```

## 🔧 Technical Details

### Models (Pydantic)

- **Project**: Main project container
- **ManuscriptMetadata**: Title, author, genre, word count
- **Character**: Name, aliases, description, traits, notes
- **PlotEvent**: Title, description, chapter, characters, importance
- **ReviewSuggestion**: Type, severity, issue, suggestion
- **EditorReview**: Overall assessment, strengths, weaknesses, suggestions

### Claude Integration

- **Model**: claude-sonnet-4-5 (with extended thinking)
- **System Prompt**: Specialized literary editor persona for fiction
- **Tools**: Built-in file tools + 8 custom MCP tools
- **Permission Mode**: Default (asks for edit approval)
- **Context Management**: Maintains conversation state across turns

### Custom MCP Server

The `create_storybook_tools()` function creates an in-process MCP server with:
- Character tracking and consistency checking
- Plot event tracking and timeline analysis
- Prose quality analysis
- Pacing detection

All tools are async and return structured JSON responses.

## 🚀 Usage Workflows

### Workflow 1: New Manuscript

1. Create new project
2. Open project → Chat with Editor
3. Write opening in manuscript file
4. Chat: "Review my opening paragraph"
5. Iterate based on feedback
6. Run automated review periodically
7. Export to DOCX when ready

### Workflow 2: Import and Improve

1. Import existing manuscript (DOCX/PDF)
2. Open project → Run Automated Review
3. Review feedback on plot, characters, prose
4. Open chat session
5. Chat: "Let's improve the pacing in Chapter 2"
6. Apply suggested edits
7. View tracked characters and plot events
8. Export improved version

### Workflow 3: Ongoing Development

1. Open existing project
2. Check character/plot tracking
3. Chat: "I want to add a subplot involving Marcus"
4. Claude suggests integration points
5. Make edits collaboratively
6. Run quick reviews on new sections
7. Maintain consistency with tracked elements

## 🎨 UI Design Principles

- **Clarity**: Clear menu structure and navigation
- **Feedback**: Progress indicators for long operations
- **Beauty**: Rich formatting with colors and panels
- **Efficiency**: Keyboard-driven interface
- **Safety**: Confirmation prompts for destructive actions

## 🔮 Future Enhancements

### Potential Features

1. **Multi-document projects**: Support for multiple chapters as separate files
2. **Version control**: Track manuscript versions and changes
3. **Collaboration**: Share projects with beta readers
4. **Advanced export**: PDF generation, ePub format
5. **Theme support**: Customize plot structure templates by genre
6. **Outline mode**: Dedicated outlining and structure planning
7. **Writing statistics**: Daily word count, writing streaks, productivity metrics
8. **AI personas**: Different editor personalities (developmental, copy editor, agent)
9. **Batch operations**: Apply edits across multiple chapters
10. **Web interface**: Browser-based version of the application

### Technical Improvements

1. **Test suite**: Comprehensive unit and integration tests
2. **Performance**: Caching for faster manuscript analysis
3. **Offline mode**: Work without API calls
4. **Plugin system**: User-created custom tools
5. **Configuration**: Customizable system prompts and tool behavior

## 📊 Performance Considerations

### API Costs

- **Chat sessions**: ~$0.01-0.05 per exchange (depends on manuscript length)
- **Automated reviews**: ~$0.10-0.50 per full manuscript (varies by length)
- **Quick feedback**: ~$0.005-0.02 per query

### Optimization Strategies

1. Use focused questions instead of broad reviews
2. Export and review offline for planning
3. Leverage character/plot tracking to reduce context
4. Use permission mode to control API usage
5. Cache review results for reference

## 🤝 Contributing

Areas for contribution:
- Additional MCP tools (style analysis, dialogue tagging, etc.)
- Export formats (ePub, PDF via LaTeX)
- UI themes and customization
- Test coverage
- Documentation improvements
- Example manuscripts and workflows

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
- Powered by [Anthropic's Claude](https://www.anthropic.com/claude)
- UI built with [Rich](https://github.com/Textualize/rich)

## 📞 Support

- **Documentation**: See README.md, INSTALL.md, and USAGE.md
- **Examples**: Check examples/ directory
- **Issues**: Report bugs or request features on the issue tracker

---

**Storybook** - Empowering authors with AI-assisted manuscript editing.
