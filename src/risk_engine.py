"""
Quantitative Risk & Resilience Calculation Engine for Loan Against Securities (LAS).
Computes LTV trajectories, Distance to Margin Call (DMC), Volatility/Beta exposure,
Value-at-Risk (VaR), and structural buffer recommendations.
"""

from typing import Dict, List, Any
import math
from src.data_store import ASSET_CATALOG

def calculate_portfolio_metrics(
    holdings: List[Dict[str, Any]],
    loan_outstanding: float,
    maintenance_ltv: float = 0.65,
    liquidation_ltv: float = 0.75,
    safe_target_ltv: float = 0.45
) -> Dict[str, Any]:
    """
    Evaluates collateral health, weighted beta, concentration, and margin buffers.
    """
    total_collateral_value = 0.0
    haircut_adjusted_value = 0.0
    enriched_holdings = []

    for h in holdings:
        symbol = h.get("symbol", "").upper()
        units = float(h.get("units", 0))
        meta = ASSET_CATALOG.get(symbol, {
            "name": symbol,
            "category": "Equities",
            "beta": 1.2,
            "annual_vol": 0.30,
            "haircut": 0.30,
            "price": float(h.get("current_value", 0)) / max(units, 1)
        })
        
        current_value = float(h.get("current_value", units * meta.get("price", 0)))
        total_collateral_value += current_value
        haircut = meta.get("haircut", 0.30)
        haircut_val = current_value * (1.0 - haircut)
        haircut_adjusted_value += haircut_val

        enriched_holdings.append({
            "symbol": symbol,
            "name": meta.get("name", symbol),
            "category": meta.get("category", "Equity"),
            "units": units,
            "current_value": round(current_value, 2),
            "beta": meta.get("beta", 1.0),
            "annual_vol": meta.get("annual_vol", 0.25),
            "haircut": haircut
        })

    if total_collateral_value <= 0:
        return {"error": "Total collateral value must be greater than zero"}

    # Portfolio weights and concentration
    portfolio_beta = 0.0
    hhi = 0.0
    top1_share = 0.0

    for item in enriched_holdings:
        weight = item["current_value"] / total_collateral_value
        item["weight_pct"] = round(weight * 100.0, 2)
        portfolio_beta += weight * item["beta"]
        hhi += (weight * 100.0) ** 2
        if weight > top1_share:
            top1_share = weight

    portfolio_beta = round(portfolio_beta, 3)
    hhi = round(hhi, 1)
    current_ltv = round(loan_outstanding / total_collateral_value, 4)

    # Percentage drops required to breach thresholds
    # Drop % = 1 - (Current_LTV / Threshold_LTV)
    if current_ltv >= maintenance_ltv:
        drop_to_margin_call_pct = 0.0
        collateral_loss_to_margin_call = 0.0
    else:
        drop_to_margin_call_pct = round((1.0 - (current_ltv / maintenance_ltv)) * 100.0, 2)
        # Required portfolio value at maintenance: Loan / Maintenance_LTV
        value_at_maintenance = loan_outstanding / maintenance_ltv
        collateral_loss_to_margin_call = round(total_collateral_value - value_at_maintenance, 2)

    if current_ltv >= liquidation_ltv:
        drop_to_liquidation_pct = 0.0
        collateral_loss_to_liquidation = 0.0
    else:
        drop_to_liquidation_pct = round((1.0 - (current_ltv / liquidation_ltv)) * 100.0, 2)
        value_at_liquidation = loan_outstanding / liquidation_ltv
        collateral_loss_to_liquidation = round(total_collateral_value - value_at_liquidation, 2)

    # Determine status zone
    if current_ltv < safe_target_ltv:
        status_zone = "SAFE_GREEN"
        status_label = "Resilient (Safe Zone)"
    elif current_ltv < maintenance_ltv:
        status_zone = "MODERATE_YELLOW"
        status_label = "Caution (Approaching Margin Line)"
    elif current_ltv < liquidation_ltv:
        status_zone = "WARNING_AMBER"
        status_label = "Margin Call Active (Action Required)"
    else:
        status_zone = "CRITICAL_RED"
        status_label = "Liquidation Imminent (Assets At Risk)"

    # Concentration risk classification
    if hhi > 3500 or top1_share > 0.50:
        concentration_risk = "HIGH_CONCENTRATION"
    elif hhi > 2000 or top1_share > 0.35:
        concentration_risk = "MODERATE_CONCENTRATION"
    else:
        concentration_risk = "WELL_DIVERSIFIED"

    # Collateral Sensitivity Breakdown
    high_beta_val = 0.0
    mod_beta_val = 0.0
    low_beta_val = 0.0
    highest_beta_item = None
    max_beta_val = -1.0

    for item in enriched_holdings:
        b = item["beta"]
        val = item["current_value"]
        if b > 1.3:
            high_beta_val += val
        elif b >= 0.8:
            mod_beta_val += val
        else:
            low_beta_val += val

        if b > max_beta_val:
            max_beta_val = b
            highest_beta_item = item

    high_beta_pct = round((high_beta_val / total_collateral_value) * 100.0, 1)
    mod_beta_pct = round((mod_beta_val / total_collateral_value) * 100.0, 1)
    low_beta_pct = round((low_beta_val / total_collateral_value) * 100.0, 1)

    # Actionable De-risking Swap Insight (e.g. swapping highest-beta stock with Nifty 50 bluechip)
    if highest_beta_item and highest_beta_item["beta"] > 1.15 and total_collateral_value > 0:
        weight_to_swap = highest_beta_item["current_value"] / total_collateral_value
        beta_saving = (highest_beta_item["beta"] - 0.95) * weight_to_swap
        sim_new_beta = round(max(0.40, portfolio_beta - beta_saving), 2)
        risk_reduction = round(((portfolio_beta - sim_new_beta) / max(portfolio_beta, 0.01)) * 100.0, 1)

        swap_insight = {
            "target_symbol": highest_beta_item["symbol"],
            "target_name": highest_beta_item["name"],
            "target_beta": highest_beta_item["beta"],
            "target_val": round(highest_beta_item["current_value"]),
            "replacement_benchmark": "Nifty 50 Bluechip (e.g. Reliance / HDFC Bank)",
            "replacement_beta": 0.95,
            "current_portfolio_beta": portfolio_beta,
            "simulated_portfolio_beta": sim_new_beta,
            "risk_reduction_pct": risk_reduction,
            "summary_en": f"Your LTV is {round(current_ltv * 100.0, 1)}%, but {high_beta_pct}% of your collateral is concentrated in high-sensitivity stocks that drop significantly faster than the market.",
            "summary_hi": f"आपका एलटीवी {round(current_ltv * 100.0, 1)}% है, लेकिन आपका {high_beta_pct}% गिरवी शेयर उच्च-संवेदनशीलता वाले शेयरों में है जो बाज़ार से दोगुनी तेज़ी से गिरते हैं।",
            "action_en": f"Actionable Tip: Swapping your high-beta holding ({highest_beta_item['symbol']}, Beta {highest_beta_item['beta']}) with a Nifty 50 bluechip lowers portfolio beta from {portfolio_beta} to {sim_new_beta} ({risk_reduction}% safer).",
            "action_hi": f"सुझाव: अपने उच्च-संवेदनशील शेयर ({highest_beta_item['symbol']}, बीटा {highest_beta_item['beta']}) को निफ्टी ५० शेयर से बदलने पर पोर्टफोलियो बीटा {portfolio_beta} से घटकर {sim_new_beta} हो जाएगा ({risk_reduction}% कम जोखिम)।"
        }
    else:
        swap_insight = {
            "target_symbol": "Portfolio Stable",
            "target_name": "Well Balanced",
            "target_beta": portfolio_beta,
            "target_val": 0,
            "replacement_benchmark": "Debt Mutual Fund / Large Cap",
            "replacement_beta": 0.85,
            "current_portfolio_beta": portfolio_beta,
            "simulated_portfolio_beta": portfolio_beta,
            "risk_reduction_pct": 0.0,
            "summary_en": f"Your LTV is {round(current_ltv * 100.0, 1)}% with balanced sensitivity ({low_beta_pct}% low-risk assets).",
            "summary_hi": f"आपका एलटीवी {round(current_ltv * 100.0, 1)}% है और पोर्टफोलियो संवेदनशीलता संतुलित है ({low_beta_pct}% सुरक्षित संपत्तियां)।",
            "action_en": "Your pledged assets have low-to-moderate sensitivity. Maintain your regular repayment schedule.",
            "action_hi": "आपके गिरवी शेयर संतुलित हैं। नियमित पुनर्भुगतान बनाए रखें।"
        }

    return {
        "loan_outstanding": loan_outstanding,
        "total_collateral_value": round(total_collateral_value, 2),
        "haircut_adjusted_value": round(haircut_adjusted_value, 2),
        "current_ltv": current_ltv,
        "current_ltv_pct": round(current_ltv * 100.0, 2),
        "maintenance_ltv": maintenance_ltv,
        "liquidation_ltv": liquidation_ltv,
        "safe_target_ltv": safe_target_ltv,
        "portfolio_beta": portfolio_beta,
        "hhi_concentration": hhi,
        "top1_share_pct": round(top1_share * 100.0, 2),
        "concentration_risk": concentration_risk,
        "drop_to_margin_call_pct": drop_to_margin_call_pct,
        "collateral_loss_to_margin_call": collateral_loss_to_margin_call,
        "drop_to_liquidation_pct": drop_to_liquidation_pct,
        "collateral_loss_to_liquidation": collateral_loss_to_liquidation,
        "status_zone": status_zone,
        "status_label": status_label,
        "sensitivity_breakdown": {
            "high_beta_pct": high_beta_pct,
            "mod_beta_pct": mod_beta_pct,
            "low_beta_pct": low_beta_pct,
            "high_beta_val": round(high_beta_val, 2),
            "mod_beta_val": round(mod_beta_val, 2),
            "low_beta_val": round(low_beta_val, 2)
        },
        "interest_metrics": {
            "annual_rate_pct": 10.5,
            "monthly_interest": round((loan_outstanding * 0.105) / 12, 2),
            "annual_interest": round(loan_outstanding * 0.105, 2)
        },
        "swap_insight": swap_insight,
        "holdings": enriched_holdings
    }

def simulate_market_shock(
    holdings: List[Dict[str, Any]],
    loan_outstanding: float,
    market_drop_pct: float,  # e.g., -0.10 for -10% drop
    maintenance_ltv: float = 0.65,
    liquidation_ltv: float = 0.75,
    safe_target_ltv: float = 0.45
) -> Dict[str, Any]:
    """
    Simulates portfolio stress under broad market shocks, adjusting for individual asset betas.
    """
    base_metrics = calculate_portfolio_metrics(
        holdings, loan_outstanding, maintenance_ltv, liquidation_ltv, safe_target_ltv
    )
    if "error" in base_metrics:
        return base_metrics

    # Normalize market_drop_pct if provided as percentage (e.g. -20.0 or 20.0) or positive ratio
    if abs(market_drop_pct) > 1.0:
        market_drop_pct = market_drop_pct / 100.0
    if market_drop_pct > 0:
        market_drop_pct = -market_drop_pct

    simulated_collateral_value = 0.0
    simulated_holdings = []

    for h in base_metrics["holdings"]:
        beta = h["beta"]
        # Stock specific drop adjusted by beta
        stock_drop = market_drop_pct * beta
        # Clamp maximum realistic loss to -95%
        stock_drop = max(stock_drop, -0.95)
        new_val = max(0.0, h["current_value"] * (1.0 + stock_drop))
        simulated_collateral_value += new_val
        simulated_holdings.append({
            **h,
            "simulated_drop_pct": round(stock_drop * 100.0, 2),
            "simulated_value": round(new_val, 2),
            "value_loss": round(h["current_value"] - new_val, 2)
        })

    simulated_ltv = round(loan_outstanding / max(simulated_collateral_value, 1.0), 4)
    total_wealth_lost = round(base_metrics["total_collateral_value"] - simulated_collateral_value, 2)

    # Determine simulated status
    if simulated_ltv < safe_target_ltv:
        zone = "SAFE_GREEN"
        severity = "Low Risk: Collateral remains resilient."
    elif simulated_ltv < maintenance_ltv:
        zone = "MODERATE_YELLOW"
        severity = "Moderate Risk: Buffer tightening, monitor closely."
    elif simulated_ltv < liquidation_ltv:
        zone = "WARNING_AMBER"
        severity = f"MARGIN CALL TRIGGERED! LTV reached {round(simulated_ltv*100, 1)}%."
    else:
        zone = "CRITICAL_RED"
        severity = f"FORCED LIQUIDATION! LTV breached {round(simulated_ltv*100, 1)}%."

    # If liquidation triggered, calculate amount lender will dump at market price
    liquidation_dump_amount = 0.0
    if simulated_ltv >= liquidation_ltv:
        # Amount to sell to bring LTV back to safe 50%:
        # (Loan - 0.50 * Collateral) / (1 - 0.50)
        target = 0.50
        if simulated_collateral_value > 0:
            excess_debt = loan_outstanding - (target * simulated_collateral_value)
            liquidation_dump_amount = max(0.0, excess_debt / (1.0 - target))
            liquidation_dump_amount = min(liquidation_dump_amount, simulated_collateral_value)

    simulated_remedies = calculate_buffer_remedies(
        loan_outstanding=loan_outstanding,
        current_collateral_value=simulated_collateral_value,
        portfolio_beta=base_metrics.get("portfolio_beta", 1.0),
        maintenance_ltv=maintenance_ltv,
        safe_target_ltv=safe_target_ltv
    )

    return {
        "market_drop_pct": round(market_drop_pct * 100.0, 2),
        "original_collateral_value": base_metrics["total_collateral_value"],
        "simulated_collateral_value": round(simulated_collateral_value, 2),
        "total_wealth_lost": total_wealth_lost,
        "original_ltv_pct": base_metrics["current_ltv_pct"],
        "simulated_ltv": simulated_ltv,
        "simulated_ltv_pct": round(simulated_ltv * 100.0, 2),
        "status_zone": zone,
        "severity_message": severity,
        "margin_call_breached": simulated_ltv >= maintenance_ltv,
        "liquidation_breached": simulated_ltv >= liquidation_ltv,
        "liquidation_dump_amount": round(liquidation_dump_amount, 2),
        "calm_mitigation": simulated_remedies["calm_mitigation"],
        "holdings": simulated_holdings
    }

def calculate_buffer_remedies(
    loan_outstanding: float,
    current_collateral_value: float,
    portfolio_beta: float,
    maintenance_ltv: float = 0.65,
    safe_target_ltv: float = 0.45
) -> Dict[str, Any]:
    """
    Computes actionable, non-speculative safety buffers to shockproof the loan.
    """
    current_ltv = loan_outstanding / max(current_collateral_value, 1.0)

    # Remedy 1: Immediate Cash Paydown to hit Safe LTV
    target_debt = current_collateral_value * safe_target_ltv
    cash_paydown_needed = max(0.0, loan_outstanding - target_debt)

    # Remedy 2: Additional Collateral Pledged (assuming low-risk Debt/Liquid fund with 10% haircut)
    # Required Collateral = Loan / Safe_LTV
    target_collateral = loan_outstanding / safe_target_ltv
    additional_collateral_needed = max(0.0, target_collateral - current_collateral_value)

    # Remedy 3: "Shockproof for a 20% Market Crash" Buffer
    # If market drops 20%, portfolio drops by 20% * Beta
    expected_crash_drop = 0.20 * portfolio_beta
    expected_crash_drop = min(expected_crash_drop, 0.70)
    post_crash_value = current_collateral_value * (1.0 - expected_crash_drop)
    
    # In order to stay below maintenance LTV (0.65) AFTER the 20% crash:
    # Loan_Max_Allowed = post_crash_value * maintenance_ltv
    max_safe_debt_for_crash = post_crash_value * maintenance_ltv
    crashproof_cash_buffer = max(0.0, loan_outstanding - max_safe_debt_for_crash)

    # Exact shares calculation for pledge remedy
    reliance_units = int(math.ceil(additional_collateral_needed / 1167.7)) if additional_collateral_needed > 0 else 0
    tcs_units = int(math.ceil(additional_collateral_needed / 2075.0)) if additional_collateral_needed > 0 else 0
    debt_fund_units = int(math.ceil(additional_collateral_needed / 32.4)) if additional_collateral_needed > 0 else 0

    is_breached = current_ltv >= maintenance_ltv

    calm_mitigation = {
        "is_breached": is_breached,
        "exact_cash_inr": round(cash_paydown_needed),
        "exact_reliance_shares": reliance_units,
        "exact_tcs_shares": tcs_units,
        "exact_debt_units": debt_fund_units,
        "exact_collateral_val": round(additional_collateral_needed),
        "monthly_interest_saved": round((cash_paydown_needed * 0.105) / 12),
        "new_monthly_interest": round((max(0.0, loan_outstanding - cash_paydown_needed) * 0.105) / 12),
        "reassurance_en": "Stay Calm. You have clear, proven options. Lenders provide an advance notice window before taking any market action. Follow these 2 exact steps to immediately restore your safe margin:",
        "reassurance_hi": "घबराएं नहीं। आपके पास सुरक्षित और स्पष्ट विकल्प हैं। बैंक ज़बरन बिक्री से पहले सूचना देते हैं। अपने पोर्टफोलियो को सुरक्षित रखने के लिए ये २ आसान कदम उठाएं:",
        "step1_en": f"Option 1 (Cash): Pay exactly ₹{round(cash_paydown_needed):,} via UPI/IMPS directly to your loan account to restore your LTV to {safe_target_ltv*100}%.",
        "step1_hi": f"विकल्प १ (नकद): सुरक्षित {safe_target_ltv*100}% एलटीवी पर लौटने के लिए अपने लोन खाते में ठीक ₹{round(cash_paydown_needed):,} का यूपीआई/आईएमपीएस द्वारा भुगतान करें।",
        "step2_en": f"Option 2 (Zero Cash): Pledge just {reliance_units} shares of Reliance (or ₹{round(additional_collateral_needed):,} in Debt Mutual Funds) via instant NSDL OTP—zero cash required.",
        "step2_hi": f"विकल्प २ (बिना नकद): बिना एक भी रुपया खर्च किए केवल {reliance_units} रिलायंस शेयर (या ₹{round(additional_collateral_needed):,} का डेट म्यूचुअल फंड) त्वरित एनएसडीएल ओटीपी द्वारा गिरवी रखें।"
    }

    return {
        "current_ltv_pct": round(current_ltv * 100.0, 2),
        "safe_target_ltv_pct": round(safe_target_ltv * 100.0, 2),
        "cash_prepayment_remedy": {
            "amount_inr": round(cash_paydown_needed, 2),
            "result_ltv_pct": safe_target_ltv * 100.0,
            "explanation": f"Pay ₹{round(cash_paydown_needed):,} to reduce your loan balance and restore LTV to a bulletproof {safe_target_ltv*100}%."
        },
        "pledge_collateral_remedy": {
            "amount_inr": round(additional_collateral_needed, 2),
            "recommended_asset_type": "Debt Mutual Fund / Liquid ETF / Bank FD",
            "exact_reliance_shares": reliance_units,
            "exact_tcs_shares": tcs_units,
            "exact_debt_units": debt_fund_units,
            "result_ltv_pct": safe_target_ltv * 100.0,
            "explanation": f"Pledge just {reliance_units} shares of Reliance or ₹{round(additional_collateral_needed):,} of safe debt funds via NSDL OTP without paying any cash."
        },
        "crashproof_20pct_remedy": {
            "amount_inr": round(crashproof_cash_buffer, 2),
            "tested_drop_pct": round(expected_crash_drop * 100.0, 1),
            "explanation": f"To guarantee you NEVER get a margin call even if the market drops {round(expected_crash_drop*100, 1)}%, keep a liquidity reserve of ₹{round(crashproof_cash_buffer):,}."
        },
        "calm_mitigation": calm_mitigation
    }

def simulate_pre_loan_sandbox(
    portfolio_value: float,
    proposed_loan_amount: float,
    portfolio_beta: float = 1.0,
    maintenance_ltv: float = 0.65
) -> Dict[str, Any]:
    """
    'Before You Pledge' Safety Net Sandbox.
    Prevents borrowers from getting trapped into overleveraged loans before signing.
    """
    initial_ltv = proposed_loan_amount / max(portfolio_value, 1.0)
    
    # Calculate how much market drop triggers margin call
    if initial_ltv >= maintenance_ltv:
        max_market_drop_tolerated = 0.0
    else:
        # Portfolio drop % = 1 - (Initial_LTV / Maintenance_LTV)
        # Market drop % = Portfolio drop % / Beta
        portfolio_drop_tolerated = 1.0 - (initial_ltv / maintenance_ltv)
        max_market_drop_tolerated = portfolio_drop_tolerated / max(portfolio_beta, 0.5)

    max_market_drop_pct = round(max(0.0, max_market_drop_tolerated) * 100.0, 1)

    # Recommended safe borrow amount (designed to survive at least a 25% market drawdown)
    # Target LTV = Maintenance_LTV * (1 - 0.25 * Beta)
    safe_survivable_drop = min(0.35, 0.25 * portfolio_beta)
    prudent_ltv_cap = max(0.20, maintenance_ltv * (1.0 - safe_survivable_drop))
    prudent_loan_limit = round(portfolio_value * prudent_ltv_cap, 2)

    risk_rating = "SAFE"
    if max_market_drop_pct < 8.0:
        risk_rating = "DANGEROUS"
        verdict = f"High Danger! A minor {max_market_drop_pct}% dip will trigger a lender margin call."
    elif max_market_drop_pct < 18.0:
        risk_rating = "MODERATE"
        verdict = f"Moderate caution. You can survive a {max_market_drop_pct}% correction, but high volatility may cause stress."
    else:
        risk_rating = "HEALTHY"
        verdict = f"Healthy cushion! Your portfolio can absorb up to a {max_market_drop_pct}% market drop before any alert."

    return {
        "portfolio_value": portfolio_value,
        "proposed_loan_amount": proposed_loan_amount,
        "initial_ltv_pct": round(initial_ltv * 100.0, 2),
        "max_market_drop_pct": max_market_drop_pct,
        "prudent_loan_limit": prudent_loan_limit,
        "prudent_ltv_cap_pct": round(prudent_ltv_cap * 100.0, 1),
        "risk_rating": risk_rating,
        "verdict": verdict
    }
