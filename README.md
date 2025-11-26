# Crosswind Console

![Status](https://img.shields.io/badge/Status-Active_Development-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-Svelte_5_%2B_Vite-orange?style=for-the-badge&logo=svelte)
![Backend](https://img.shields.io/badge/Backend-FastAPI_%2B_Python-blue?style=for-the-badge&logo=fastapi)
![AI](https://img.shields.io/badge/AI-Intelligent_Orchestration-purple?style=for-the-badge&logo=google-gemini)

> **Intelligent Orchestration for the Modern Explorer.**
> A unified research dashboard that blends immersive 3D aesthetics with powerful AI agents to surface opportunities in Travel, Jobs, and Social Trends.

---

## 🚀 Overview

**Crosswind Console** is not just a dashboard; it's an **AI-driven orchestrator**. It solves the problem of information fragmentation by deploying specialized agents to scour the web, analyze data, and present actionable insights in a single, cohesive interface.

Whether you're looking for the cheapest flight to Tokyo, the next big career move, or a viral trend before it peaks, Crosswind Console coordinates the complex work of data gathering and reasoning behind the scenes, delivering results through a stunning, glassmorphic UI.

---

## ✨ Key Capabilities

### 🧠 Intelligent Orchestration
At its core, the system uses advanced **LLM Reasoning** to understand user intent. It doesn't just search; it *plans*.
*   **Context-Aware**: Understands "Find me a trip to Paris" vs. "Find me a tech job in Paris".
*   **Tool Chaining**: Automatically selects the right tools (Search, Scrapers, APIs) to fulfill a request.

### 🌍 Multi-Modal Travel Agent
A next-generation travel assistant that goes beyond simple flight search.
*   **Hybrid Ground Transport Engine**: Combines **Google Search** discovery with **Firecrawl** deep scraping to find bus and train routes (FlixBus, Rome2Rio) that standard APIs miss.
*   **Fallback Reliability**: Automatically switches to the **Kiwi API** for standard routes if scraping fails, ensuring you never get a "no results" error.
*   **Flight Discovery**: Real-time flight pricing and route analysis.

### 💼 Career & Trend Agents
*   **Jobs Agent**: Aggregates opportunities from major platforms, filtering by relevance and potential.
*   **Trends Agent**: Monitors social signals to identify rising topics and viral content.

### 🎨 Immersive Experience
*   **Dynamic Island Navigation**: A sleek, iOS-inspired navigation bar that expands and adapts to your context.
*   **3D Visuals**: Interactive 3D elements (Icon Cloud) powered by Three.js for a premium feel.
*   **Glassmorphism**: A modern, translucent design language that feels alive.

---

## 🛠️ How It Works

The architecture is built for speed, modularity, and intelligence.

1.  **The Interface (Frontend)**:
    *   Built with **Svelte 5** and **Vite** for blazing fast performance.
    *   Handles user interactions and renders the immersive 3D environment.
    *   Communicates with the backend via typed API contracts.

2.  **The Brain (Backend)**:
    *   Powered by **FastAPI (Python)**.
    *   Acts as the central coordinator, receiving user prompts and dispatching them to the appropriate agents.

3.  **The Tools (MCP Servers)**:
    *   We use the **Model Context Protocol (MCP)** to standardize how the AI interacts with external tools.
    *   **Travel Server**: Handles flight/ground transport logic (Search + Scrape).
    *   **Trends/Jobs Servers**: Specialized connectors for their respective domains.
    *   **Docker Gateway**: Manages these tools securely and efficiently.

---

## 💻 Tech Stack

*   **Frontend**: Svelte, TypeScript, TailwindCSS, Three.js
*   **Backend**: Python, FastAPI, Uvicorn
*   **Data & AI**: Model Context Protocol (MCP), Firecrawl, Playwright, Google Custom Search, RapidAPI
*   **Infrastructure**: Docker

---

## ⚡ Getting Started

### Prerequisites
*   Node.js & npm
*   Python 3.10+
*   Docker (optional, for MCP Gateway)

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
# Activate virtual env (Windows: .venv\Scripts\activate, Mac/Linux: source .venv/bin/activate)
pip install -e .
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` to launch the console.

### 3. MCP Servers (Optional)
To enable full AI capabilities, ensure your `.env` file is configured with necessary API keys (`RAPIDAPI_KEY`, `GOOGLE_SEARCH_CX`, etc.) and run the specific server scripts in `mcp/`.

---

*Built with ❤️ by the Crosswind Team.*
