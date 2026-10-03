"""
FastAPI Endpoints for LTV-Kavach Investor Resilience Platform.
"""

import sys
pkg_path = "/home/deepank-singh/Documents/ltv-kavach/packages"
if pkg_path not in sys.path:
    sys.path.insert(0, pkg_path)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from src.data_store import ASSET_CATALOG, INVESTOR_PERSONAS, HISTORICAL_CRASH_SCENARIOS
from src.risk_engine import (
    calculate_portfolio_metrics,
    simulate_market_shock,
    calculate_buffer_remedies,
    simulate_pre_loan_sandbox
)
from src.ml_model import ml_engine
from src.vernacular_engine import generate_vernacular_guidance

router = APIRouter(prefix="/api")

class HoldingItem(BaseModel):
    symbol: str
    units: float
    current_value: Optional[float] = None

class AnalyzeRequest(BaseModel):
    persona_id: Optional[str] = None
    holdings: Optional[List[HoldingItem]] = None
    loan_outstanding: Optional[float] = None
    maintenance_ltv: float = 0.65
    liquidation_ltv: float = 0.75
    borrower_cash_buffer: float = 25000.0

class StressTestRequest(BaseModel):
    persona_id: Optional[str] = None
    holdings: Optional[List[HoldingItem]] = None
    loan_outstanding: Optional[float] = None
    market_drop_pct: float = -0.10
    maintenance_ltv: float = 0.65
    liquidation_ltv: float = 0.75

class SandboxRequest(BaseModel):
    portfolio_value: float
    proposed_loan_amount: float
    portfolio_beta: float = 1.0

@router.get("/personas")
def get_personas():
    """Returns pre-configured investor loan personas."""
    return {"personas": list(INVESTOR_PERSONAS.values())}

@router.get("/historical-scenarios")
def get_historical_scenarios():
    """Returns historical crash stress benchmarks."""
    return {"scenarios": HISTORICAL_CRASH_SCENARIOS}

@router.get("/asset-catalog")
def get_asset_catalog():
    """Returns sample reference equities and mutual funds."""
    return {"catalog": ASSET_CATALOG}

@router.post("/analyze")
def analyze_loan(req: AnalyzeRequest):
    """
    Complete analysis pipeline: Quantitative Risk + Explainable ML + Buffer Remedies + Vernacular.
    """
    holdings_data = []
    loan_amount = 0.0
    persona_meta = None
    cash_buffer = req.borrower_cash_buffer

    if req.persona_id and req.persona_id in INVESTOR_PERSONAS:
        p = INVESTOR_PERSONAS[req.persona_id]
        persona_meta = p
        holdings_data = p["holdings"]
        loan_amount = p["loan_outstanding"]
        cash_buffer = p.get("borrower_cash_buffer", cash_buffer)
    elif req.holdings and req.loan_outstanding:
        holdings_data = [h.dict() for h in req.holdings]
        loan_amount = req.loan_outstanding
    else:
        # Default to high-risk persona for instant demonstration
        p = INVESTOR_PERSONAS["persona_ramesh_high_risk"]
        persona_meta = p
        holdings_data = p["holdings"]
        loan_amount = p["loan_outstanding"]
        cash_buffer = p.get("borrower_cash_buffer", cash_buffer)

    # 1. Deterministic Financial Metrics
    metrics = calculate_portfolio_metrics(
        holdings_data,
        loan_amount,
        maintenance_ltv=req.maintenance_ltv,
        liquidation_ltv=req.liquidation_ltv
    )

    if "error" in metrics:
        raise HTTPException(status_code=400, detail=metrics["error"])

    # 2. Structural Buffer Remedies
    remedies = calculate_buffer_remedies(
        loan_outstanding=loan_amount,
        current_collateral_value=metrics["total_collateral_value"],
        portfolio_beta=metrics["portfolio_beta"],
        maintenance_ltv=req.maintenance_ltv
    )

    # 3. Machine Learning Vulnerability Prediction
    top1_share = metrics["top1_share_pct"] / 100.0
    buffer_ratio = cash_buffer / max(loan_amount, 1.0)
    # Estimate annual vol from portfolio beta
    estimated_annual_vol = 0.15 + (metrics["portfolio_beta"] * 0.12)

    ml_prediction = ml_engine.predict_vulnerability(
        starting_ltv=metrics["current_ltv"],
        portfolio_beta=metrics["portfolio_beta"],
        hhi_concentration=metrics["hhi_concentration"],
        annual_volatility=estimated_annual_vol,
        top1_holding_share=top1_share,
        buffer_liquidity_ratio=buffer_ratio
    )

    # 4. Vernacular Explanations (Hindi & English)
    full_context = {**metrics, "remedies": remedies}
    vernacular_hi = generate_vernacular_guidance(full_context, lang="hi")
    vernacular_en = generate_vernacular_guidance(full_context, lang="en")

    return {
        "persona": persona_meta,
        "metrics": metrics,
        "remedies": remedies,
        "ml_vulnerability": ml_prediction,
        "vernacular": {
            "hi": vernacular_hi,
            "en": vernacular_en
        }
    }

@router.post("/stress-test")
def stress_test(req: StressTestRequest):
    """
    Simulates portfolio stress at custom or historical crash drops.
    """
    holdings_data = []
    loan_amount = 0.0

    if req.persona_id and req.persona_id in INVESTOR_PERSONAS:
        p = INVESTOR_PERSONAS[req.persona_id]
        holdings_data = p["holdings"]
        loan_amount = p["loan_outstanding"]
    elif req.holdings and req.loan_outstanding:
        holdings_data = [h.dict() for h in req.holdings]
        loan_amount = req.loan_outstanding
    else:
        p = INVESTOR_PERSONAS["persona_ramesh_high_risk"]
        holdings_data = p["holdings"]
        loan_amount = p["loan_outstanding"]

    result = simulate_market_shock(
        holdings=holdings_data,
        loan_outstanding=loan_amount,
        market_drop_pct=req.market_drop_pct,
        maintenance_ltv=req.maintenance_ltv,
        liquidation_ltv=req.liquidation_ltv
    )

    return result

@router.post("/sandbox-borrow")
def pre_loan_sandbox(req: SandboxRequest):
    """
    Evaluates safety limits before a user pledges collateral.
    """
    return simulate_pre_loan_sandbox(
        portfolio_value=req.portfolio_value,
        proposed_loan_amount=req.proposed_loan_amount,
        portfolio_beta=req.portfolio_beta
    )

@router.get("/depository-alert-preview/{persona_id}")
def depository_alert_preview(persona_id: str):
    """
    Mocks an official NSDL Depository Pledge Alert message sent via SMS / WhatsApp.
    """
    p = INVESTOR_PERSONAS.get(persona_id, INVESTOR_PERSONAS["persona_ramesh_high_risk"])
    metrics = calculate_portfolio_metrics(p["holdings"], p["loan_outstanding"])
    
    sms_text = (
        f"[NSDL-KAVACH ALERT] Dear Investor ({p['name']}), your pledged securities against loan from "
        f"{p['lender']} have reached an LTV of {metrics['current_ltv_pct']}%. "
        f"Margin maintenance line is {round(p['lender_maintenance_ltv']*100)}%. "
        f"A market drop of {metrics['drop_to_margin_call_pct']}% will trigger lender liquidation. "
        f"Verify your portfolio buffer at ltvkavach.nsdl.org"
    )

    whatsapp_text = (
        f"🛡️ *NSDL PLEDGE COLLATERAL EARLY WARNING*\n\n"
        f"Dear *{p['name']}*,\n"
        f"Depository Participant: *NSDL / 003841*\n"
        f"Lender: *{p['lender']}*\n\n"
        f"⚠️ *Current LTV Status:* {metrics['current_ltv_pct']}%\n"
        f"📉 *Distance to Margin Call:* {metrics['drop_to_margin_call_pct']}%\n"
        f"💰 *Collateral Value:* ₹{metrics['total_collateral_value']:,}\n"
        f"💳 *Loan Outstanding:* ₹{metrics['loan_outstanding']:,}\n\n"
        f"💡 *Recommended Buffer Action:* Prepay ₹{round(max(0, metrics['loan_outstanding'] - metrics['total_collateral_value']*0.45)):,} "
        f"or pledge low-volatility debt funds to prevent forced market dumping.\n\n"
        f"_This is a public investor protection alert issued in public interest under SEBI / NSDL Investor Resilience Guidelines._"
    )

    return {
        "recipient": p["name"],
        "phone_masked": "+91 98XXX XX041",
        "sms_message": sms_text,
        "whatsapp_message": whatsapp_text
    }
