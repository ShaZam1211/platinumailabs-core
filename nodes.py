import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from state import AgentState
from database import query_property

# Load environment variables from .env file
load_dotenv()

# Initialize the standard enterprise intelligence engine
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# ==========================================
# STRUCTURAL COMPLIANCE SCHEMA FOR CRITIC
# ==========================================
class EvaluationResult(BaseModel):
    is_approved: bool = Field(description="True if the draft is 100% accurate based ONLY on the verified context. False if it contains unverified facts, amenities, or features.")
    feedback: str = Field(description="Detailed critique specifying what unverified claims were made if rejected, or empty string if approved.")

# Forces the model to respond STRICTLY according to our schema structure
structured_critic = llm.with_structured_output(EvaluationResult)

# ==========================================
# AGENT NODE DEFINITIONS
# ==========================================

def gateway_node(state: AgentState):
    print("\n[Node 1: Gateway] Interrogating dynamic database...")
    
    # Extract the contextual data matching the user input dynamically from SQLite
    db_context = query_property(state.raw_input)
    
    return {
        "parsed_intent": "Luxury Real Estate Purchase Inquiry",
        "data_context": db_context
    }

def executor_node(state: AgentState):
    print("[Node 2: Executor] Generating customized email response via LLM...")
    
    # Fully personalized corporate system parameters
    system_prompt = (
        "You are Sharan Menon, an elite luxury real estate concierge representing PlatinumAILabs in Mumbai.\n"
        "Task: Draft a premium, high-converting email response to the client's inquiry.\n\n"
        f"Client Inquiry: {state.raw_input}\n"
        f"Verified Database Context: {state.data_context}\n\n"
        "CRITICAL RULES:\n"
        "1. Rely ONLY on the facts explicitly stated in the database context.\n"
        "2. Do NOT invent amenities, features, or architectural details.\n"
        "3. ALWAYS sign off the email formally using exactly this signature block, with no placeholders:\n"
        "   Warm regards,\n\n"
        "   Sharan Menon\n"
        "   Elite Luxury Real Estate Concierge\n"
        "   PlatinumAILabs\n"
    )
    
    if state.critic_feedback:
        print("⚠️ Executor entering self-correction loop using critic feedback...")
        system_prompt += f"\n\n🛑 REJECTION FEEDBACK FROM CRITIC:\n{state.critic_feedback}\nModify the response to remove the flagged error immediately."
    else:
        # TRAP: Forcing a hallucination on the first pass to test our engine
        system_prompt += "\nSpecial Note for this initial draft: Mention that it includes an infinity pool on the terrace."

    response = llm.invoke(system_prompt)
    
    return {
        "generated_output": response.content
    }

def critic_node(state: AgentState):
    print("[Node 3: Critic] Executing structural compliance check...")
    
    critic_prompt = (
        "You are a strict real estate regulatory auditor.\n"
        "Compare the generated draft against the verified database context to spot fabrications or assumptions.\n\n"
        f"Verified Database Context: {state.data_context}\n"
        f"Generated Draft: {state.generated_output}\n\n"
        "Check: Is every statement in the draft supported by the database context? "
        "If they invented features like pools, views, or high-ceilings not listed, reject it."
    )
    
    result = structured_critic.invoke(critic_prompt)
    
    if not result.is_approved:
        print(f"❌ CRITIC ALARM: Draft Rejected!\nReason: {result.feedback}")
        return {
            "critic_feedback": result.feedback,
            "routing_decision": "retry"
        }
    
    print("✅ CRITIC APPROVED: Draft matches database facts flawlessly.")
    return {
        "routing_decision": "approve",
        "critic_feedback": ""
    }