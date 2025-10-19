# Storybook - AI-Powered Manuscript Editor

A sophisticated application for fiction authors to edit and refine their manuscripts using Claude AI. Available as both a **CLI application** and a **modern web interface**.

## 🎯 Choose Your Interface

### 📱 Web Application (Recommended)
Modern, real-time web interface with live chat, manuscript editor, and project management.

**Quick Start:**
```bash
cd storybook-web
./setup.sh
npm run dev
# Open http://localhost:3000
```

👉 **See [QUICKSTART_WEB.md](QUICKSTART_WEB.md)** for 5-minute setup guide
👉 **See [WEB_APP_README.md](WEB_APP_README.md)** for complete architecture

### 💻 CLI Application
Console-based interface for terminal enthusiasts.

**Quick Start:**
```bash
pip install -e .
storybook
```

👉 **See [USAGE.md](USAGE.md)** for CLI guide

## ✨ Features

### Core Capabilities
- **Project Management**: Create, import, edit, and delete manuscript projects
- **Document Import**: Support for DOCX, PDF, and plain text files
- **Interactive Chat**: Natural conversation interface with Claude AI
- **Automated Literary Review**: Fiction-focused editorial feedback
- **Character Continuity**: Track and maintain character consistency
- **Event/Plot Tracking**: Monitor plot points and story progression
- **Export Options**: Export to DOCX, PDF, or Markdown

### Web Application Features
- 🌐 **Modern Web UI** - Next.js 14 with React 18+
- ⚡ **Real-time Chat** - Live conversation with streaming responses
- 📝 **Manuscript Editor** - Full-featured editor with auto-save
- 👥 **Character Tracking** - Visual display of all characters
- 📖 **Plot Timeline** - Interactive plot event viewer
- 🔄 **Auto-sync** - Real-time updates across all tabs
- 💾 **Export/Import** - Upload and download manuscripts
- 📊 **Statistics** - Word count, character count, and more

### CLI Application Features
- 🎨 **Rich Console UI** - Beautiful terminal interface
- 🔧 **Interactive Menus** - Easy navigation and controls
- 📊 **Table Views** - Formatted tables for data
- 🎯 **Direct Control** - Full command-line access

## 🏗️ Architecture

### Web Application Stack
```
┌─────────────────────────────────────────────────────────┐
│           Next.js 14 Frontend (React 18+)                │
│  Modern UI with real-time updates and chat              │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST + WebSocket
┌────────────────────▼────────────────────────────────────┐
│        Express Backend (Node.js 20 + TypeScript)        │
│  REST API, Socket.IO, Python Bridge                     │
└────────────────────┬────────────────────────────────────┘
                     │ subprocess communication
┌────────────────────▼────────────────────────────────────┐
│              Python CLI Application                      │
│  Claude Agent SDK, Project Manager, Tools               │
└────────────────────┬────────────────────────────────────┘
                     │ Anthropic API
┌────────────────────▼────────────────────────────────────┐
│                 Claude AI (Sonnet 4.5)                  │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

**Web Application:**
- Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS
- Backend: Express, Socket.IO, Node.js 20
- Real-time: WebSocket with event streaming
- Integration: Python subprocess bridge

**CLI Application:**
- Python 3.10+
- Claude Agent SDK
- Rich (terminal UI)
- Pydantic (data validation)

**AI Integration:**
- Claude Sonnet 4.5 (extended thinking)
- Custom MCP tools (8 specialized tools)
- Context-aware conversations
- Streaming responses

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js 20+ (for web app)
- Anthropic API key

### Install CLI

```bash
# From source
git clone <repository>
cd storybook-adk
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Install Web Application

```bash
cd storybook-web
npm install
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## 🚀 Quick Start

### Web Application

```bash
cd storybook-web
./setup.sh           # Automated setup
npm run dev          # Start servers
# Open http://localhost:3000
```

**What runs:**
- Next.js frontend at `http://localhost:3000`
- Express backend at `http://localhost:3001`
- Python CLI integration via subprocess

### CLI Application

```bash
# Set your API key
export ANTHROPIC_API_KEY=your_key_here

# Launch Storybook
storybook

# Follow the menu to:
# 1. Create a new project
# 2. Import an existing manuscript
# 3. Start editing with AI assistance
```

## 📖 Usage

### Web Interface Workflow

1. **Create Project** - Click "New Project" on dashboard
2. **Import Manuscript** - Upload DOCX, PDF, or TXT file (optional)
3. **Chat with AI** - Get real-time feedback and suggestions
4. **Edit Manuscript** - Use the built-in editor
5. **Track Progress** - View characters and plot events
6. **Export** - Download as DOCX or Markdown

### CLI Interface Workflow

1. **Create Project** - Select "New Project" from menu
2. **Import File** - Optionally import existing manuscript
3. **Chat Mode** - Interactive conversation with Claude
4. **Run Review** - Automated literary analysis
5. **View Tracking** - Check characters and plot events
6. **Export** - Save in multiple formats

### Common Tasks

**Ask Claude for help:**
```
Web: Use "Chat with AI" tab
CLI: Select "Chat with Editor" from project menu
```

**Review your manuscript:**
```
Web: Click "Start Review" button
CLI: Select "Run Automated Review"
```

**Track characters:**
```
Web: Switch to "Characters" tab
CLI: Select "View Characters"
```

**Export your work:**
```
Web: Click "Export" → Choose format
CLI: Select "Export Project" → Choose format
```

## 📁 Project Structure

```
storybook-adk/
├── src/storybook/              # Python CLI application
│   ├── main.py                 # CLI entry point
│   ├── models.py               # Data models
│   ├── project_manager.py      # Project CRUD
│   ├── chat.py                 # Chat sessions
│   ├── editor.py               # Literary editor
│   ├── tools.py                # Custom MCP tools
│   ├── document_converter.py   # Import/export
│   ├── ui.py                   # Console UI
│   └── web_integration.py      # 🆕 Web API layer
│
├── storybook-web/              # 🆕 Web application
│   ├── app/                    # Next.js frontend
│   │   ├── components/         # React components
│   │   ├── lib/               # Client libraries
│   │   └── projects/          # Project pages
│   ├── server/                 # Express backend
│   │   ├── routes/            # API routes
│   │   ├── services/          # Backend services
│   │   └── types/             # TypeScript types
│   └── README.md              # Web app docs
│
├── tests/                      # Test suite
├── examples/                   # Sample manuscripts
├── data/                       # Local project storage
│
├── pyproject.toml             # Python config
├── README.md                  # This file
├── INSTALL.md                 # Installation guide
├── USAGE.md                   # CLI usage guide
├── WEB_APP_README.md          # 🆕 Web architecture
├── QUICKSTART_WEB.md          # 🆕 Web quick start
└── WEB_APP_SUMMARY.md         # 🆕 Implementation summary
```

## 🎨 Screenshots & UI

### Web Application
- **Dashboard**: Project cards with statistics
- **Chat Panel**: Real-time conversation with Claude
- **Editor**: Full-featured manuscript editor
- **Characters**: Visual character tracking
- **Plot Events**: Interactive timeline
- **Metadata**: Project settings and info

### CLI Application
- **Main Menu**: Project selection and management
- **Chat Interface**: Terminal-based conversation
- **Tables**: Formatted character and plot data
- **Progress Bars**: Visual feedback for operations

## 🔧 Advanced Features

### Custom MCP Tools
Eight specialized tools for manuscript analysis:
- `track_character` - Store character information
- `list_characters` - View all tracked characters
- `check_character_consistency` - Verify consistency
- `track_plot_event` - Record plot points
- `list_plot_events` - View all events
- `analyze_plot_timeline` - Check timeline
- `analyze_prose_quality` - Evaluate prose
- `detect_pacing_issues` - Identify pacing

### Real-time Features (Web)
- **Live Chat** - Streaming AI responses
- **Auto-save** - Automatic manuscript saving
- **WebSocket** - Real-time updates
- **Event Streaming** - Progress indicators
- **Thinking Visualization** - See AI reasoning

### API Access (Web)
REST API available at `http://localhost:3001/api`:
- `/projects` - Project management
- `/chat` - Chat sessions
- `/review` - Automated reviews

WebSocket events for real-time communication.

## 📚 Documentation

### Getting Started
- **[INSTALL.md](INSTALL.md)** - Detailed installation
- **[USAGE.md](USAGE.md)** - CLI usage guide
- **[QUICKSTART_WEB.md](QUICKSTART_WEB.md)** - Web quick start (5 min)

### Architecture & Development
- **[WEB_APP_README.md](WEB_APP_README.md)** - Complete web architecture
- **[WEB_APP_SUMMARY.md](WEB_APP_SUMMARY.md)** - Implementation details
- **[STORYBOOK_OVERVIEW.md](STORYBOOK_OVERVIEW.md)** - Project overview
- **[storybook-web/README.md](storybook-web/README.md)** - Web app specifics

### Examples
- **[examples/](examples/)** - Sample manuscripts and workflows
- **[DEMO.md](DEMO.md)** - Demo walkthrough

## 🎯 Use Cases

### For Authors
- **First Draft** - Write with AI assistance
- **Revision** - Get detailed feedback on structure and style
- **Character Work** - Track character consistency
- **Plot Development** - Monitor story progression
- **Final Polish** - Grammar and prose refinement

### For Editors
- **Manuscript Review** - Quick assessment of submissions
- **Developmental Editing** - Plot and character analysis
- **Copy Editing** - Grammar and style checking
- **Feedback** - Detailed, actionable suggestions

### For Writing Groups
- **Critique Partners** - Share and review work
- **Beta Readers** - Collect structured feedback
- **Writing Workshops** - Analyze group submissions

## 🔮 Future Enhancements

### Planned Features
- Multi-user support with authentication
- Collaborative real-time editing
- Manuscript version control
- Advanced search and filtering
- Mobile responsive design
- Progressive Web App (PWA)
- Offline mode with sync
- Custom AI prompts
- Analytics dashboard
- Writing statistics

### Technical Improvements
- Database integration (PostgreSQL)
- Redis caching
- Queue system for long operations
- Automated testing suite
- CI/CD pipeline
- Monitoring and logging
- Performance profiling

## 💡 Examples

### Example Chat Prompts

```
"Review the opening paragraph and suggest improvements"
"Check if Sarah's character is consistent throughout"
"Analyze the pacing of Chapter 3"
"Suggest ways to make the dialogue more natural"
"Identify any plot holes in the current draft"
```

### Example Workflows

**Workflow 1: New Novel**
```
1. Create project (web or CLI)
2. Write opening chapters
3. Chat with AI for feedback
4. Refine based on suggestions
5. Run automated review
6. Track characters as they appear
7. Export to DOCX for beta readers
```

**Workflow 2: Manuscript Revision**
```
1. Import existing manuscript (DOCX/PDF)
2. Run full automated review
3. Work through suggestions chapter by chapter
4. Use chat for specific questions
5. Check character consistency
6. Verify plot timeline
7. Export polished version
```

## 📊 Performance

### API Costs (Estimated)
- Chat session: ~$0.01-0.05 per exchange
- Automated review: ~$0.10-0.50 per manuscript
- Quick feedback: ~$0.005-0.02 per query

### Response Times
- API endpoint: ~50-150ms
- Chat streaming: Real-time (< 50ms latency)
- Review processing: 5-30 seconds
- Export operations: 1-5 seconds

## 🔒 Security

### Current Implementation
- Input validation on all endpoints
- TypeScript type safety
- Error handling and logging
- CORS configuration
- Environment variable protection

### Production Recommendations
- Add authentication (JWT)
- Implement authorization
- Enable rate limiting
- Use HTTPS
- Encrypt API keys
- Add session management
- Set up monitoring

## 🤝 Contributing

We welcome contributions! Areas for contribution:
- Additional MCP tools
- New export formats (ePub, PDF)
- UI themes and customization
- Test coverage
- Documentation improvements
- Example manuscripts
- Bug fixes and optimizations

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)
- Powered by [Anthropic's Claude](https://www.anthropic.com/claude)
- CLI UI built with [Rich](https://github.com/Textualize/rich)
- Web UI built with [Next.js](https://nextjs.org/)

## 📞 Support

### Getting Help
1. Check documentation (INSTALL.md, USAGE.md, WEB_APP_README.md)
2. Review examples in `examples/` directory
3. Search issues on GitHub
4. Create detailed bug reports

### Troubleshooting

**Web App Issues:**
- See [QUICKSTART_WEB.md](QUICKSTART_WEB.md) troubleshooting section
- Check browser console for errors
- Verify backend is running on port 3001
- Ensure `ANTHROPIC_API_KEY` is set

**CLI Issues:**
- Verify Python 3.10+ is installed
- Check virtual environment is activated
- Ensure API key is set: `export ANTHROPIC_API_KEY=...`
- Test with: `python -c "import storybook; print('OK')"`

## 🎬 Quick Reference

### Web Application
```bash
cd storybook-web
npm run dev                    # Start dev servers
npm run build                  # Build for production
npm start                      # Start production
```

### CLI Application
```bash
storybook                      # Launch CLI
pip install -e ".[dev]"        # Install with dev deps
pytest tests/                  # Run tests
```

### Environment Setup
```bash
# Python virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# Install dependencies
pip install -e .               # CLI
cd storybook-web && npm install  # Web
```

---

**Storybook** - Empowering authors with AI-assisted manuscript editing.

**Available as CLI and Web Application** - Choose your preferred interface!

**Built with Claude AI, Python, Next.js, and TypeScript**
