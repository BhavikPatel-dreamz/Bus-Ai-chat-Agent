# QuickBus Assistant - AI-Powered Bus Search Backend

QuickBus Assistant is a Flask-based AI backend designed to provide a seamless, conversational interface for searching bus availability. It leverages LangChain, Google Gemini, and Llama 3.1 to understand user intent, extract search parameters (origin, destination, date), and interact with real-time bus search tools.

## 🚀 Features

- **Conversational Search**: Users can search for buses using natural language (e.g., "Find me a bus from Nairobi to Mombasa tomorrow").
- **Intent Routing & Parameter Extraction**: Automatically identifies search parameters and maintains context across multiple messages.
- **Real-Time Integration**: Uses a dedicated `search_bus` tool to fetch live availability.
- **Session Management**: Maintains conversation history and a structured "search state" for each user.
- **Dual-LLM Architecture**:
    - **Google Gemini**: Powers the primary agent for tool calling and user interaction.
    - **Llama 3.1 (via Groq/Ollama)**: Used for summarizing and updating the structured session state.

## 🛠️ Architecture Overview

1.  **Entry Point (`app.py` / `routes/chat.py`)**: Handles incoming POST requests to `/chat`.
2.  **Chatbot Agent (`agents/chatbot_agent.py`)**: The orchestrator that coordinates between memory, the LLM agent, and state updates.
3.  **LangChain Agent (`agents/agent.py`)**: Configured with a specialized system prompt and the `search_bus` tool.
4.  **Memory System (`services/memory.py`)**: Stores raw message history and extracted entities (origin, destination, date).
5.  **Tools (`tools/search_bus.py`)**: Functional components that the agent calls to perform external actions.

## 📋 Prerequisites

- Python 3.9 or higher
- [Google AI Studio API Key](https://aistudio.google.com/) (for Gemini)
- [Groq API Key](https://console.groq.com/) (for Llama 3.1)

## ⚙️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd chatbot_server
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   FLASK_PORT=5000
   ```

5. **Run the Server**
   ```bash
   python app.py
   ```
   The server will start on `http://localhost:5000`.

## 📡 API Usage

### Chat Endpoint
**URL**: `/chat`
**Method**: `POST`
**Body**:
```json
{
  "user_id": "unique_user_id_123",
  "message": "Are there any buses to Kisumu from Nairobi on Friday?"
}
```

**Response**:
```json
{
  "response": "I found 3 buses available from Nairobi to Kisumu on Friday, Oct 25th...",
  "status": "success"
}
```

## 🧪 Testing

To run the automated test suite:
```bash
pytest tests/
```

## 🛡️ Project Scope
The assistant is currently optimized for:
- Checking bus availability and schedules.
- Answering general inquiries about QuickBus services.
- *Note: This version does not handle bookings, payments, or user authentication.*
