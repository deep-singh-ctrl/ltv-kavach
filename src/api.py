"""
FastAPI Endpoints for LTV-Kavach Investor Resilience Platform.
Includes Live Market Data, Custom Profiles & CSV Statement Parsing.
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
from src.market_data import search_indian_stocks, fetch_live_stock_quote
from src.profile_store import (
    list_custom_profiles,
    save_custom_profile,
    delete_custom_profile,
    parse_csv_statement
)

router = APIRouter(prefix="/api")

class HoldingItem(BaseModel):
    symbol: str
    units: float
    current_value: Optional[float] = None
    price: Optional[float] = None
    name: Optional[str] = None
    category: Optional[str] = None
    beta: Optional[float] = None
    haircut: Optional[float] = None

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

class CsvImportRequest(BaseModel):
    csv_text: str

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

@router.get("/stocks/search")
def search_stocks(q: str = ""):
    """Live search across 100+ Indian stocks, mutual funds and ETFs."""
    return {"results": search_indian_stocks(q)}

@router.get("/stocks/quote/{symbol}")
def get_quote(symbol: str):
    """Fetches real-time price & beta for any NSE stock."""
    return fetch_live_stock_quote(symbol)

@router.get("/custom-profiles")
def get_custom_profiles():
    """Returns all user-created persistent borrower profiles."""
    return {"profiles": list_custom_profiles()}

@router.post("/custom-profiles")
def create_custom_profile(profile: Dict[str, Any]):
    """Saves or updates a persistent custom user profile."""
    saved = save_custom_profile(profile)
    return {"profile": saved}

@router.delete("/custom-profiles/{profile_id}")
def remove_custom_profile(profile_id: str):
    """Deletes a custom user profile."""
    success = delete_custom_profile(profile_id)
    return {"success": success}

@router.post("/import-csv")
def import_csv(req: CsvImportRequest):
    """Parses portfolio CSV text into structured holdings with live prices."""
    holdings = parse_csv_statement(req.csv_text)
    return {"holdings": holdings}

@router.post("/analyze")
def analyze_loan(req: AnalyzeRequest):
    """
    Complete analysis pipeline: Quantitative Risk + Explainable ML + Buffer Remedies + Vernacular.
    Supports predefined personas, custom saved profiles, or ad-hoc holdings.
    """
    holdings_data = []
    loan_amount = 0.0
    persona_meta = None
    cash_buffer = req.borrower_cash_buffer

    # 1. First check unified profiles store
    custom_list = list_custom_profiles()
    matched = next((c for c in custom_list if c["id"] == req.persona_id), None)
    if matched:
        persona_meta = matched
        holdings_data = matched.get("holdings", [])
        loan_amount = float(matched.get("loan_outstanding", 0.0))
        cash_buffer = float(matched.get("borrower_cash_buffer", 25000.0))
    elif req.persona_id and req.persona_id in INVESTOR_PERSONAS:
        p = INVESTOR_PERSONAS[req.persona_id]
        persona_meta = p
        holdings_data = p["holdings"]
        loan_amount = p["loan_outstanding"]
        cash_buffer = p.get("borrower_cash_buffer", cash_buffer)
    elif req.persona_id:
        raise HTTPException(status_code=404, detail="Profile not found")

    # 3. Ad-hoc custom input
    elif req.holdings and req.loan_outstanding:
        holdings_data = [h.dict() for h in req.holdings]
        loan_amount = req.loan_outstanding
    else:
        # Default fallback
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

    custom_list = list_custom_profiles()
    matched = next((c for c in custom_list if c["id"] == req.persona_id), None)
    if matched:
        holdings_data = matched.get("holdings", [])
        loan_amount = float(matched.get("loan_outstanding", 0.0))
    elif req.persona_id and req.persona_id in INVESTOR_PERSONAS:
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
    return simulate_pre_loan_sandbox(
        portfolio_value=req.portfolio_value,
        proposed_loan_amount=req.proposed_loan_amount,
        portfolio_beta=req.portfolio_beta
    )

@router.get("/depository-alert-preview/{persona_id}")
def depository_alert_preview(persona_id: str):
    p = None
    if persona_id in INVESTOR_PERSONAS:
        p = INVESTOR_PERSONAS[persona_id]
    elif persona_id.startswith("custom_"):
        custom_list = list_custom_profiles()
        p = next((c for c in custom_list if c["id"] == persona_id), None)

    if not p:
        p = INVESTOR_PERSONAS["persona_ramesh_high_risk"]

    metrics = calculate_portfolio_metrics(p["holdings"], p["loan_outstanding"])
    lender = p.get("lender", "Your NBFC Lender")
    name = p.get("name", "Investor")

    sms_text = (
        f"[NSDL-KAVACH ALERT] Dear {name}, your pledged collateral with {lender} "
        f"has an LTV of {metrics['current_ltv_pct']}%. "
        f"A market drop of {metrics['drop_to_margin_call_pct']}% will trigger lender liquidation. "
        f"Check safety buffer at ltvkavach.nsdl.org"
    )

    whatsapp_text = (
        f"🛡️ *NSDL COLLATERAL RESILIENCE ALERT*\n\n"
        f"Dear *{name}*,\n"
        f"Lender: *{lender}*\n\n"
        f"⚠️ *Current LTV:* {metrics['current_ltv_pct']}%\n"
        f"📉 *Distance to Margin Call:* {metrics['drop_to_margin_call_pct']}%\n"
        f"💰 *Pledged Portfolio Value:* ₹{metrics['total_collateral_value']:,}\n"
        f"💳 *Loan Borrowed:* ₹{metrics['loan_outstanding']:,}\n\n"
        f"💡 *Resilience Buffer Recommendation:* Pay ₹{round(max(0, metrics['loan_outstanding'] - metrics['total_collateral_value']*0.45)):,} "
        f"or pledge low-risk debt funds to protect against forced selling."
    )

    return {
        "recipient": name,
        "phone_masked": "+91 98XXX XX041",
        "sms_message": sms_text,
        "whatsapp_message": whatsapp_text
    }
