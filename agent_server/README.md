# TripMate - Intelligent Bus Booking Agent

TripMate is a sophisticated AI-powered bus booking assistant built with **Flask**, **LangChain**, and **Google Gemini**. It allows users to search for buses, check seat availability, book tickets, and complete payments through a natural language interface.

## 🚀 Features

- **Natural Language Interaction:** Chat naturally to find and book bus tickets.
- **Intelligent Tool Routing:** Automatically invokes backend APIs for real-time data.
- **Session State Management:** maintains context across conversations, including passenger details and selected trips.
- **Secure Integration:** Uses JWT-based authentication for sensitive operations like booking and payments.
- **Multi-LLM Architecture:** Uses Google Gemini for agent reasoning and Llama 3.1 (via Hugging Face) for state extraction.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI Framework:** LangChain
- **LLMs:** 
  - **Google Gemini 1.5 Flash:** Core agent logic and tool calling.
  - **Llama 3.1 8B (via Hugging Face):** State extraction and conversation summarization.
- **API Integration:** Requests, HTTPX
- **Environment Management:** Python-dotenv

## 📂 Project Structure

```text
agent_server/
├── app.py                # Flask entry point
├── config.py             # Global configurations & Environment variables
├── agent/
│   ├── agent.py          # Agent definition & System prompts
│   ├── executor.py       # Message handling logic
│   └── prompts/          # Specialized prompts (e.g., State extraction)
├── routes/
│   └── chat.py           # Chat & Health API endpoints
├── services/
│   ├── llm.py            # LLM provider configurations
│   ├── session.py        # In-memory session & state management
│   └── key_manager.py    # Rotation logic for API keys
├── tools/
│   ├── search_bus.py     # Bus search tool
│   ├── seats.py          # Seat availability tool
│   ├── create_ticket.py  # Ticket booking tool
│   ├── payment.py        # Payment completion tool
│   └── base.py           # Shared HTTP utilities for tools
└── utils/                # Helper functions (Email validation, logging, etc.)
```

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.10+
- A Google AI Studio API Key (Gemini)
- A Hugging Face Token (for Llama 3.1 state extraction)

### 2. Clone the Repository
```bash
git clone <repository-url>
cd agent_server
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Create a `.env` file in the root directory and add the following:

```env
FLASK_PORT=8000
BASE_URL=http://your-bus-api-url/api
GOOGLE_API_KEYS=your_gemini_key_1,your_gemini_key_2
HF_TOKEN=your_huggingface_token
```

### 6. Run the Server
```bash
python app.py
```
The server will start on `http://127.0.0.1:8000`.

## 💬 API Usage

### Chat Endpoint
**POST** `/chat`

**Payload:**
```json
{
  "session_id": "unique-user-id",
  "message": "I want to go from Delhi to Mumbai tomorrow",
  "access_token": "your-jwt-auth-token"
}
```

**Response:**
```json
{
  "reply": "I found several buses for your trip from Delhi to Mumbai on 2026-03-13. Would you like to see the available seats for a specific bus?"
}
```

## 🔄 Booking Workflow

1. **Search:** User provides source, destination, and date. Agent calls `search_bus`.
2. **Select & Check Seats:** User selects a bus. Agent calls `get_all_seats`.
3. **Provide Details:** User provides passenger names and seat numbers.
4. **Create Ticket:** Agent validates data and calls `create_ticket`.
5. **Payment:** User confirms payment. Agent calls `complete_ticket_payment`.

## 🛡️ Key Management
The system includes a `key_manager.py` that supports rotation of multiple Google API keys to handle rate limits effectively in a production-like environment.
