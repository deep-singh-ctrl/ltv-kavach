"""
Unit and Integration Tests for LTV-Kavach Quantitative and ML Engines.
"""

import sys
pkg_path = "/home/deepank-singh/Documents/ltv-kavach/packages"
root_path = "/home/deepank-singh/Documents/ltv-kavach"
if pkg_path not in sys.path:
    sys.path.insert(0, pkg_path)
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.risk_engine import (
    calculate_portfolio_metrics,
    simulate_market_shock,
    calculate_buffer_remedies,
    simulate_pre_loan_sandbox
)
from src.ml_model import ml_engine
from src.vernacular_engine import generate_vernacular_guidance
from src.data_store import INVESTOR_PERSONAS

def test_portfolio_metrics_ramesh_high_risk():
    ramesh = INVESTOR_PERSONAS["persona_ramesh_high_risk"]
    metrics = calculate_portfolio_metrics(ramesh["holdings"], ramesh["loan_outstanding"])
    
    assert "error" not in metrics
    assert metrics["current_ltv_pct"] > 60.0
    assert metrics["portfolio_beta"] > 1.5
    assert metrics["hhi_concentration"] > 3000
    assert metrics["drop_to_margin_call_pct"] < 10.0 # near margin call!

def test_portfolio_metrics_sunita_safe():
    sunita = INVESTOR_PERSONAS["persona_sunita_conservative"]
    metrics = calculate_portfolio_metrics(sunita["holdings"], sunita["loan_outstanding"])
    
    assert "error" not in metrics
    assert metrics["current_ltv_pct"] < 25.0
    assert metrics["status_zone"] == "SAFE_GREEN"
    assert metrics["drop_to_margin_call_pct"] > 50.0

def test_stress_test_liquidation_trigger():
    ramesh = INVESTOR_PERSONAS["persona_ramesh_high_risk"]
    # With beta ~1.8, a 10% market drop produces ~18% portfolio loss
    res = simulate_market_shock(ramesh["holdings"], ramesh["loan_outstanding"], market_drop_pct=-0.10)
    
    assert res["simulated_ltv_pct"] > 70.0
    assert res["margin_call_breached"] is True

def test_buffer_remedies():
    remedies = calculate_buffer_remedies(
        loan_outstanding=380000.0,
        current_collateral_value=580000.0,
        portfolio_beta=1.8,
        maintenance_ltv=0.65,
        safe_target_ltv=0.45
    )
    cash_remedy = remedies["cash_prepayment_remedy"]["amount_inr"]
    # Target debt at 45% = 580000 * 0.45 = 261000. Cash needed = 380000 - 261000 = 119000
    assert cash_remedy == 119000.0
    assert remedies["pledge_collateral_remedy"]["amount_inr"] > 0

def test_ml_vulnerability_predictions():
    pred_high = ml_engine.predict_vulnerability(
        starting_ltv=0.65,
        portfolio_beta=1.85,
        hhi_concentration=4500,
        annual_volatility=0.45,
        top1_holding_share=0.55,
        buffer_liquidity_ratio=0.03
    )
    assert pred_high["vulnerability_score"] >= 60
    assert pred_high["risk_grade"] in ["HIGH", "CRITICAL"]

    pred_safe = ml_engine.predict_vulnerability(
        starting_ltv=0.22,
        portfolio_beta=0.65,
        hhi_concentration=1200,
        annual_volatility=0.15,
        top1_holding_share=0.25,
        buffer_liquidity_ratio=0.35
    )
    assert pred_safe["vulnerability_score"] < 40
    assert pred_safe["risk_grade"] in ["LOW", "MODERATE"]

def test_vernacular_guidance_generation():
    fake_context = {
        "current_ltv_pct": 68.0,
        "drop_to_margin_call_pct": 2.5,
        "status_zone": "WARNING_AMBER",
        "remedies": {
            "cash_prepayment_remedy": {"amount_inr": 45000.0},
            "pledge_collateral_remedy": {"amount_inr": 65000.0}
        }
    }
    hi_guide = generate_vernacular_guidance(fake_context, lang="hi")
    assert "शेयर" in hi_guide["message"]
    assert "₹45,000" in hi_guide["action_prompt"]

def test_sensitivity_and_swap_insight():
    ramesh = INVESTOR_PERSONAS["persona_ramesh_high_risk"]
    metrics = calculate_portfolio_metrics(ramesh["holdings"], ramesh["loan_outstanding"])
    
    assert "sensitivity_breakdown" in metrics
    sb = metrics["sensitivity_breakdown"]
    assert sb["high_beta_pct"] > 60.0 # Suzlon and Zomato
    assert sb["high_beta_val"] > 0.0

    assert "swap_insight" in metrics
    si = metrics["swap_insight"]
    assert si["target_symbol"] == "SUZLON"
    assert si["simulated_portfolio_beta"] < metrics["portfolio_beta"]
    assert si["risk_reduction_pct"] > 20.0
    assert "Nifty 50" in si["replacement_benchmark"]
    assert len(si["summary_hi"]) > 0
    assert len(si["action_hi"]) > 0

def test_calm_mitigation_remedies():
    ramesh = INVESTOR_PERSONAS["persona_ramesh_high_risk"]
    remedies = calculate_buffer_remedies(
        loan_outstanding=ramesh["loan_outstanding"],
        current_collateral_value=496000.0,
        portfolio_beta=1.82,
        maintenance_ltv=0.65
    )
    assert "calm_mitigation" in remedies
    cm = remedies["calm_mitigation"]
    assert cm["exact_cash_inr"] > 0
    assert cm["exact_reliance_shares"] > 0
    assert cm["exact_debt_units"] > 0
    assert "Stay Calm" in cm["reassurance_en"]
    assert "घबराएं नहीं" in cm["reassurance_hi"]

    # Also test calm mitigation in simulate_market_shock
    stress = simulate_market_shock(ramesh["holdings"], ramesh["loan_outstanding"], market_drop_pct=-0.15)
    assert "calm_mitigation" in stress
    assert stress["calm_mitigation"]["exact_cash_inr"] > 0

if __name__ == "__main__":
    test_portfolio_metrics_ramesh_high_risk()
    test_portfolio_metrics_sunita_safe()
    test_stress_test_liquidation_trigger()
    test_buffer_remedies()
    test_ml_vulnerability_predictions()
    test_vernacular_guidance_generation()
    test_sensitivity_and_swap_insight()
    test_calm_mitigation_remedies()
    print("✅ All 8 Risk Engine, Sensitivity, & Calm Mitigation tests passed successfully!")

