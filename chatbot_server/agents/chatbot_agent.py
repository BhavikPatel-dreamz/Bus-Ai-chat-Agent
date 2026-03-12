from services.llm import get_llm_summary
from services.memory import SessionMemory
from agents.intent_router import intent_route
from agents.inquiry_handler import handler_inquire
import json

from agents.agent import create_agent_for_search
from utils.print_msg import debug_print_messages


# Agents creation for the action/tool calling
agent = create_agent_for_search()

# Main entry point for handling a user message.
def handle_message(user_message : str, session):
    reply = None
   
    # convert state → readable text for LLM
    print("------------------------------------------------")
    history = session.get_history()
    # print(f"Past conversation : \n {history}")
    # print("------------------------------------------------")
    
    state = session.get_state()
    print(f"\n Currunt state:{state}")
    
    state_context = f"""
    Current session state (source of truth):
    {json.dumps(state, indent=2)}

    Use this state to decide what tool to call or what to ask next.
    Do NOT invent values.
    """


    messages = [
        {"role": "system", "content": state_context},
        *history,  # past messages
        {"role": "user", "content": user_message},
    ]

    
    result = agent.invoke({"messages": messages},
                          config={"configurable": {"session": session}})
    # print(f"\n response from result : {result}")
   
   
    debug_print_messages(result["messages"])
    
    
    # Final assistant reply
    reply = result["messages"][-1].content
    # print(f"\n response from tool : {reply}")
    
    
    # added history
    session.add_history("user",user_message)
    session.add_history("assistant",reply)  
    
    
    # update structured session state  
    session.state_update_from_llm(get_llm_summary())
    
    
    return reply
        