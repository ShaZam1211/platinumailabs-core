from pydantic import BaseModel, Field

class AgentState(BaseModel):
    raw_input: str = Field(description="The unstructured inbound lead string")
    parsed_intent: str = Field(default="", description="The prioritized target workflow category")
    data_context: str = Field(default="", description="Ground truth pulled via MCP")
    generated_output: str = Field(default="", description="The generated response draft")
    critic_feedback: str = Field(default="", description="Hallucination or formatting feedback")
    routing_decision: str = Field(default="review", description="Next node direction flag")