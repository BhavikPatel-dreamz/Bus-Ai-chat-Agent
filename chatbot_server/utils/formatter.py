from services.llm import get_llm
from tools.search_bus import search_bus
from agents.prompts.prompt import FORMATTER_PROMPT
import json

llm = get_llm()

def format_bus_list(data):
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    buses = data.get("buses", [])
    
    if not buses:
        return "No buses found for your route."

    # print(prompt)
    response = llm.invoke(FORMATTER_PROMPT.format(buses = buses)).content
    print("------------------------------------------------")
    print(f"Response from Formatter's llm :\n {response}")
    print("------------------------------------------------")
    return response
   
