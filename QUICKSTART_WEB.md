# Storybook Web - Quick Start Guide

Get the web application running in 5 minutes!

## Prerequisites

- Node.js 20+
- Python 3.10+
- Anthropic API key

## Installation

### Option 1: Automated Setup (Recommended)

```bash
cd storybook-web
./setup.sh
```

This will:
- Check Node.js and Python versions
- Install all dependencies
- Create .env file
- Set up Python environment

### Option 2: Manual Setup

```bash
# 1. Install Node dependencies
cd storybook-web
npm install

# 2. Setup Python environment
cd ..
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .

# 3. Configure environment
cd storybook-web
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Configure API Key

Edit `storybook-web/.env`:

```bash
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Get your key from: https://console.anthropic.com

## Run the Application

```bash
cd storybook-web
npm run dev
```

This starts:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:3001

## First Steps

1. **Open your browser** to http://localhost:3000
2. **Create a project** - Click "New Project"
3. **Start chatting** - Go to "Chat with AI" tab
4. **Edit manuscript** - Switch to "Manuscript" tab
5. **Track progress** - View "Characters" and "Plot Events"

## Features

### Real-time Chat
Chat with Claude AI to get manuscript feedback, editing suggestions, and creative ideas.

### Manuscript Editor
Edit your manuscript directly in the browser with real-time word count and auto-save.

### Character Tracking
View all characters mentioned in your manuscript with their descriptions, traits, and appearances.

### Plot Events
Track major plot points, their importance, and which characters are involved.

### Export
Export your manuscript to DOCX or Markdown format.

## Troubleshooting

### Can't connect to server
- Make sure both servers are running: `npm run dev`
- Check that port 3001 is not in use
- Verify `.env` has correct URLs

### Python errors
- Activate virtual environment: `source ../.venv/bin/activate`
- Reinstall CLI: `pip install -e ..`
- Test manually: `storybook`

### API key errors
- Verify `ANTHROPIC_API_KEY` is set in `.env`
- Check key is valid at https://console.anthropic.com
- Restart server after changing `.env`

## Development Commands

```bash
# Run both frontend and backend
npm run dev

# Run frontend only
npm run dev:next

# Run backend only
npm run dev:server

# Build for production
npm run build

# Start production server
npm start

# Type checking
npm run type-check

# Linting
npm run lint
```

## Project Structure

```
storybook-web/
├── app/              # Next.js frontend
│   ├── components/   # React components
│   ├── lib/         # Client libraries
│   └── projects/    # Project pages
├── server/          # Express backend
│   ├── routes/      # API routes
│   ├── services/    # Backend services
│   └── types/       # TypeScript types
└── public/          # Static files
```

## Next Steps

- Read [WEB_APP_README.md](../WEB_APP_README.md) for complete architecture
- Check [README.md](./README.md) for detailed API documentation
- Explore the code to understand the real-time communication
- Customize the UI to fit your needs

## Support

Need help?
1. Check the documentation files
2. Review the error logs
3. Test CLI functionality: `storybook`
4. Check console for detailed errors

---

**Happy writing! ✍️**
