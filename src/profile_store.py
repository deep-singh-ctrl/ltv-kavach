"""
Persistence & Custom User Profile Management.
Stores all profiles (including initial presets) in JSON so ANY profile can be deleted or edited.
"""

import os
import json
import uuid
import csv
import io
from typing import List, Dict, Any, Optional
from src.market_data import fetch_live_stock_quote

PROFILES_FILE = "/home/deepank-singh/Documents/ltv-kavach/data/custom_profiles.json"

DEFAULT_INITIAL_PROFILES = [
    {
        "id": "persona_ramesh_high_risk",
        "name": "Ramesh Gupta",
        "borrower_name": "Ramesh Gupta",
        "location": "Indore, MP",
        "desc": "Small Business Owner | Smallcaps",
        "loan_outstanding": 380000.0,
        "lender": "FastCredit NBFC",
        "holdings": [
            {"symbol": "SUZLON", "name": "Suzlon Energy Ltd", "units": 3200, "price": 78.0, "current_value": 249600.0, "beta": 2.15, "haircut": 0.50},
            {"symbol": "ZOMATO", "name": "Zomato Ltd", "units": 750, "price": 265.0, "current_value": 198750.0, "beta": 1.75, "haircut": 0.40},
            {"symbol": "TATAPOWER", "name": "Tata Power Co Ltd", "units": 320, "price": 435.0, "current_value": 139200.0, "beta": 1.55, "haircut": 0.35}
        ],
        "total_collateral": 587550.0,
        "current_ltv_pct": 64.7,
        "badge": "65% LTV (At Risk)",
        "badge_class": "bg-rose-100 text-rose-700 border-rose-200"
    },
    {
        "id": "persona_priya_moderate",
        "name": "Priya Sharma",
        "borrower_name": "Priya Sharma",
        "location": "Jaipur, RJ",
        "desc": "Salaried Professional | Balanced MF",
        "loan_outstanding": 420000.0,
        "lender": "CapitalTrust Finance",
        "holdings": [
            {"symbol": "PPFC_MF", "name": "Parag Parikh Flexi Cap Fund", "units": 5500, "price": 78.5, "current_value": 431750.0, "beta": 0.85, "haircut": 0.25},
            {"symbol": "HDFCBANK", "name": "HDFC Bank Ltd", "units": 180, "price": 1650.0, "current_value": 297000.0, "beta": 0.92, "haircut": 0.20},
            {"symbol": "TATAMOTORS", "name": "Tata Motors Ltd", "units": 235, "price": 960.0, "current_value": 225600.0, "beta": 1.35, "haircut": 0.30}
        ],
        "total_collateral": 954350.0,
        "current_ltv_pct": 44.0,
        "badge": "44% LTV (Caution)",
        "badge_class": "bg-amber-50 text-amber-700 border-amber-200"
    },
    {
        "id": "persona_sunita_conservative",
        "name": "Sunita Verma",
        "borrower_name": "Sunita Verma",
        "location": "Patna, BR",
        "desc": "Retired Principal | Bluechip & Debt",
        "loan_outstanding": 250000.0,
        "lender": "National Bank of India",
        "holdings": [
            {"symbol": "TCS", "name": "Tata Consultancy Services Ltd", "units": 120, "price": 2075.0, "current_value": 249000.0, "beta": 0.78, "haircut": 0.20},
            {"symbol": "ITC", "name": "ITC Ltd", "units": 650, "price": 485.0, "current_value": 315250.0, "beta": 0.65, "haircut": 0.20},
            {"symbol": "HDFC_SHORT_DEBT", "name": "HDFC Short Term Debt Fund", "units": 12000, "price": 32.4, "current_value": 388800.0, "beta": 0.05, "haircut": 0.10}
        ],
        "total_collateral": 953050.0,
        "current_ltv_pct": 26.2,
        "badge": "26% LTV (Safe)",
        "badge_class": "bg-emerald-50 text-emerald-700 border-emerald-200"
    }
]

def _ensure_file():
    os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)
    if not os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "w") as f:
            json.dump(DEFAULT_INITIAL_PROFILES, f, indent=2)

def list_custom_profiles() -> List[Dict[str, Any]]:
    _ensure_file()
    try:
        with open(PROFILES_FILE, "r") as f:
            data = json.load(f)
            if not data:
                # Re-seed if completely empty
                return DEFAULT_INITIAL_PROFILES
            return data
    except Exception:
        return DEFAULT_INITIAL_PROFILES

def save_custom_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_file()
    profiles = list_custom_profiles()
    
    prof_id = profile.get("id") or f"custom_{uuid.uuid4().hex[:8]}"
    profile["id"] = prof_id

    total_collateral = 0.0
    for h in profile.get("holdings", []):
        sym = h.get("symbol", "").upper()
        units = float(h.get("units", 1))
        if "price" not in h or float(h.get("price", 0)) <= 0:
            quote = fetch_live_stock_quote(sym)
            h["price"] = quote["price"]
            h["beta"] = quote["beta"]
            h["haircut"] = quote["haircut"]
            h["name"] = quote["name"]
        
        current_val = round(units * float(h["price"]), 2)
        h["current_value"] = current_val
        total_collateral += current_val

    profile["total_collateral"] = round(total_collateral, 2)
    loan = float(profile.get("loan_outstanding", 0.0))
    ltv = round((loan / max(total_collateral, 1.0)) * 100.0, 1)
    profile["current_ltv_pct"] = ltv

    if ltv < 50.0:
        profile["badge"] = f"{ltv}% LTV (Safe)"
        profile["badge_class"] = "bg-emerald-50 text-emerald-700 border-emerald-200"
    elif ltv < 65.0:
        profile["badge"] = f"{ltv}% LTV (Caution)"
        profile["badge_class"] = "bg-amber-50 text-amber-700 border-amber-200"
    else:
        profile["badge"] = f"{ltv}% LTV (At Risk)"
        profile["badge_class"] = "bg-rose-100 text-rose-700 border-rose-200"

    existing_idx = next((i for i, p in enumerate(profiles) if p["id"] == prof_id), None)
    if existing_idx is not None:
        profiles[existing_idx] = profile
    else:
        profiles.append(profile)

    with open(PROFILES_FILE, "w") as f:
        json.dump(profiles, f, indent=2)

    return profile

def delete_custom_profile(prof_id: str) -> bool:
    _ensure_file()
    profiles = list_custom_profiles()
    filtered = [p for p in profiles if p["id"] != prof_id]
    if len(filtered) != len(profiles):
        with open(PROFILES_FILE, "w") as f:
            json.dump(filtered, f, indent=2)
        return True
    return False

def parse_csv_statement(csv_content: str) -> List[Dict[str, Any]]:
    holdings = []
    reader = csv.reader(io.StringIO(csv_content.strip()))
    header = None

    for row in reader:
        if not row or not any(row):
            continue
        cleaned = [c.strip() for c in row]
        if header is None:
            header = [h.lower() for h in cleaned]
            continue

        row_dict = dict(zip(header, cleaned))
        sym = row_dict.get("symbol") or row_dict.get("ticker") or row_dict.get("stock") or (cleaned[0] if len(cleaned) > 0 else "")
        units_str = row_dict.get("units") or row_dict.get("quantity") or row_dict.get("qty") or (cleaned[1] if len(cleaned) > 1 else "1")

        if not sym:
            continue

        try:
            units = float(units_str)
        except ValueError:
            units = 1.0

        quote = fetch_live_stock_quote(sym)
        holdings.append({
            "symbol": quote["symbol"],
            "name": quote["name"],
            "category": quote["category"],
            "units": units,
            "price": quote["price"],
            "current_value": round(units * quote["price"], 2),
            "beta": quote["beta"],
            "haircut": quote["haircut"]
        })

    return holdings
