from flask import Blueprint, request, jsonify
from agents.chatbot_agent import handle_message
from services.memory import get_session


chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"error": "session_id is required for per-client session management"}), 400

    # Retrieve or create a unique session for this specific client
    session = get_session(session_id)
    
    response = handle_message(user_message, session)

    return jsonify({"message": response})
