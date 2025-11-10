import os
import pandas as pd
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph , START , END
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import Dict, Any, TypedDict
from langchain.groq import ChatGroq


claims = pd.read_csv('/Users/prabhat/OneDrive/Desktop/codingbase/PYTHON_Codebase/AI_WARAANTY_DETECTOR/Data/warranty_claims - Copy.csv')


loader = PyPDFLoader('/Users/prabhat/OneDrive/Desktop/codingbase/PYTHON_Codebase/AI_WARAANTY_DETECTOR/Data/AutoDrive_Warranty_Policy_2025.pdf')
load= loader.load()
policy_text = " ".join([doc.page_content for doc in load])


from langchain.chat_models import init_chat_model
llm =  init_chat_model ("openai/gpt-oss-20b",model_provider='GROQ',api_key = '')


class ClassState(TypedDict):
    claims:Dict[str,Any]
    policy_tracker:str
    fraud_tracker:str
    fraud_score:float
    evidence:str
    decision:str

def policy_check_agent(State: ClassState) -> ClassState:
    claim = State["claims"]

    # ✅ Safely get Vehicle Type (use default if missing)
    vehicle_type = claim.get("Vehicle Type", "Unknown")

    # ✅ Infer vtype based on value
    if vehicle_type.lower() == "car":
        vtype = "Four Wheeler"
    elif vehicle_type.lower() in ["bike", "scooter", "motorcycle"]:
        vtype = "Two Wheeler"
    else:
        vtype = "Unknown"

    # Build your prompt
    prompt = f"""
    You are an expert insurance policy analyst. Analyze the following warranty claim details against the provided warranty policy document.

    Policy manual:
    {policy_text}

    Warranty claim details:
    vtype: {vtype}
    claim: {claim}

    Based on the above warranty policy document and claim details, determine:
    Answer: Policy is Covered or Not Covered. Provide a brief explanation for your decision.
    """

    # Invoke LLM
    response = llm.invoke(prompt)

    # Store the result
    State["policy_tracker"] = response.content.strip()
    return State



def fraud_detection_agent(State: ClassState) -> ClassState:
    claim = State['claims']

    prompt = f"""
    You are an expert fraud detection analyst. Analyze the following warranty claim details for potential fraud indicators.
     warranty policy document :
        {policy_text}

    claim details:
    claim:{claim}

        Based on the above warranty policy document and claim details, assess the likelihood of fraud. Provide a fraud score between 0 (no fraud) to 1 (definite fraud) along with a brief explanation.

    """
    response = llm.invoke(prompt)
    try:
        score = float(response.content.strip())
    except :
        score=0.5
    State['evidence'] = response.content.strip()
    State['fraud_score'] = score
    return State


def evidence_collector_agent(State: ClassState) -> ClassState:
    claim = State['claims']

    prompt = f"""
    You are an expert evidence collection analyst. Based on the following warranty claim details and previous analyses, summarize the key evidence supporting or refuting the claim.

     warranty policy document :
        {policy_text}

    claim details:
    claim:{claim}

    Previous Analyses:
    Policy Analysis: {State['policy_tracker']}
    Fraud Detector : {State['fraud_tracker']}
    Fraud Score: {State['fraud_score']}

     Based on the above information, summarize the key evidence supporting or refuting the claim.
        Answer:List any red flags, inconsistencies, or supporting details found in the claim.

    Provide a concise summary of the key evidence.

    """
    response = llm.invoke(prompt)
    State['evidence'] = response.content.strip()
    return State


def action_agent(State: ClassState) -> ClassState:
    claim = State['claims']
    policy_analysis = State['policy_tracker']
  
    evidence =  State['evidence']

    prompt = f"""
    You are an expert claims decision analyst. Based on the following warranty claim details and previous analyses, make a final decision on the claim.

     warranty policy document :
        {policy_text}

    claim details:
    claim:{claim}

    Previous Analyses:
    Policy Analysis: {State['policy_tracker']}
    
    Fraud Score: {State['fraud_score']}
    Evidence Summary: {State['evidence']}

     Based on the above information, make a final decision on the claim.
        Answer:Approve or Deny the claim. Provide a brief justification for your decision.

    """
    decision_text = ""
    try :
        if "approve" in decision_text.lower():
            decision_text = "Approve"   
        elif "deny" in decision_text.lower():
            decision_text = "DisApprove"

        elif "insufficient" in evidence.lower():
            decision_text = "Escalate for further review"

    except:
        decision_text = "Escalate for further review"


    response = llm.invoke(prompt)
    State['decision'] = response.content.strip()
    return State



graph = StateGraph(ClassState)

graph.add_node("PolicyCheck", policy_check_agent)
graph.add_node("FraudScoring", fraud_detection_agent)
graph.add_node("EvidenceCollector", evidence_collector_agent)
graph.add_node("Action", action_agent)

graph.set_entry_point("PolicyCheck")
graph.add_edge("PolicyCheck", "FraudScoring")
graph.add_edge("FraudScoring", "EvidenceCollector")
graph.add_edge("EvidenceCollector", "Action")
graph.add_edge("Action", END)

app = graph.compile()



results = []

for idx, row in claims.iterrows():
    state = app.invoke({"claims": row.to_dict(), 
                       "policy_tracker": "",
                       "fraud_tracker": "",
                       "fraud_score": 0.0,
                       "evidence": "",
                       "decision": ""})
    results.append({
        "claim_id": row["claim_id"],
        "model": row["model"],
        "decision": state["decision"],
        "policy_tracker": state["policy_tracker"],
        "fraud_score": state.get("fraud_score", 0.0),
        "evidence": state["evidence"]
    })

results_df = pd.DataFrame(results)
