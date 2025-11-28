from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from app.state import AgentState
from app.nodes import extract_info_node, chatbot_node
from app.scoring import score_node

workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("extract", extract_info_node)
workflow.add_node("score", score_node)
workflow.add_node("respond", chatbot_node)

# Flux : Start -> Extract -> Score -> Respond -> End (Attente input user)
workflow.set_entry_point("extract")
workflow.add_edge("extract", "score")
workflow.add_edge("score", "respond")
workflow.add_edge("respond", END)

checkpointer = SqliteSaver.from_conn_string("sqlite:///checkpoints.db")
app = workflow.compile(checkpointer=checkpointer)