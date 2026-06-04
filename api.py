import re
from fastapi import FastAPI, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import engine

# Initialize enterprise application routing
app = FastAPI(
    title="PlatinumAILabs Core Engine API", 
    description="Autonomous Multi-Agent Routing, Compliance, and Generation Pipeline",
    version="1.0.0"
)

# Enable secure communication across different corporate domains (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In strict production, swap with the client's actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define strict payload input schemas
class LeadInboundPayload(BaseModel):
    lead_source: str = "Webform Integration"
    raw_text: str

# Replicate the core DPDP field-level protection algorithm
def apply_dpdp_masking(text: str) -> str:
    # Mask standard 10-digit mobile number patterns
    text = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE_NUMBER]', text)
    # Mask standard email domain configurations
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', text)
    return text

@app.get("/")
def read_root():
    return {"status": "operational", "engine": "PlatinumAILabs Distributed Graph Active"}

@app.post("/api/v1/triage-lead")
async def triage_lead(payload: LeadInboundPayload):
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Inbound payload text string cannot be structurally null or empty.")
    
    # 1. Enforce strict data-privacy perimeter insulation
    secured_input = apply_dpdp_masking(payload.raw_text)
    
    try:
        # 2. Stream processed text packet directly into LangGraph state machine memory
        initial_state = {"raw_input": secured_input}
        final_state = engine.invoke(initial_state)
        
        # 3. Serialize output components back to the receiving webhook consumer
        return {
            "status": "processed",
            "compliance_metrics": {
                "dpdp_masking_applied": True,
                "critic_intervention_logged": final_state.get("critic_feedback") != ""
            },
            "payload_analytics": {
                "source": payload.lead_source,
                "inferred_intent": final_state.get("parsed_intent")
            },
            "ground_truth_context": final_state.get("data_context"),
            "final_verified_response": final_state.get("generated_output")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Graph Exception: {str(e)}")