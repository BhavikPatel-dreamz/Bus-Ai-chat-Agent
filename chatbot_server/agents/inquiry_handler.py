import json
from services.llm import get_llm
from tools.search_bus import search_bus
from tools.get_all_stops import get_all_stops
from utils.formatter import format_bus_list
from services.memory import SessionMemory
from agents.prompts.prompt import INQUIRY_HANDLER_PROMPT
from datetime import date


def handler_inquire(user_message,session):
    intent = extract_params(user_message)
    print(f"response from extract-params: {intent}")
    if(intent["intent"] == "invalid_stop_query"):
        invalid_stop = (intent["params"])[invalid_stop]
        return f"{invalid_stop} is invalid stop.Please enter the valid stop."
    
    elif(intent["intent"] == "invalid_date_query"):
        invalid_date = intent["invalid_date"]
        return f"{invalid_date} is a past date. Please enter a valid travel date."
    
    elif(intent["intent"] == "search_bus"):
        payload = intent['params']
        # print(payload)
        apiResponse =  search_bus(payload)
        # print(apiResponse)
        
        return format_bus_list(apiResponse)
    

    else:
        return "Sorry ! I couldn't understand your query."

      

def extract_params(user_message):

    llm = get_llm()

    data = get_all_stops()
    stops = data["allstops"]
    # print(stops)

    TODAY = date.today().isoformat()

    prompt = [
        ("system", INQUIRY_HANDLER_PROMPT.format(TODAY = TODAY, user_message = user_message,stops = stops)),
        ("user", user_message)
    ]
    
    response = llm.invoke(prompt)
    content = json.loads(response.content)
    
    print("------------------------------------------------")
    print(f"Respnse from inquiry_handler's llm :\n {content}")
    print("------------------------------------------------")
    
    return content