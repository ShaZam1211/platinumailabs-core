from typing import Literal
from state import AgentState

def evaluation_router(state: AgentState) -> Literal["executor", "__end__"]:
    if state.routing_decision == "retry":
        print("🔄 Routing back to Executor for self-correction...")
        return "executor"
    print("🚀 Passing to Human Approval Dashboard.")
    return "__end__"