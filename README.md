# GMACHIE - Agentic GTM Machine

An agentic Go-To-Market copilot that uses multiple specialized AI agents to plan, execute, and optimize GTM campaigns across channels autonomously.

## Architecture

### Layers
1. **Input & Context Layer** - Product info, ICP, goals
2. **Agent Orchestration Layer** - Multi-agent controller, task queue, state store
3. **Specialized GTM Agents** - Strategy, Research, Content, Channel, Analytics
4. **Tools & Integrations Layer** - APIs for socials, CRM, analytics

### Agents
- **Strategy Agent** - Creates GTM plan (personas, channels, messaging, KPIs)
- **Research Agent** - Audience insights, competitor analysis, trending topics
- **Content Agent** - Generates channel-specific content (posts, emails, ads)
- **Channel Agents** - Execute campaigns (X/Twitter, LinkedIn, Email)
- **Analytics Agent** - Measure performance and adapt strategy

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (TypeScript + Tailwind)
- **Database**: SQLite (for demo) / Postgres (production)
- **LLM**: Anthropic Claude (via existing free-claude-code proxy)
- **State**: Redis-like in-memory store

## Quick Start

### Backend
```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Backend on Render
This repo includes `render.yaml`, `requirements.txt`, and `.python-version`.

Use these settings if configuring the existing Render service manually:
```bash
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
Python Version: 3.13.13
```

Set these Render environment variables:
```bash
CORS_ORIGINS=https://your-vercel-app.vercel.app
CONVEX_BASE_URL=<your-convex-http-url>
CONVEX_AUTH_TOKEN=<your-convex-token>
IRONLABS_API_KEY=<your-ironlabs-key>
IRONLABS_BASE_URL=https://api.ironlabs.ai/v1
IRONLABS_MODEL=claude-3-opus
REAL_MODE=false
```

### Frontend on Vercel
This repo includes `vercel.json`, so Vercel can deploy the `frontend` app from the monorepo root.

Vercel commands:
```bash
Install Command: cd frontend && npm install
Build Command: cd frontend && npm run build
Output Directory: frontend/.next
```

Set this Vercel environment variable:
```bash
NEXT_PUBLIC_API_URL=https://your-render-service.onrender.com
```
The same value is also committed in `frontend/.env.production` for this deployment:
```bash
NEXT_PUBLIC_API_URL=https://gmachie.onrender.com
```

## Demo
See `scripts/run_demo.py` for automated demo that runs the full GTM loop.

## Project Structure
```
GMACHIE/
├── backend/
│   ├── agents/          # Agent implementations
│   ├── api/            # FastAPI routes
│   ├── core/           # Orchestrator, state management
│   ├── data/           # Models and database
│   ├── integrations/   # Social/email API clients (mocked for demo)
│   └── main.py
├── frontend/
│   ├── src/
│   ├── pages/
│   └── components/
├── data/               # Sample data, demo content
└── scripts/            # Demo and utility scripts
```
