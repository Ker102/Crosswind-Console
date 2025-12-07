# Crosswind Console

![Status](https://img.shields.io/badge/Status-Beta_Release_Loading...-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Frontend](https://img.shields.io/badge/Frontend-Svelte_5_%2B_Vite-orange?style=for-the-badge&logo=svelte)
![Backend](https://img.shields.io/badge/Backend-FastAPI_%2B_Python-blue?style=for-the-badge&logo=fastapi)
![AI](https://img.shields.io/badge/AI-Multi--Agent_Orchestration-purple?style=for-the-badge&logo=google-gemini)

> **The High-Performance AI Orchestrator for the Modern Explorer.**
> A unified, immersive research dashboard that coordinates specialized AI agents to surface deep insights in Travel, Careers, and Social Trends.

---

## 🚀 Overview

**Crosswind Console** is a cutting-edge **AI Orchestration Platform** built for speed and depth. Unlike generic chatbots, Crosswind deploys **3 specialized AI Agents** (and growing) that work in tandem to solve complex research tasks.

Built on the blazing-fast combination of **FastAPI** and **Svelte 5**, the application offers a premium, glassmorphic interface that feels instant and alive. It solves information fragmentation by giving each agent access to **powerful, real-time tools**—from deep web scrapers to flight aggregators—allowing them to fetch opportunities that standard searches miss.

> **Status**: 🚧 Early Production / Beta Coming Soon

---

## 🧠 Core Capabilities: The 3-Agent System

Crosswind acts as a central brain, routing your intent to the expert agent best suited for the job.

### ✈️ 1. Travel Agent
*The Ultimate Trip Architect.*
*   **Accommodations**: Deep searches for **Airbnb** listings (via Apify) and hotels to find hidden gems and long-term stay deals.
*   **Flights**: Compares prices across **Skyscanner** and **Kiwi** simultaneously to ensure you get the absolute best fare.
*   **Ground Transport**: Unique "hybrid logic" that combines Google Search with deep scraping to find local bus and train routes (FlixBus, Rome2Rio).

### 💼 2. Jobs & Career Agent
*Your Personal Career Strategist.*
*   **Opportunity Scout**: Aggregates job listings from major platforms, filtered by your specific criteria.
*   **Resume Optimiztion**: analyzes your CV against target roles to maximize match potential.
*   **Market Analysis**: Scrapes company data to give you the edge in interviews.

### 📈 3. Trends Agent
*The Social Signal Decoder.*
*   **Viral Hunter**: Monitors **TikTok, Twitter, and Instagram** to spot rising trends before they peak.
*   **Cross-Platform Analysis**: Correlates data across platforms to validate true engagement.

### 🔮 Coming Soon: Stocks & Crypto Agent
*   **Market Watch**: Real-time analysis of financial markets and crypto assets.
*   **Sentiment Analysis**: Correlating news and social sentiment with price action.

---

## ⚡ Engineered for Performance

We refuse to compromise on speed or aesthetics.

*   **Frontend**: Built with **Svelte 5** and **Vite**, delivering an interface that is reactive, lightweight, and capable of rendering complex 3D visualizations (Three.js) without stutter.
*   **Backend**: **FastAPI** (Python) manages the orchestration layer, handling asynchronous tool execution and LLM streaming with millisecond latency.
*   **Tooling**: Powered by the **Model Context Protocol (MCP)**, connecting our agents to a vast ecosystem of external APIs and data sources securely.

---

## 💻 Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | Svelte 5, TypeScript, TailwindCSS | High-performance reactive UI |
| **3D Engine** | Three.js (Spline) | Immersive visual elements |
| **Backend** | Python, FastAPI, Uvicorn | Async task orchestration |
| **Intelligence** | Google Gemini Pro | Core reasoning engine |
| **Data Tools** | MCP, Apify, Firecrawl, Kiwi, Skyscanner | Real-time data fetching |
| **Infrastructure** | Docker | Containerized deployment |

---

## 🛠️ Getting Started (Dev)

### Prerequisites
*   Node.js & npm
*   Python 3.10+
*   Docker (Optional)

### 1. Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
uvicorn app.main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` to enter the console.

---

*Built with ❤️ by the Crosswind Team.*
