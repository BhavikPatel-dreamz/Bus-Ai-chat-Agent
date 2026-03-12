import requests
from config import BACKEND_URL
from langchain_core.tools import tool
from services.memory import SessionMemory
from langchain_core.runnables import RunnableConfig

# def search_bus(payload: dict):
#     print(payload)
    
#     if(payload['traveldate'] !=  None):
#         return requests.post(
#             f"http://localhost:2026/api/user/search",
#             json=payload
#         ).json()
#     else:
#         del payload['traveldate']
#         return requests.post(
#             f"http://localhost:2026/api/ai/getbus",
#             json=payload
#         ).json()



@tool
def search_bus(from_city : str, to_city:str , traveldate: str | None , config: RunnableConfig ):
    
    """
    This is the ONLY tool allowed for bus search and bus availability queries.

    PURPOSE:
    - Fetch real bus availability information between two cities.
    - This tool must be used whenever the user intent is related to searching, listing,
    or checking buses on a route.

    PARAMETERS:
    - from_city (str):
        • Source city name.
        • Must be one of the valid cities already known to the system.
        • Must be in PascalCase (e.g., Surat, Ahmedabad)
    - to_city (str):
        • Destination city name.
        • Must be one of the valid cities already known to the system.
        • Must be in PascalCase (e.g., Mumbai, Vadodara)
    - traveldate (str | None):
        • Format: YYYY-MM-DD (ISO 8601), e.g., 2026-02-09
        • If provided → return buses only for that specific travel date.
        • If None → return all buses available on the given route (no date filtering).
        • When resolving traveldate:
            - Use today's_date strictly as the reference.
            - Do NOT add buffer days.
            - Never modify or shift dates by +1 day or for convenience.
        
    BEHAVIOR:
    - If date is provided:
        → Call POST /api/user/search    {from,to,traveldate}
        

    - If date is NOT provided (null or missing):
        → Call POST /api/ai/getbus  {from,to}
       

    STRICT TOOL USAGE RULES:
    - This tool MUST be used for all bus-related queries.
    - Do NOT answer bus queries manually.
    - Do NOT guess or assume missing values.
    - Do NOT call the tool if either from_city or to_city is missing.
    - If required parameters are missing:
        → Ask a clear follow-up question instead of calling the tool.

    """

    session = config["configurable"]["session"]

    payload= {
        "from" : from_city,
        "to" : to_city,
        "traveldate" : traveldate
    }
    session.set_state("from",payload["from"])
    session.set_state("to",payload["to"])
    
    if payload["traveldate"] != None:
        session.set_state("date" , payload["traveldate"])
  

    print(f"\n Payload from llm : {payload}")
    
    # with-date api calling
    if(payload['traveldate'] !=  None):
        search_bus_api_response= requests.post(
            f"{BACKEND_URL}/api/user/search",
            json=payload
        ).json()
    
    # without-date api calling
    else:
        del payload['traveldate']
        search_bus_api_response =requests.post(
            f"{BACKEND_URL}/api/ai/getbus",
            json=payload
        ).json()
    
    
    print(f"\n reply of search_bus_api:{search_bus_api_response}")
    
    buses = search_bus_api_response.get("buses", [])
    session.set_state("search_response", buses)
      
    return search_bus_api_response
       