import re
import httpx
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from main import engine

# Initialize application routing
app = FastAPI(
    title="PlatinumAILabs Enterprise Webhook Engine", 
    description="Autonomous Multi-Agent Routing with Outbound Webhook Relay",
    version="1.1.0"
)

# Enable secure cross-domain communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define an expanded schema that accepts an optional outbound relay destination
class LeadInboundPayload(BaseModel):
    lead_source: str = "Webform Automation"
    raw_text: str
    outbound_webhook_url: Optional[str] = None  # The destination URL (e.g., Zapier/CRM)

def apply_dpdp_masking(text: str) -> str:
    text = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE_NUMBER]', text)
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', text)
    return text

# Asynchronous background worker to forward the audited output and keep your API ultra-fast
async def send_outbound_webhook(target_url: str, processed_data: dict):
    async with httpx.AsyncClient() as client:
        try:
            print(f"[WEBHOOK INFRA] Attempting to dispatch audited payload to: {target_url}")
            response = await client.post(target_url, json=processed_data, timeout=10.0)
            print(f"[WEBHOOK INFRA] Server responded with status code: {response.status_code}")
        except Exception as e:
            print(f"[WEBHOOK ERROR] Failed to deliver data payload to destination: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "operational", "pipeline": "Outbound Webhook Relay Engine Active"}

@app.post("/api/v1/triage-lead")
async def triage_lead(payload: LeadInboundPayload, background_tasks: BackgroundTasks):
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Inbound payload text string cannot be null.")
    
    # 1. Enforce privacy insulation layer
    secured_input = apply_dpdp_masking(payload.raw_text)
    
    try:
        # 2. Invoke the multi-agent graph
        initial_state = {"raw_input": secured_input}
        final_state = engine.invoke(initial_state)
        
        # 3. Structure the final compiled payload
        response_payload = {
            "status": "success",
            "metadata": {
                "source": payload.lead_source,
                "critic_intervention_logged": final_state.get("critic_feedback") != ""
            },
            "analytics": {
                "inferred_intent": final_state.get("parsed_intent")
            },
            "ground_truth_context": final_state.get("data_context"),
            "final_verified_response": final_state.get("generated_output")
        }
        
        # 4. If an outbound destination exists, queue it as a non-blocking background process
        if payload.outbound_webhook_url:
            background_tasks.add_task(send_outbound_webhook, payload.outbound_webhook_url, response_payload)
            response_payload["webhook_status"] = "Queued for immediate outbound delivery"
            
        return response_payload
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Graph Exception: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Graph Exception: {str(e)}")
