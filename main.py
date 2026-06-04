from langgraph.graph import StateGraph, START, END
from state import AgentState
from nodes import gateway_node, executor_node, critic_node
from router import evaluation_router

# Build the workflow engine
workflow = StateGraph(AgentState)

# Register the architectural nodes
workflow.add_node("gateway", gateway_node)
workflow.add_node("executor", executor_node)
workflow.add_node("critic", critic_node)

# Construct the sequence
workflow.add_edge(START, "gateway")
workflow.add_edge("gateway", "executor")
workflow.add_edge("executor", "critic")

# Apply the conditional routing breakout
workflow.add_conditional_edges(
    "critic",
    evaluation_router,
    {
        "executor": "executor",
        "__end__": END
    }
)

engine = workflow.compile()

if __name__ == "__main__":
    initial_input = {"raw_input": "Hey, is that 3BHK apartment in Bandra West still available? Give me details."}
    print("--- RUNNING MODULAR CURSOR CORE ENGINE ---")
    final_state = engine.invoke(initial_input)
    
    print("\n🚀 FINAL APPROVED OUTPUT SENDER STATE:")
    print(final_state["generated_output"])