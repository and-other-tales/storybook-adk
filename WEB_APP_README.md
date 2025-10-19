# Storybook Web Application - Complete Guide

## Overview

The Storybook Web Application is a modern, full-stack implementation that provides complete real-time control of the Storybook CLI manuscript editor through a web interface.

## Architecture

### Full Stack Components

```
┌──────────────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Next.js 14 + React 18 Frontend                 │  │
│  │  - Project Dashboard                                    │  │
│  │  - Real-time Chat Interface                            │  │
│  │  - Manuscript Editor                                    │  │
│  │  - Character/Plot Tracking                             │  │
│  │  - Metadata Management                                 │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────┬───────────────────────────────┬───────────────┘
               │ HTTP REST API                 │ WebSocket
               │                               │ (Socket.IO)
┌──────────────▼───────────────────────────────▼───────────────┐
│               Node.js 20 + Express Backend                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  REST API Routes      │  Socket.IO Handler             │  │
│  │  - Projects           │  - Real-time Chat              │  │
│  │  - Manuscripts        │  - Review Streaming            │  │
│  │  - Characters         │  - Project Updates             │  │
│  │  - Plot Events        │  - Error Handling              │  │
│  │  - Export/Import      │                                │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Python Bridge Service (TypeScript)              │  │
│  │  - Subprocess Management                                │  │
│  │  - Command Execution                                    │  │
│  │  - Session Handling                                     │  │
│  │  - Event Streaming                                      │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────┬───────────────────────────────────────────────┘
               │ subprocess spawn + stdio pipes
┌──────────────▼───────────────────────────────────────────────┐
│                  Python CLI Backend                           │
│  ┌────────────────────────────────────────────────────────┐  │
│  │         Storybook CLI Application                       │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Web Integration Layer (NEW)                     │  │  │
│  │  │  - list_projects()                               │  │  │
│  │  │  - create/delete_project()                       │  │  │
│  │  │  - read/write_manuscript()                       │  │  │
│  │  │  - update_metadata()                             │  │  │
│  │  │  - export_project()                              │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  Existing CLI Components                         │  │  │
│  │  │  - ProjectManager                                │  │  │
│  │  │  - ChatSession + Claude Agent SDK                │  │  │
│  │  │  - LiteraryEditor                                │  │  │
│  │  │  - DocumentConverter                             │  │  │
│  │  │  - Custom MCP Tools (8 tools)                    │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────┬───────────────────────────────────────────────┘
               │ Anthropic API
┌──────────────▼───────────────────────────────────────────────┐
│                   Claude AI (Sonnet 4.5)                     │
│  - Natural Language Processing                                │
│  - Manuscript Analysis                                        │
│  - Character/Plot Tracking                                    │
│  - Literary Feedback                                          │
└──────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Prerequisites

- **Node.js 20+** and npm
- **Python 3.10+**
- **Anthropic API key** (get from https://console.anthropic.com)

### 2. Installation

```bash
# Clone or navigate to project
cd storybook-adk

# Install Python dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .

# Install Node.js dependencies
cd storybook-web
npm install

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the Application

```bash
# From storybook-web directory
npm run dev
```

This starts:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001

### 4. Access the Web UI

Open your browser to http://localhost:3000

## Key Features

### 1. Project Management
- ✅ Create new manuscript projects
- ✅ List all projects with metadata
- ✅ Delete projects with confirmation
- ✅ View project statistics (word count, characters, plot events)

### 2. Real-time Chat with AI
- ✅ Live conversation with Claude AI
- ✅ Streaming responses
- ✅ Thinking process visualization
- ✅ Tool usage indicators
- ✅ Markdown rendering
- ✅ Message history

### 3. Manuscript Editor
- ✅ Full-featured text editor
- ✅ Real-time word/character count
- ✅ Auto-save functionality
- ✅ Syntax highlighting for markdown

### 4. Character Tracking
- ✅ View all tracked characters
- ✅ Character descriptions and traits
- ✅ Aliases and first appearances
- ✅ Notes and development arcs

### 5. Plot Event Timeline
- ✅ View all plot events
- ✅ Importance levels (low, medium, high, critical)
- ✅ Chapter references
- ✅ Character involvement
- ✅ Sortable by importance

### 6. Metadata Management
- ✅ Edit title, author, genre
- ✅ Add manuscript notes
- ✅ View statistics (word count, chapters, dates)
- ✅ Real-time updates

### 7. Export Functionality
- ✅ Export to DOCX
- ✅ Export to Markdown
- ⏳ Export to PDF (planned)

### 8. Document Import
- ✅ Import DOCX files
- ✅ Import PDF files
- ✅ Import TXT/Markdown files
- ✅ Automatic conversion to markdown

## Technical Implementation

### Frontend (Next.js 14)

**Pages:**
- `/` - Project dashboard (list, create, delete)
- `/projects/[id]` - Project detail view with tabs

**Components:**
- `ChatPanel` - Real-time AI chat interface
- `EditorPanel` - Manuscript text editor
- `CharactersPanel` - Character tracking display
- `PlotEventsPanel` - Plot event timeline
- `MetadataPanel` - Project metadata editor

**Libraries:**
- `api.ts` - REST API client wrapper
- `socket.ts` - Socket.IO client manager
- `types.ts` - TypeScript type definitions

### Backend (Express + TypeScript)

**Routes:**
- `/api/projects` - Project CRUD operations
- `/api/chat` - Chat session management
- `/api/review` - Automated review endpoints

**Services:**
- `python-bridge.ts` - Python subprocess manager
- `socket.ts` - WebSocket event handlers
- `python_runner.py` - Python command executor
- `chat_bridge.py` - Real-time chat streaming
- `review_bridge.py` - Review progress streaming

### Python Integration

**New Module: `web_integration.py`**

Provides web-friendly functions:
- `list_projects()` → JSON array
- `load_project(id)` → JSON object
- `create_project(name)` → JSON object
- `delete_project(id)` → void
- `update_metadata(id, data)` → JSON object
- `read_manuscript(id)` → string
- `write_manuscript(id, content)` → void
- `export_project(id, format)` → file path

**Bridge Scripts:**
- `python_runner.py` - Execute functions and return JSON
- `chat_bridge.py` - Stream chat events via stdout
- `review_bridge.py` - Stream review progress via stdout

## Real-time Communication

### WebSocket Events

**Client → Server:**
```typescript
socket.emit('chat:send', { projectId, message });
socket.emit('review:start', { projectId, focusAreas });
socket.emit('project:subscribe', projectId);
```

**Server → Client:**
```typescript
socket.on('chat:message', (message) => { /* ... */ });
socket.on('chat:thinking', (thinking) => { /* ... */ });
socket.on('chat:tool', (tool) => { /* ... */ });
socket.on('review:progress', (progress) => { /* ... */ });
socket.on('review:complete', (review) => { /* ... */ });
```

## Data Flow Examples

### Example 1: Creating a Project

```
User clicks "Create Project"
  ↓
Frontend sends POST /api/projects
  ↓
Express backend receives request
  ↓
Python Bridge spawns subprocess
  ↓
Python executes: web_integration.create_project("My Novel")
  ↓
ProjectManager creates project directory and files
  ↓
Returns project JSON
  ↓
Express sends response to frontend
  ↓
Frontend redirects to /projects/{id}
```

### Example 2: Real-time Chat

```
User types message and clicks send
  ↓
Frontend emits socket event: chat:send
  ↓
Backend creates chat session subprocess
  ↓
Python chat_bridge.py starts listening
  ↓
User message sent via stdin
  ↓
Claude Agent SDK processes message
  ↓
Events streamed to stdout:
  - chat:thinking (AI is thinking)
  - chat:tool (using a tool)
  - chat:message (response chunk)
  ↓
Backend parses events and emits to frontend
  ↓
Frontend updates UI in real-time
```

### Example 3: Automated Review

```
User clicks "Start Review"
  ↓
Frontend emits: review:start
  ↓
Backend creates review session subprocess
  ↓
Python review_bridge.py starts
  ↓
LiteraryEditor analyzes manuscript
  ↓
Progress events streamed:
  - review:progress ("Analyzing plot...")
  - review:progress ("Checking characters...")
  - review:complete (full review object)
  ↓
Frontend displays progress bar and results
```

## File Structure

```
storybook-adk/
├── src/storybook/              # Python CLI
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── models.py               # Pydantic models
│   ├── project_manager.py      # Project CRUD
│   ├── chat.py                 # Chat sessions
│   ├── editor.py               # Literary editor
│   ├── tools.py                # MCP tools
│   ├── document_converter.py   # Import/export
│   ├── ui.py                   # Console UI
│   └── web_integration.py      # ⭐ NEW: Web API layer
│
├── storybook-web/              # Web application
│   ├── app/                    # Next.js app
│   │   ├── components/         # React components
│   │   ├── lib/               # Client libraries
│   │   ├── projects/          # Project pages
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   │
│   ├── server/                 # Express backend
│   │   ├── routes/            # API routes
│   │   │   ├── projects.ts
│   │   │   ├── chat.ts
│   │   │   └── review.ts
│   │   ├── services/          # Backend services
│   │   │   ├── python-bridge.ts      # ⭐ Python integration
│   │   │   ├── socket.ts             # ⭐ WebSocket handler
│   │   │   ├── python_runner.py      # ⭐ Python executor
│   │   │   ├── chat_bridge.py        # ⭐ Chat streaming
│   │   │   └── review_bridge.py      # ⭐ Review streaming
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── index.ts
│   │
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── .env.example
│   └── README.md
│
├── pyproject.toml
├── README.md
└── WEB_APP_README.md          # This file
```

## Configuration

### Environment Variables

Create `storybook-web/.env`:

```bash
# Frontend
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:3001

# Backend
PORT=3001
NODE_ENV=development

# Python
PYTHON_PATH=../.venv/bin/python

# AI
ANTHROPIC_API_KEY=your_actual_api_key_here
```

## Development Workflow

### Frontend Development

```bash
cd storybook-web
npm run dev:next
```

Hot reload enabled for React components and pages.

### Backend Development

```bash
cd storybook-web
npm run dev:server
```

Auto-restart enabled via `tsx watch`.

### Full Stack Development

```bash
cd storybook-web
npm run dev
```

Runs both frontend and backend concurrently.

## Troubleshooting

### Issue: Frontend can't connect to backend

**Solution:**
1. Check `.env` file has correct URLs
2. Verify backend is running on port 3001
3. Check browser console for CORS errors
4. Clear browser cache and restart

### Issue: Python commands fail

**Solution:**
1. Activate virtual environment: `source .venv/bin/activate`
2. Install CLI: `pip install -e .`
3. Test manually: `python -c "import storybook; print('OK')"`
4. Check Python path in backend logs

### Issue: WebSocket connection failed

**Solution:**
1. Check Socket.IO CORS settings in `server/index.ts`
2. Try polling transport: `?transport=polling`
3. Verify firewall allows port 3001
4. Check server logs for errors

### Issue: Chat not streaming

**Solution:**
1. Verify `ANTHROPIC_API_KEY` is set
2. Check Python bridge logs
3. Test CLI chat manually: `storybook`
4. Ensure proper Python environment

## Testing

### Manual Testing Checklist

- [ ] Create a new project
- [ ] View project list
- [ ] Open project detail page
- [ ] Send a chat message and receive response
- [ ] Edit manuscript content
- [ ] Save manuscript
- [ ] View characters panel
- [ ] View plot events panel
- [ ] Edit metadata
- [ ] Export to DOCX
- [ ] Delete project

### API Testing

```bash
# Test health endpoint
curl http://localhost:3001/health

# List projects
curl http://localhost:3001/api/projects

# Create project
curl -X POST http://localhost:3001/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Novel"}'
```

## Production Deployment

### Build

```bash
cd storybook-web
npm run build
```

### Run

```bash
npm start
```

### Docker (Optional)

Create `Dockerfile`:

```dockerfile
FROM node:20-alpine

# Install Python
RUN apk add --no-cache python3 py3-pip

# Setup app
WORKDIR /app
COPY . .

# Install dependencies
RUN cd storybook-web && npm install
RUN python -m pip install -e .

# Build frontend
RUN cd storybook-web && npm run build

# Expose ports
EXPOSE 3000 3001

# Start
CMD ["npm", "start", "--prefix", "storybook-web"]
```

## Performance Considerations

### Backend
- Subprocess pooling for frequent operations
- Connection pooling for database (if added)
- Rate limiting for API endpoints

### Frontend
- Code splitting via Next.js
- Lazy loading for components
- Debounced auto-save
- Virtualized lists for large datasets

### Real-time
- Heartbeat for connection health
- Automatic reconnection
- Message queuing during disconnects
- Binary transport for large payloads

## Security

### API Security
- [ ] Add authentication (JWT recommended)
- [ ] Validate all inputs
- [ ] Sanitize user content
- [ ] Rate limit endpoints
- [ ] HTTPS in production

### WebSocket Security
- [ ] Authenticate socket connections
- [ ] Validate event payloads
- [ ] Implement room-based permissions
- [ ] Monitor for abuse

## Future Enhancements

### Planned Features
- [ ] User authentication and multi-tenancy
- [ ] Real-time collaborative editing
- [ ] Chat history persistence
- [ ] Review history and comparisons
- [ ] Manuscript version control
- [ ] Advanced search and filtering
- [ ] Mobile responsive design
- [ ] Progressive Web App (PWA)
- [ ] Offline mode with sync
- [ ] AI model selection
- [ ] Custom system prompts
- [ ] Batch operations
- [ ] Analytics dashboard

### Technical Improvements
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Redis for caching
- [ ] Queue system for long operations
- [ ] Automated testing suite
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Error tracking (Sentry)
- [ ] Performance profiling

## Contributing

1. Follow TypeScript best practices
2. Add types for all functions
3. Handle errors gracefully
4. Test real-time features
5. Document new features
6. Follow existing code style

## License

MIT

## Support

For issues or questions:
1. Check documentation
2. Review error logs
3. Test CLI separately
4. Create detailed bug reports

---

**Built with Next.js 14, Express, TypeScript, and Claude AI**

**Integrates seamlessly with Storybook CLI for full-featured manuscript editing**
