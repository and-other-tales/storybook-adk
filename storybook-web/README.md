# Storybook Web

Web interface for Storybook AI-powered manuscript editor.

## Overview

This is a full-stack web application that provides a modern, real-time interface to control the Storybook CLI application. It features:

- **Next.js 14** frontend with React 18+
- **Node.js 20** backend with Express and TypeScript
- **Real-time communication** via Socket.IO
- **Python integration** bridge to Storybook CLI
- **Claude Agent SDK** integration with context store and custom tools

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                         │
│              (React 18, Tailwind CSS)                       │
│   - Project Management UI                                   │
│   - Real-time Chat Interface                                │
│   - Manuscript Editor                                        │
│   - Character & Plot Tracking                               │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST + WebSocket
┌────────────────────▼────────────────────────────────────────┐
│              Express Backend (TypeScript)                    │
│   - REST API Routes                                         │
│   - Socket.IO Real-time Server                              │
│   - Python Bridge Service                                   │
└────────────────────┬────────────────────────────────────────┘
                     │ subprocess + stdin/stdout
┌────────────────────▼────────────────────────────────────────┐
│              Python CLI (Storybook)                         │
│   - Project Manager                                         │
│   - Claude Agent SDK Integration                            │
│   - Document Converter                                      │
│   - Custom MCP Tools                                        │
│   - Literary Editor                                         │
└─────────────────────────────────────────────────────────────┘
```

## Features

### Real-time Chat
- Live conversation with Claude AI
- Streaming responses with thinking indicators
- Tool usage visualization
- Markdown rendering

### Project Management
- Create, edit, and delete projects
- Import manuscripts (DOCX, PDF, TXT, MD)
- Export to multiple formats
- Metadata management

### Manuscript Editor
- Full-featured text editor
- Real-time word count
- Auto-save functionality
- Syntax highlighting

### Character & Plot Tracking
- View tracked characters with traits and descriptions
- Plot event timeline
- Importance levels and chapter references

## Prerequisites

- Node.js 20+
- Python 3.10+
- Anthropic API key

## Installation

### 1. Install Dependencies

```bash
cd storybook-web
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_api_key_here
```

### 3. Ensure Python Environment

The web app uses the Python virtual environment from the main project:

```bash
# From project root
cd ..
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Development

Run both the Next.js dev server and the Express backend:

```bash
npm run dev
```

This starts:
- Next.js frontend at http://localhost:3000
- Express API server at http://localhost:3001

### Separate Commands

```bash
# Frontend only
npm run dev:next

# Backend only
npm run dev:server
```

## Production Build

```bash
# Build both frontend and backend
npm run build

# Start production servers
npm start
```

## API Endpoints

### REST API

- `GET /api/projects` - List all projects
- `POST /api/projects` - Create new project
- `GET /api/projects/:id` - Get project details
- `PUT /api/projects/:id/metadata` - Update metadata
- `DELETE /api/projects/:id` - Delete project
- `GET /api/projects/:id/manuscript` - Get manuscript content
- `PUT /api/projects/:id/manuscript` - Update manuscript
- `GET /api/projects/:id/characters` - Get characters
- `GET /api/projects/:id/plot-events` - Get plot events
- `POST /api/projects/:id/export` - Export project

### WebSocket Events

**Client to Server:**
- `project:subscribe` - Subscribe to project updates
- `project:unsubscribe` - Unsubscribe from project
- `chat:send` - Send chat message
- `review:start` - Start automated review

**Server to Client:**
- `chat:message` - Chat message received
- `chat:thinking` - AI thinking process
- `chat:tool` - Tool being used
- `chat:complete` - Chat turn complete
- `review:progress` - Review progress update
- `review:complete` - Review complete
- `project:updated` - Project data changed
- `error` - Error occurred

## Project Structure

```
storybook-web/
├── app/                    # Next.js app directory
│   ├── components/        # React components
│   │   ├── ChatPanel.tsx
│   │   ├── EditorPanel.tsx
│   │   ├── CharactersPanel.tsx
│   │   ├── PlotEventsPanel.tsx
│   │   └── MetadataPanel.tsx
│   ├── lib/               # Client libraries
│   │   ├── api.ts         # REST API client
│   │   ├── socket.ts      # Socket.IO client
│   │   └── types.ts       # TypeScript types
│   ├── projects/          # Project pages
│   │   └── [id]/page.tsx  # Project detail page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── server/                # Express backend
│   ├── routes/           # API routes
│   │   ├── projects.ts
│   │   ├── chat.ts
│   │   └── review.ts
│   ├── services/         # Backend services
│   │   ├── python-bridge.ts     # Python CLI bridge
│   │   ├── socket.ts            # Socket.IO handler
│   │   ├── python_runner.py    # Python command runner
│   │   ├── chat_bridge.py      # Chat streaming
│   │   └── review_bridge.py    # Review streaming
│   ├── types/            # TypeScript types
│   │   └── index.ts
│   └── index.ts          # Server entry point
├── public/               # Static assets
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.ts
```

## Technology Stack

### Frontend
- **Next.js 14** - React framework
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Socket.IO Client** - Real-time communication
- **React Markdown** - Markdown rendering
- **Lucide React** - Icons

### Backend
- **Express** - Web server
- **Socket.IO** - WebSocket server
- **TypeScript** - Type safety
- **Node.js 20** - Runtime

### Integration
- **Python 3.10+** - CLI backend
- **Claude Agent SDK** - AI integration
- **Pydantic** - Data validation

## Troubleshooting

### Connection Issues

If the frontend can't connect to the backend:

1. Check that both servers are running
2. Verify `.env` file has correct URLs
3. Check browser console for CORS errors
4. Ensure port 3001 is not in use

### Python Integration Issues

If Python commands fail:

1. Verify virtual environment is activated
2. Check Python path in environment
3. Ensure Storybook CLI is installed: `pip install -e .`
4. Test CLI manually: `storybook`

### WebSocket Connection Failed

1. Check server logs for errors
2. Verify Socket.IO CORS configuration
3. Try different transport: add `?transport=polling` to URL
4. Check firewall settings

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- Next.js automatically reloads on file changes
- `tsx watch` restarts backend on changes

### Debugging

Enable verbose logging:

```typescript
// In server/index.ts
console.log('Detailed logging:', data);
```

### Testing

```bash
# Type checking
npm run type-check

# Linting
npm run lint
```

## Contributing

1. Follow TypeScript best practices
2. Use async/await for asynchronous code
3. Handle errors gracefully
4. Add types for all functions
5. Test real-time features thoroughly

## License

MIT - See LICENSE file

## Support

For issues or questions:
1. Check existing documentation
2. Review error logs
3. Test CLI functionality separately
4. Create detailed bug reports

---

**Built with Next.js, Express, and Claude AI**
