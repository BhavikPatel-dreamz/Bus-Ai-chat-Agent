# Bus AI Chat Agent Ecosystem

An intelligent, multi-module bus travel assistant ecosystem powered by **Google Gemini**, **Llama 3.1**, and **LangChain**. This repository contains two specialized AI agents designed to handle different stages of the bus travel lifecycle: from initial inquiries and discovery to full-service booking and payment.

## Project Overview

This ecosystem is split into two primary backend services:

1.  **TripMate (agent_server):** A comprehensive, state-aware booking agent that guides users through searching, seat selection, ticket creation, and secure payment.
2.  **QuickBus Assistant (chatbot_server):** A specialized, read-only discovery agent focused on bus availability, route information, and general service inquiries.

---

## Architecture

Both modules leverage a modern AI stack:
- **Core Orchestration:** LangChain for agent reasoning and tool calling.
- **LLM Layer:** 
    - **Google Gemini 1.5 Flash:** Powers the primary conversational logic.
    - **Llama 3.1 (via Hugging Face/Groq):** Handles structured state extraction and conversation summarization.
- **Backend:** Flask (Python) with RESTful API endpoints.
- **State Management:** Sophisticated session-based memory that persists user intent and booking data across turns.

---

## Repository Structure

```text
Bus-Ai-chat-Agent/
├── agent_server/           # Full-service Booking Agent (TripMate)
│   ├── agent/              # Agent logic & system prompts
│   ├── tools/              # Booking, Seats, & Payment tools
│   ├── services/           # LLM config & Session management
│   └── routes/             # Flask API endpoints (/chat, /health)
├── chatbot_server/         # Search & Discovery Agent (QuickBus)
│   ├── agents/             # Intent-based search agent logic
│   ├── tools/              # Specialized search tools
│   └── services/           # Memory & State management
└── README.md               # Main project documentation
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- [Google AI Studio API Key](https://aistudio.google.com/) (Gemini)
- [Hugging Face Token](https://huggingface.co/settings/tokens) (for Llama 3.1)
- [Groq API Key](https://console.groq.com/) (Optional, for alternative Llama 3.1 hosting)
- [LangSmith API Key](https://smith.langchain.com/) (Optional, for tracing and debugging)

### 2. Installation

Clone the repository and set up virtual environments for both modules.

**For TripMate (agent_server):**
```bash
cd agent_server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**For QuickBus (chatbot_server):**
```bash
cd ../chatbot_server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration

Create a `.env` file in **both** `agent_server` and `chatbot_server` directories.

**agent_server/.env:**
```env
FLASK_PORT=8000
BASE_URL=http://your-backend-api-url/api
GOOGLE_API_KEYS=key1,key2  # Supports rotation
HF_TOKEN=your_huggingface_token

# LangSmith Configuration (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT="tripmate-agent"
```

**chatbot_server/.env:**
```env
FLASK_PORT=5050
BACKEND_URL=http://your-backend-api-url/api
GOOGLE_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key
HF_TOKEN=your_huggingface_token

# LangSmith Configuration (Optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT="quickbus-chatbot"
```

---

## Running the Services

### Start TripMate
```bash
cd agent_server
python app.py
```
*Accessible at: http://localhost:8000*

### Start QuickBus Assistant
```bash
cd chatbot_server
python app.py
```
*Accessible at: http://localhost:5050*

---

## API Usage

Both servers expose a `/chat` endpoint.

**Request Body:**
```json
{
  "session_id": "user_unique_id",
  "message": "Find buses from Delhi to Mumbai for tomorrow",
  "access_token": "optional_jwt_token" 
}
```

---

## Key Features & Observability
- **LangSmith Integration:** Full support for LangSmith tracing, allowing for deep inspection of agent reasoning, tool calls, and LLM latency.
- **Multi-LLM State Extraction:** Uses a secondary LLM to ensure the session state (origin, destination, date) is always synchronized with the conversation.
- **Tool Integrity:** Agents are strictly instructed to use tools as the single source of truth and never fabricate data.
- **Scope Enforcement:** QuickBus is architected to gracefully refuse booking/payment requests, ensuring a clear separation of concerns.
- **Key Rotation:** `agent_server` includes a `key_manager` to handle API rate limits by rotating through multiple Gemini keys.

