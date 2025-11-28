from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import extract_info_node, chatbot_node

workflow = StateGraph(AgentState)

# Définition des noeuds
workflow.add_node("extract", extract_info_node)
workflow.add_node("respond", chatbot_node)

# Flux : Start -> Extract -> Respond -> End (Attente input user)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "respond")
workflow.add_edge("respond", END)

app = workflow.compile()