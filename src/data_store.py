"""
Reference Asset Database and Investor Personas for Indian Markets.
Includes realistic equity and mutual fund parameters (Beta, Haircut, Volatility).
"""

from typing import Dict, List, Any

# Standard asset dictionary with typical Indian NBFC/Bank LAS haircuts & betas
ASSET_CATALOG = {
    # Bluechips & Low Volatility
    "TCS": {"name": "Tata Consultancy Services", "category": "Large Cap", "beta": 0.78, "annual_vol": 0.18, "haircut": 0.20, "price": 4200.0},
    "RELIANCE": {"name": "Reliance Industries Ltd", "category": "Large Cap", "beta": 0.95, "annual_vol": 0.21, "haircut": 0.20, "price": 2980.0},
    "HDFCBANK": {"name": "HDFC Bank Ltd", "category": "Large Cap", "beta": 0.92, "annual_vol": 0.20, "haircut": 0.20, "price": 1650.0},
    "INFY": {"name": "Infosys Ltd", "category": "Large Cap", "beta": 0.88, "annual_vol": 0.22, "haircut": 0.20, "price": 1820.0},
    "ITC": {"name": "ITC Ltd", "category": "Large Cap", "beta": 0.65, "annual_vol": 0.16, "haircut": 0.20, "price": 485.0},
    
    # Mutual Funds / Balanced / Debt
    "PPFC_MF": {"name": "Parag Parikh Flexi Cap Fund", "category": "Diversified MF", "beta": 0.85, "annual_vol": 0.14, "haircut": 0.25, "price": 78.5},
    "NIFTY_BEES": {"name": "Nippon India Nifty 50 ETF", "category": "Index ETF", "beta": 1.00, "annual_vol": 0.15, "haircut": 0.20, "price": 275.0},
    "HDFC_SHORT_DEBT": {"name": "HDFC Short Term Debt Fund", "category": "Debt MF", "beta": 0.05, "annual_vol": 0.04, "haircut": 0.10, "price": 32.4},
    "ICICI_LIQUID": {"name": "ICICI Prudential Liquid Fund", "category": "Liquid MF", "beta": 0.02, "annual_vol": 0.02, "haircut": 0.10, "price": 355.0},

    # Midcaps (Moderate Volatility)
    "TATAMOTORS": {"name": "Tata Motors Ltd", "category": "Mid/Large Cap", "beta": 1.35, "annual_vol": 0.29, "haircut": 0.35, "price": 960.0},
    "POLYCAB": {"name": "Polycab India Ltd", "category": "Mid Cap", "beta": 1.25, "annual_vol": 0.28, "haircut": 0.35, "price": 6450.0},
    "FEDERALBNK": {"name": "Federal Bank Ltd", "category": "Mid Cap", "beta": 1.30, "annual_vol": 0.27, "haircut": 0.35, "price": 185.0},

    # Smallcaps & Speculative (High Volatility, High Beta)
    "SUZLON": {"name": "Suzlon Energy Ltd", "category": "Small Cap High Beta", "beta": 2.15, "annual_vol": 0.48, "haircut": 0.50, "price": 78.0},
    "ZOMATO": {"name": "Zomato Ltd", "category": "High Growth Tech", "beta": 1.75, "annual_vol": 0.42, "haircut": 0.45, "price": 265.0},
    "TATAPOWER": {"name": "Tata Power Co Ltd", "category": "Power / Cyclical", "beta": 1.55, "annual_vol": 0.36, "haircut": 0.40, "price": 435.0},
    "IDEA": {"name": "Vodafone Idea Ltd", "category": "Penny / Distressed", "beta": 2.45, "annual_vol": 0.62, "haircut": 0.60, "price": 9.2}
}

# Pre-packaged personas representing real-world Tier-2/3 investor loan profiles
INVESTOR_PERSONAS = {
    "persona_ramesh_high_risk": {
        "id": "persona_ramesh_high_risk",
        "name": "Ramesh Gupta",
        "location": "Indore, Madhya Pradesh",
        "tagline": "Small Business Owner | High-Beta Leveraged Borrower",
        "loan_type": "Digital Instant Loan Against Shares (LAS)",
        "lender": "FastCredit NBFC",
        "loan_outstanding": 380000.0,
        "lender_maintenance_ltv": 0.65,    # Warning / Margin Call triggers at 65%
        "lender_liquidation_ltv": 0.75,    # Forced sell-off at 75%
        "borrower_cash_buffer": 15000.0,   # Very low emergency liquidity
        "holdings": [
            {"symbol": "SUZLON", "units": 3200, "current_value": 249600.0},
            {"symbol": "ZOMATO", "units": 750, "current_value": 198750.0},
            {"symbol": "TATAPOWER", "units": 320, "current_value": 139200.0}
        ],
        "narrative": "Ramesh pledged his high-flying green energy and tech stocks for working capital. Because his portfolio is 100% high-beta, even a routine 7% market dip pushes his LTV past 70%."
    },
    "persona_priya_moderate": {
        "id": "persona_priya_moderate",
        "name": "Priya Sharma",
        "location": "Jaipur, Rajasthan",
        "tagline": "Salaried Professional | Balanced Mutual Fund Borrower",
        "loan_type": "Fintech App Loan Against Mutual Funds (LAMF)",
        "lender": "CapitalTrust Finance",
        "loan_outstanding": 420000.0,
        "lender_maintenance_ltv": 0.65,
        "lender_liquidation_ltv": 0.75,
        "borrower_cash_buffer": 85000.0,
        "holdings": [
            {"symbol": "PPFC_MF", "units": 5500, "current_value": 431750.0},
            {"symbol": "HDFCBANK", "units": 180, "current_value": 297000.0},
            {"symbol": "TATAMOTORS", "units": 235, "current_value": 225600.0}
        ],
        "narrative": "Priya pledged a mix of large-cap equity and diversified mutual funds for medical emergency funds. Her LTV is around 44%, offering a solid buffer against mild corrections."
    },
    "persona_sunita_conservative": {
        "id": "persona_sunita_conservative",
        "name": "Sunita Verma",
        "location": "Patna, Bihar",
        "tagline": "Retired School Principal | Defensive Portfolio",
        "loan_type": "Bank Overdraft Against Securities",
        "lender": "National Bank of India",
        "loan_outstanding": 250000.0,
        "lender_maintenance_ltv": 0.65,
        "lender_liquidation_ltv": 0.75,
        "borrower_cash_buffer": 200000.0,
        "holdings": [
            {"symbol": "TCS", "units": 120, "current_value": 504000.0},
            {"symbol": "ITC", "units": 650, "current_value": 315250.0},
            {"symbol": "HDFC_SHORT_DEBT", "units": 12000, "current_value": 388800.0}
        ],
        "narrative": "Sunita borrowed conservatively against dividend bluechips and debt funds. She has strong buffers and negligible risk of liquidation even during extreme market shocks."
    }
}

# Historical market crash stress-testing benchmarks
HISTORICAL_CRASH_SCENARIOS = [
    {
        "id": "covid_crash_2020",
        "name": "March 2020 COVID Panic",
        "broad_market_drop": -0.26,
        "description": "Nifty plunged 26% in 3 weeks. Smallcaps & high-beta stocks plummeted up to 40%."
    },
    {
        "id": "election_volatility_2024",
        "name": "June 4, 2024 Election Volatility",
        "broad_market_drop": -0.059,
        "description": "Nifty dropped 5.9% in a single trading session with midcaps falling over 8-12%."
    },
    {
        "id": "rate_hike_tightening_2022",
        "name": "2022 Global Rate Tightening",
        "broad_market_drop": -0.11,
        "description": "Prolonged multi-month correction of 11% driven by inflation and foreign institutional outflows."
    },
    {
        "id": "routine_correction_8pct",
        "name": "Routine Market Dip (-8%)",
        "broad_market_drop": -0.08,
        "description": "A standard healthy quarterly pullback. Tests whether the borrower is over-leveraged."
    }
]
