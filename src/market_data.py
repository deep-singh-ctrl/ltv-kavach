"""
Live Market Data Engine for Indian Equities & Mutual Funds.
Features live dynamic NSE/BSE search via yfinance Search and real-time quotes.
"""

import sys
pkg_path = "/home/deepank-singh/Documents/ltv-kavach/packages"
if pkg_path not in sys.path:
    sys.path.insert(0, pkg_path)

from typing import Dict, List, Any, Optional
import yfinance as yf

# Curated catalog of top popular Indian Equities, MFs & ETFs for instant 0ms response
POPULAR_INDIAN_CATALOG = [
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
    {"symbol": "TATAMOTORS", "name": "Tata Motors Ltd", "category": "Auto Mid/Large", "beta": 1.35, "haircut": 0.30, "base_price": 960.0, "nse_ticker": "TATAMOTORS.NS"},
    {"symbol": "EICHERMOT", "name": "Eicher Motors Ltd", "category": "Auto & Royal Enfield", "beta": 1.10, "haircut": 0.25, "base_price": 6920.0, "nse_ticker": "EICHERMOT.NS"},
    {"symbol": "TATAPOWER", "name": "Tata Power Co Ltd", "category": "Power & Energy", "beta": 1.55, "haircut": 0.35, "base_price": 435.0, "nse_ticker": "TATAPOWER.NS"},
    {"symbol": "SUZLON", "name": "Suzlon Energy Ltd", "category": "Small Cap High Beta", "beta": 2.15, "haircut": 0.50, "base_price": 78.0, "nse_ticker": "SUZLON.NS"},
    {"symbol": "ZOMATO", "name": "Zomato Ltd", "category": "High Growth Tech", "beta": 1.75, "haircut": 0.40, "base_price": 265.0, "nse_ticker": "ZOMATO.NS"},
    {"symbol": "PAYTM", "name": "One97 Communications (Paytm)", "category": "Fintech High Beta", "beta": 2.10, "haircut": 0.55, "base_price": 680.0, "nse_ticker": "PAYTM.NS"},
    {"symbol": "NIFTYBEES", "name": "Nippon India Nifty 50 ETF", "category": "Index ETF", "beta": 1.00, "haircut": 0.15, "base_price": 275.0, "nse_ticker": "NIFTYBEES.NS"},
    {"symbol": "GOLDBEES", "name": "Nippon India Gold ETF", "category": "Commodity ETF", "beta": 0.15, "haircut": 0.15, "base_price": 68.5, "nse_ticker": "GOLDBEES.NS"},
    {"symbol": "PPFC_MF", "name": "Parag Parikh Flexi Cap Fund", "category": "Diversified Equity MF", "beta": 0.85, "haircut": 0.25, "base_price": 78.5, "nse_ticker": None},
    {"symbol": "HDFC_SHORT_DEBT", "name": "HDFC Short Term Debt Fund", "category": "Debt Mutual Fund", "beta": 0.05, "haircut": 0.10, "base_price": 32.4, "nse_ticker": None},
    {"symbol": "ICICI_LIQUID", "name": "ICICI Prudential Liquid Fund", "category": "Liquid Mutual Fund", "beta": 0.02, "haircut": 0.10, "base_price": 355.0, "nse_ticker": None}
]

STOCK_LOOKUP = {s["symbol"]: s for s in POPULAR_INDIAN_CATALOG}

def search_indian_stocks(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    """
    Searches both curated Indian catalog AND queries live Yahoo Finance for any NSE/BSE listed stock.
    """
    q = query.strip()
    if not q:
        return POPULAR_INDIAN_CATALOG[:limit]

    q_upper = q.upper()
    seen_symbols = set()
    results = []

    # 1. First, check curated catalog for instant matches
    for s in POPULAR_INDIAN_CATALOG:
        if q_upper in s["symbol"] or q_upper in s["name"].upper() or q_upper in s["category"].upper():
            results.append(s)
            seen_symbols.add(s["symbol"])
            if len(results) >= limit:
                return results

    # 2. Query live Yahoo Finance Search API for any Indian stock (e.g. Eicher Motors, Adani, MRF, etc.)
    try:
        search_res = yf.Search(q, max_results=12)
        if search_res and search_res.quotes:
            for item in search_res.quotes:
                raw_sym = item.get("symbol", "")
                # Only include Indian exchanges: NSE (.NS) or BSE (.BO)
                if ".NS" in raw_sym or ".BO" in raw_sym:
                    clean_sym = raw_sym.replace(".NS", "").replace(".BO", "").upper()
                    if clean_sym in seen_symbols:
                        continue
                    seen_symbols.add(clean_sym)

                    company_name = item.get("longname") or item.get("shortname") or clean_sym
                    sector = item.get("sector") or item.get("industry") or ("NSE Equity" if ".NS" in raw_sym else "BSE Equity")
                    
                    # Try to get live price or default
                    est_price = 0.0
                    try:
                        t = yf.Ticker(raw_sym)
                        p = t.fast_info.last_price
                        if p and p > 0:
                            est_price = round(float(p), 2)
                    except Exception:
                        pass

                    results.append({
                        "symbol": clean_sym,
                        "name": company_name,
                        "category": sector,
                        "beta": 1.15,
                        "haircut": 0.25,
                        "base_price": est_price if est_price > 0 else 100.0,
                        "nse_ticker": raw_sym
                    })
                    if len(results) >= limit:
                        break
    except Exception as e:
        print(f"[Market Data Search Error] {e}")

    return results

def fetch_live_stock_quote(symbol: str) -> Dict[str, Any]:
    """
    Fetches real-time price, beta, and haircut for any stock on NSE.
    """
    sym = symbol.strip().upper().replace(".NS", "").replace(".BO", "")
    meta = STOCK_LOOKUP.get(sym)

    price = meta.get("base_price", 100.0) if meta else 100.0
    name = meta.get("name", sym) if meta else sym
    category = meta.get("category", "Equity") if meta else "Equity"
    beta = meta.get("beta", 1.15) if meta else 1.15
    haircut = meta.get("haircut", 0.25) if meta else 0.25
    source = "cached"

    # Try live NSE ticker
    nse_tickers = [f"{sym}.NS", f"{sym}.BO", sym]
    for ticker_sym in nse_tickers:
        try:
            ticker = yf.Ticker(ticker_sym)
            fast_price = ticker.fast_info.last_price
            if fast_price and fast_price > 0:
                price = round(float(fast_price), 2)
                source = "live_nse"
                # If name wasn't in catalog, retrieve info name
                if not meta or meta["name"] == sym:
                    try:
                        n = ticker.fast_info.get("longName") or ticker.fast_info.get("shortName")
                        if n:
                            name = n
                    except Exception:
                        pass
                break
        except Exception:
            continue

    return {
        "symbol": sym,
        "name": name,
        "category": category,
        "price": price,
        "beta": beta,
        "haircut": haircut,
        "data_source": source
    }
