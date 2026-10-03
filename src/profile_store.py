"""
Persistence & Custom User Profile Management.
Stores user-created portfolios in JSON and parses imported CSV statements.
"""

import os
import json
import uuid
import csv
import io
from typing import List, Dict, Any, Optional
from src.market_data import fetch_live_stock_quote

PROFILES_FILE = "/home/deepank-singh/Documents/ltv-kavach/data/custom_profiles.json"

def _ensure_file():
    os.makedirs(os.path.dirname(PROFILES_FILE), exist_ok=True)
    if not os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "w") as f:
            json.dump([], f)

def list_custom_profiles() -> List[Dict[str, Any]]:
    _ensure_file()
    try:
        with open(PROFILES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_custom_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    _ensure_file()
    profiles = list_custom_profiles()
    
    prof_id = profile.get("id") or f"custom_{uuid.uuid4().hex[:8]}"
    profile["id"] = prof_id

    # Compute live current value for all holdings
    total_collateral = 0.0
    for h in profile.get("holdings", []):
        sym = h.get("symbol", "").upper()
        units = float(h.get("units", 1))
        # If price not supplied, fetch live quote
        if "price" not in h or h["price"] <= 0:
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
    profile["current_ltv_pct"] = round((loan / max(total_collateral, 1.0)) * 100.0, 1)

    # Upsert
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
    """
    Parses CSV text with flexible headers (Symbol/Ticker, Units/Quantity, Price/Value).
    """
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
