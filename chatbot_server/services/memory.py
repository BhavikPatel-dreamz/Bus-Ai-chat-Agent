import json
from agents.prompts.prompt import STATE_EXRACT_PROMPT
from datetime import date

# Dictionary to store per-client sessions: session_id -> SessionMemory instance
sessions = {}

def get_session(session_id: str) -> 'SessionMemory':
    """Retrieve an existing session or create a new one for the given session_id."""
    if session_id not in sessions:
        sessions[session_id] = SessionMemory()
    return sessions[session_id]

class SessionMemory:
    def __init__(self, max_pairs=10):
        # max_pairs = number of user–assistant pairs to keep
        self.max_messages = max_pairs * 2
        self.history = []
        self.state = {
            "today's_date" : str(date.today()),
            "today's_day": date.today().strftime("%A"),
            "from": None,
            "to": None,
            "traveldate": None,
            "search_response" : []
        }

    def add_history(self, role, message):
    
        self.history.append({
            "role": role,
            "content": message
        })

        # Trim oldest messages if limit exceeded (FIFO)
        if len(self.history) > self.max_messages:
            excess = len(self.history) - self.max_messages
            self.history = self.history[excess:]

    def get_history(self):
        return self.history
        # formatted_history = []

        # for turn in self.history:
        #     role = turn.get("role", "unknown")
        #     message = turn.get("message", "")
        #     formatted_history.append(f"{role}: {message}")

        # return "\n\n".join(formatted_history)

    # state memory (intent, params, etc.)
    def set_state(self, key, value):
        self.state[key] = value
        # print(type(state[key]))
     
    def extract_state_from_text(self, llm, history_text):
        prompt = STATE_EXRACT_PROMPT.format(history=history_text)

        resp = llm.invoke(prompt).content

        try:
            return json.loads(resp)
        except Exception:
            return {}   
    

    def state_update_from_llm(self, llm):

        history_text = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in self.history
        )

        extracted = self.extract_state_from_text(llm, history_text)

        print(f"Extracted Params by LLM from state update function: {extracted}")

        for k, v in extracted.items():
            if v is not None:
                self.set_state(k, v)
    
    def get_state(self):
        return self.state

    def clear(self):
        self.history.clear()
        self.state.clear()
    
    
    
# =======================================================================

# function based session handling:

# import json
# from agents.prompts.prompt import STATE_EXRACT_PROMPT


# # --------------------------------------------------
# # Session creation
# # --------------------------------------------------
# def create_session(max_pairs=10):
#     return {
#         "max_messages": max_pairs * 2,
#         "history": [],
#         "state": {
#             "from": None,
#             "to": None,
#             "date": None,
#         }
#     }


# # --------------------------------------------------
# # History handling
# # --------------------------------------------------
# def add_history(session, role, message):
#     session["history"].append({
#         "role": role,
#         "message": message
#     })

#     # Trim oldest messages if limit exceeded (FIFO)
#     if len(session["history"]) > session["max_messages"]:
#         excess = len(session["history"]) - session["max_messages"]
#         session["history"] = session["history"][excess:]


# def get_history(session):
#     formatted_history = []

#     for turn in session["history"]:
#         role = turn.get("role", "unknown")
#         message = turn.get("message", "")
#         formatted_history.append(f"{role}: {message}")

#     return "\n\n".join(formatted_history)


# # --------------------------------------------------
# # State handling
# # --------------------------------------------------
# def set_state(session, key, value):
#     session["state"][key] = value


# def get_state(session, key, default=None):
#     return session["state"].get(key, default)


# def clear_session(session):
#     session["history"].clear()
#     session["state"] = {
#         "from": None,
#         "to": None,
#         "date": None,
#     }


# # --------------------------------------------------
# # LLM-based state extraction
# # --------------------------------------------------
# def extract_state_from_text(llm, history_text):
#     prompt = STATE_EXRACT_PROMPT.format(history=history_text)

#     resp = llm.invoke(prompt).content

#     try:
#         return json.loads(resp)
#     except Exception:
#         return {}


# def state_update_from_llm(llm, session):
#     history_text = "\n".join(
#         f"{m['role']}: {m['message']}"
#         for m in session["history"]
#     )

#     extracted = extract_state_from_text(llm, history_text)

#     print(f"Extracted Params by LLM : {extracted}")

#     for k, v in extracted.items():
#         if v is not None:
#             set_state(session, k, v)
