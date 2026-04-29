#Tracks Player Progression.

def create_initial_state():
    return {
        "world":"Space-Horror",
        "current_node":"intro",
        "visited":[],
        "fear":0,
        "confidence":50
        }


#State as defined above LOL.
def update_state(state,next_node):
    state["visited"].append(state["current_node"])
    state["current_node"]=next_node
    if next_node in ["trap","locked exit"]:
        state["fear"]+=10
        state["confidence"]-=3
    if next_node in ["investigate","talk"]:
        state["fear"]-=2
        state["confidence"]+=3

    return state
        

