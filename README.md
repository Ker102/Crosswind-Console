# Crosswind Console

![Status](https://img.shields.io/badge/Status-Beta_Release-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-Svelte_5_%2B_Vite-orange?style=for-the-badge&logo=svelte)
![Backend](https://img.shields.io/badge/Backend-FastAPI_%2B_LangChain-blue?style=for-the-badge&logo=fastapi)
![AI](https://img.shields.io/badge/AI-Gemini_2.0_%2B_RAG-purple?style=for-the-badge&logo=google-gemini)

> **The High-Performance AI Orchestrator for the Modern Explorer.**
> A unified, immersive research dashboard that coordinates specialized specialized AI Agents to surface deep insights in Travel, Careers, and Social Trends. 

---

## 🚀 Overview

**Crosswind Console** is a next-generation **AI Orchestration Platform** built for speed, depth, and precision. It leverages **LangChain 1.x** and **Google Gemini 2.0** to coordinate a fleet of specialized agents that can "think" and "act" using real-time tools.

Unlike generic chatbots, Crosswind uses a **Hybrid RAG + MCP Architecture**:
1.  **RAG (Retrieval-Augmented Generation)**: Injects deep domain knowledge (API manuals, travel guides) into the AI's context.
2.  **MCP (Model Context Protocol)**: Connects the AI to 120+ real-time tools (Amadeus, Flights Sky, Booking.com) via a persistent, high-performance connection pool.

> **Performance Upgrade (Jan 2026)**: Now featuring a custom HTTP MCP client that reduces tool execution latency from **60s to <3s**.

---

## 🧠 Core Capabilities: The 3-Agent System

### ✈️ 1. Travel Agent (Amadeus + Sky)
*The Ultimate Trip Architect.*
*   **Smart Search**: Uses **Amadeus GDS** and **Skyscanner** to find real-time flight availability and pricing.
*   **Hotel Intelligence**: Cross-references **Amadeus Hotels** and **Booking.com** for best rates.
*   **Deep Reasoning**: Understands complex queries like *"Find a cheap flight to Paris that lands before noon and a hotel near the Eiffel Tower with a pool."*

### 💼 2. Jobs & Career Agent
*Your Personal Career Strategist.*
*   **Opportunity Scout**: Aggregates job listings from major platforms filtered by your specific criteria.
*   **Market Analysis**: Scrapes company data to give you the competitive edge.

### 📈 3. Trends Agent
*The Social Signal Decoder.*
*   **Viral Hunter**: Monitors social platforms to spot rising trends before they peak.
*   **Cross-Platform Analysis**: Correlates data to validate true engagement.

---

## ⚡ Engineered for Speed

*   **Frontend**: **Svelte 5 (Runes)** + **Vite** for an instant, reactive glassmorphic UI.
*   **Backend**: **FastAPI** + **LangChain** for robust agent orchestration.
*   **Data Layer**: **Supabase pgvector** for high-speed RAG retrieval.
*   **Tooling**: **Persistent MCP Client** (Python httpx) for lightning-fast API interaction.

---

## 💻 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Svelte 5, TypeScript, TailwindCSS | High-performance reactive UI |
| **Orchestration** | **LangChain 1.x** | Agent state & tool binding |
| **Intelligence** | **Google Gemini 2.0 Flash** | Core reasoning engine |
| **API Integration** | **FastAPI** + **MCP** | Tool serving & execution |
| **Knowledge Base** | **Supabase pgvector** | RAG context retrieval |
| **Travel APIs** | Amadeus, Skyscanner, Booking.com | Real-time global data |

---

## 🛠️ Getting Started (Dev)

### Prerequisites
*   Node.js & npm
*   Python 3.10+
*   Amadeus / RapidAPI Keys (in `.env`)

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` to launch the console.

---

*Built with ❤️ by the Crosswind Team.*
