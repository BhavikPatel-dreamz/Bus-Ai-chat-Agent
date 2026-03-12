import json
from services.llm import get_llm
from agents.prompts.prompt import INTENT_CLASSIFIER


llm = get_llm()

def intent_route(user_message,session):
    
    history = session.get_history()

    prompt = [
    ("system", INTENT_CLASSIFIER.format(HISTORY = history, user_message = user_message)),
    ("user", user_message)
    ]
    
    response = llm.invoke(prompt)
    # print("RAW LLM OUTPUT:")
    # print(response.content)
    # content = json.loads(response.content)
    
    # # print(content)
    # return content
    
    raw = response.content
    print("------------------------------------------------")
    print("RAW LLM OUTPUT FROM intent_router :\n", raw)
    print("------------------------------------------------")

    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1 or end < start:
        print(("No valid JSON object found in LLM output"))
        return "You have entered invalid query."

    clean = raw[start:end+1]

    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        print("JSON PARSE ERROR:", e)
        print("CLEANED JSON:\n", clean)
        raise