"""
Live Market Data Engine for Indian Equities & Mutual Funds.
Integrates yfinance for real-time NSE prices with cached fallback and autocomplete search.
"""

import sys
pkg_path = "/home/deepank-singh/Documents/ltv-kavach/packages"
if pkg_path not in sys.path:
    sys.path.insert(0, pkg_path)

from typing import Dict, List, Any, Optional
import yfinance as yf

# Comprehensive Master Catalog of Indian Equities, MFs & ETFs
INDIAN_STOCKS_CATALOG = [
    # Top Large Caps
    {"symbol": "RELIANCE", "name": "Reliance Industries Ltd", "category": "Large Cap", "beta": 0.95, "haircut": 0.20, "base_price": 1168.0, "nse_ticker": "RELIANCE.NS"},
    {"symbol": "TCS", "name": "Tata Consultancy Services Ltd", "category": "Large Cap", "beta": 0.78, "haircut": 0.20, "base_price": 2075.0, "nse_ticker": "TCS.NS"},
    {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd", "category": "Large Cap", "beta": 0.92, "haircut": 0.20, "base_price": 1650.0, "nse_ticker": "HDFCBANK.NS"},
    {"symbol": "INFY", "name": "Infosys Ltd", "category": "Large Cap", "beta": 0.88, "haircut": 0.20, "base_price": 1820.0, "nse_ticker": "INFY.NS"},
    {"symbol": "ICICIBANK", "name": "ICICI Bank Ltd", "category": "Large Cap", "beta": 0.96, "haircut": 0.20, "base_price": 1240.0, "nse_ticker": "ICICIBANK.NS"},
    {"symbol": "ITC", "name": "ITC Ltd", "category": "Large Cap", "beta": 0.65, "haircut": 0.20, "base_price": 485.0, "nse_ticker": "ITC.NS"},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel Ltd", "category": "Large Cap", "beta": 0.82, "haircut": 0.20, "base_price": 1640.0, "nse_ticker": "BHARTIARTL.NS"},
    {"symbol": "SBIN", "name": "State Bank of India", "category": "Large Cap PSU", "beta": 1.15, "haircut": 0.25, "base_price": 790.0, "nse_ticker": "SBIN.NS"},
    {"symbol": "LT", "name": "Larsen & Toubro Ltd", "category": "Large Cap Infrastructure", "beta": 0.90, "haircut": 0.20, "base_price": 3520.0, "nse_ticker": "LT.NS"},
    {"symbol": "BAJFINANCE", "name": "Bajaj Finance Ltd", "category": "Large Cap NBFC", "beta": 1.25, "haircut": 0.25, "base_price": 6850.0, "nse_ticker": "BAJFINANCE.NS"},

    # Popular Midcaps & Growth Stocks
    {"symbol": "TATAMOTORS", "name": "Tata Motors Ltd", "category": "Auto Mid/Large", "beta": 1.35, "haircut": 0.30, "base_price": 960.0, "nse_ticker": "TATAMOTORS.NS"},
    {"symbol": "TATAPOWER", "name": "Tata Power Co Ltd", "category": "Power & Energy", "beta": 1.55, "haircut": 0.35, "base_price": 435.0, "nse_ticker": "TATAPOWER.NS"},
    {"symbol": "TATASTEEL", "name": "Tata Steel Ltd", "category": "Metals / Cyclical", "beta": 1.45, "haircut": 0.35, "base_price": 158.0, "nse_ticker": "TATASTEEL.NS"},
    {"symbol": "POLYCAB", "name": "Polycab India Ltd", "category": "Mid Cap Wires", "beta": 1.25, "haircut": 0.30, "base_price": 6450.0, "nse_ticker": "POLYCAB.NS"},
    {"symbol": "FEDERALBNK", "name": "Federal Bank Ltd", "category": "Mid Cap Bank", "beta": 1.30, "haircut": 0.35, "base_price": 185.0, "nse_ticker": "FEDERALBNK.NS"},
    {"symbol": "TRENT", "name": "Trent Ltd", "category": "High Growth Retail", "beta": 1.40, "haircut": 0.30, "base_price": 7400.0, "nse_ticker": "TRENT.NS"},
    {"symbol": "HAL", "name": "Hindustan Aeronautics Ltd", "category": "Defense PSU", "beta": 1.30, "haircut": 0.30, "base_price": 4250.0, "nse_ticker": "HAL.NS"},
    {"symbol": "BEL", "name": "Bharat Electronics Ltd", "category": "Defense PSU", "beta": 1.20, "haircut": 0.30, "base_price": 285.0, "nse_ticker": "BEL.NS"},
    {"symbol": "IRCTC", "name": "IRCTC Ltd", "category": "PSU Tourism", "beta": 1.25, "haircut": 0.35, "base_price": 890.0, "nse_ticker": "IRCTC.NS"},

    # High Beta / Small Caps
    {"symbol": "SUZLON", "name": "Suzlon Energy Ltd", "category": "Small Cap High Beta", "beta": 2.15, "haircut": 0.50, "base_price": 78.0, "nse_ticker": "SUZLON.NS"},
    {"symbol": "ZOMATO", "name": "Zomato Ltd", "category": "High Growth Tech", "beta": 1.75, "haircut": 0.40, "base_price": 265.0, "nse_ticker": "ZOMATO.NS"},
    {"symbol": "PAYTM", "name": "One97 Communications (Paytm)", "category": "Fintech High Beta", "beta": 2.10, "haircut": 0.55, "base_price": 680.0, "nse_ticker": "PAYTM.NS"},
    {"symbol": "YESBANK", "name": "Yes Bank Ltd", "category": "Distressed Banking", "beta": 2.25, "haircut": 0.55, "base_price": 21.5, "nse_ticker": "YESBANK.NS"},
    {"symbol": "IDEA", "name": "Vodafone Idea Ltd", "category": "Penny Telecom", "beta": 2.45, "haircut": 0.60, "base_price": 9.2, "nse_ticker": "IDEA.NS"},
    {"symbol": "IREDA", "name": "Indian Renewable Energy Agency", "category": "Green PSU", "beta": 1.85, "haircut": 0.45, "base_price": 225.0, "nse_ticker": "IREDA.NS"},
    {"symbol": "RVNL", "name": "Rail Vikas Nigam Ltd", "category": "Railway PSU", "beta": 1.95, "haircut": 0.45, "base_price": 490.0, "nse_ticker": "RVNL.NS"},

    # Mutual Funds & Safe Collateral ETFs
    {"symbol": "NIFTYBEES", "name": "Nippon India Nifty 50 ETF", "category": "Index ETF", "beta": 1.00, "haircut": 0.15, "base_price": 275.0, "nse_ticker": "NIFTYBEES.NS"},
    {"symbol": "GOLDBEES", "name": "Nippon India Gold ETF", "category": "Commodity ETF", "beta": 0.15, "haircut": 0.15, "base_price": 68.5, "nse_ticker": "GOLDBEES.NS"},
    {"symbol": "BANKBEES", "name": "Nippon India Nifty Bank ETF", "category": "Banking ETF", "beta": 1.10, "haircut": 0.20, "base_price": 525.0, "nse_ticker": "BANKBEES.NS"},
    {"symbol": "PPFC_MF", "name": "Parag Parikh Flexi Cap Fund", "category": "Diversified Equity MF", "beta": 0.85, "haircut": 0.25, "base_price": 78.5, "nse_ticker": None},
    {"symbol": "HDFC_SHORT_DEBT", "name": "HDFC Short Term Debt Fund", "category": "Debt Mutual Fund", "beta": 0.05, "haircut": 0.10, "base_price": 32.4, "nse_ticker": None},
    {"symbol": "ICICI_LIQUID", "name": "ICICI Prudential Liquid Fund", "category": "Liquid Mutual Fund", "beta": 0.02, "haircut": 0.10, "base_price": 355.0, "nse_ticker": None}
]

# Lookup dictionary by uppercase symbol
STOCK_LOOKUP = {s["symbol"]: s for s in INDIAN_STOCKS_CATALOG}

def search_indian_stocks(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    """
    Autocomplete search across symbol and company name.
    """
    q = query.strip().upper()
    if not q:
        return INDIAN_STOCKS_CATALOG[:limit]

    matches = []
    for s in INDIAN_STOCKS_CATALOG:
        if q in s["symbol"] or q in s["name"].upper() or q in s["category"].upper():
            matches.append(s)
            if len(matches) >= limit:
                break
    return matches

def fetch_live_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Fetches live market price via yfinance fast_info with instant cached fallback.
    """
    sym = symbol.strip().upper()
    meta = STOCK_LOOKUP.get(sym, {
        "symbol": sym,
        "name": sym,
        "category": "Equity",
        "beta": 1.20,
        "haircut": 0.35,
        "base_price": 100.0,
        "nse_ticker": f"{sym}.NS"
    })

    price = meta.get("base_price", 100.0)
    source = "cached_catalog"

    nse_ticker = meta.get("nse_ticker") or f"{sym}.NS"
    try:
        ticker = yf.Ticker(nse_ticker)
        fast_price = ticker.fast_info.last_price
        if fast_price and fast_price > 0:
            price = round(float(fast_price), 2)
            source = "live_nse"
    except Exception as e:
        # Fall back gracefully to base price without breaking UI
        pass

    return {
        "symbol": sym,
        "name": meta.get("name", sym),
        "category": meta.get("category", "Equity"),
        "price": price,
        "beta": meta.get("beta", 1.20),
        "haircut": meta.get("haircut", 0.35),
        "data_source": source
    }
