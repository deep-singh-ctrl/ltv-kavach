# 🛡️ LTV-Kavach (एलटीवी कवच)
### Public-Good Investor Resilience & Collateral Guardian for Loan Against Securities (LAS)
**Submission for SEBI • NSDL SANGYAN Investor Resilience Hackathon 2026**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Cloudflare_HTTPS-emerald.svg)](https://sparc-draw-affected-walking.trycloudflare.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-deep--singh--ctrl%2Fltv--kavach-blue.svg)](https://github.com/deep-singh-ctrl/ltv-kavach)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Regulatory](https://img.shields.io/badge/Regulatory-SEBI%20%7C%20RBI%20LAS-emerald.svg)](#-regulatory-protection--borrower-rights)
[![Bilingual](https://img.shields.io/badge/Language-English%20%7C%20हिन्दी%20(100%25)-amber.svg)](#-key-highlights)

---

## 🌐 Live Application Link

> **Try the Live App Now**: **[https://sparc-draw-affected-walking.trycloudflare.com](https://sparc-draw-affected-walking.trycloudflare.com)**  
> *(Live public link. No login or installation required. Works on desktop and mobile).*

---

## 📌 What is LTV-Kavach?

In India today, taking a **Loan Against Securities (LAS)** or **Loan Against Mutual Funds (LAMF)** takes under 5 minutes via instant Demat OTP. Millions of retail investors pledge their long-term investments for emergency cash.

However, when stock markets dip, a dangerous trap occurs:
- **Your loan debt stays fixed**, but your pledged stock value drops.
- This causes your **Loan-to-Value (LTV)** ratio to shoot up toward bank margin calls (65%) and forced liquidation (75%).
- Borrowers panic, unaware of their legal rights or that they can resolve the shortfall with **₹0 cash** simply by pledging additional unpledged shares.

**LTV-Kavach** solves this. It is a calm, public-good web application that protects retail borrowers by translating complex margin math into plain language and calm, actionable steps.

---

## 🚶‍♂️ The Simple 2-Step Journey

```
┌────────────────────────────────────────────────────────────────────────┐
│  STEP 1: LOAN HEALTH & COLLATERAL SENSITIVITY                          │
│  • Visual Risk Meter: Safe (<50%), Warning (50-65%), Sell Risk (>65%) │
│  • Buffer to Bank Warning: "How much can the market fall before alert?"│
│  • Monthly Interest Burden: Live ₹/month cost at 10.5% p.a.            │
│  • Bluechip Swap Simulation: Replace volatile smallcaps with Nifty 50  │
├────────────────────────────────────────────────────────────────────────┤
│  STEP 2: MARKET CRASH SIMULATOR & CALM RESTORATION                     │
│  • Interactive Market Dip Slider (-0% to -35%) with Quick Presets      │
│  • Unpaid Interest Horizon: Simulates debt creep (+30d, +60d, +90d)    │
│  • Drawing Power vs Gross LTV based on regulatory stock haircuts       │
│  • Per-Stock Crash Breakdown (Beta-weighted individual asset drops)    │
│  • Live Equity Cushion Visualizer (Your net wealth buffer)             │
│  • 2-Option Calm Recovery Plan: Cash Prepayment vs Zero-Cash Demat OTP │
└────────────────────────────────────────────────────────────────────────┘
```

### Step 1: Loan Health & Sensitivity Check
- **Color-Coded Risk Meter**: Clearly displays your LTV zone (Green: Safe `<50%`, Amber: Warning `50%-65%`, Red: Danger `>65%`).
- **Safety Buffer**: Tells you in plain words: *"How much can the market fall before the bank issues a warning?"*
- **Portfolio Sensitivity & Bluechip Swap**: Shows whether your pledged collateral is made of volatile smallcaps. One click simulates swapping a high-risk stock with a stable Nifty 50 stock to widen your cushion.
- **Monthly Interest Burden**: Tracks ongoing interest costs ($10.5\% \text{ p.a.}$) in ₹/month.

### Step 2: Market Crash Simulator & Calm Recovery
- **Interactive Market Dip Slider**: Drag the slider from $0\%$ to $-35\%$ (or click quick presets: June 4 dip `-6%`, correction `-12%`, crash `-25%`) to see what happens to your loan tomorrow.
- **Accrued Interest Horizon**: Simulates the silent debt creep if interest is left unpaid for 30, 60, or 90 days ($D_{\text{effective}} = D_{\text{principal}} + \frac{D \cdot r \cdot t}{365}$).
- **Drawing Power vs Gross LTV**: Calculates eligible borrowing power using official regulatory haircuts (15% for Debt funds, 20% for Bluechips, 50% for Smallcaps).
- **Asset-by-Asset Impact**: Shows individual price drops based on each stock's beta.
- **Calm 2-Option Recovery Plan** *(No Panic!)*:
  1. **Option 1: Cash Paydown via UPI** — Exact ₹ needed to restore a safe 45% LTV, plus the monthly interest you permanently save.
  2. **Option 2: Zero-Cash Demat OTP Pledge** — Exact number of shares (e.g., Reliance or Debt MF units) to pledge via instant NSDL OTP—requiring **₹0 cash**.

---

## ⚖️ Regulatory Protection & Borrower Rights (SEBI & RBI)

LTV-Kavach teaches borrowers the rights lenders often hide:

| Regulatory Feature | Regulatory Rule | Borrower Benefit |
| :--- | :--- | :--- |
| **Demat Custody & Ownership** | SEBI Margin Pledge Circulars | Pledged shares remain in your own Demat account under lien. You retain **100% of dividends, bonuses, and rights issues**. |
| **Statutory 7-Day Cure Window** | RBI Prudential Norms for LAS | Banks cannot immediately dump your shares. You have a legal notice window (up to 7 working days) to restore margin. |
| **No Silent Liquidation** | Depository Regulations (NSDL/CDSL) | Depositories send official SMS and email alerts directly to your mobile number, preventing secret lender sales. |
| **Right to Cure via Collateral** | RBI Master Direction | Borrowers are **never forced to pay cash**. Pledging unpledged bluechips or Debt Mutual Funds via instant OTP immediately restores the margin. |

---

## 💡 Key Highlights

| Feature | Description |
| :--- | :--- |
| **🌐 Live Cloud Link** | Accessible online via secure HTTPS tunnel: [Try Live Demo](https://sparc-draw-affected-walking.trycloudflare.com). |
| **🇮🇳 100% Bilingual (Hindi ⇄ English)** | Full interface toggle with spoken vernacular voice guidance (`SpeechSynthesis`). |
| **🎓 First-Time Borrower Guide** | 4 simple interactive lessons on LTV formulas, legal rights, beta volatility, and zero-cash pledging. |
| **📄 1-Page Resilience Certificate** | Generates a clean, printable PDF report for the borrower (`Ctrl+P` / Print button). |
| **📈 Live NSE Quotes & CSV Importer** | Search active NSE stocks or paste broker statements (`SYMBOL, UNITS`). |
| **🛡️ 100% Public Good** | Zero stock tips, zero loan referral commissions, zero commercial bias. |

---

## ⚡ Quickstart (Run Locally)

### 1. Clone & Run
```bash
git clone https://github.com/deep-singh-ctrl/ltv-kavach.git
cd ltv-kavach
./run.sh
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

### 2. Run Automated Tests
```bash
python3 -c "import tests.test_risk_engine as t; [getattr(t, f)() for f in dir(t) if f.startswith('test_')]; print('All 9 tests passed!')"
```

---

## 🏆 Hackathon Alignment (SEBI • NSDL SANGYAN 2026)

- **Track D (Behavioural Resilience)**: Replaces panic borrowing with calm, quantitative zero-cash Demat OTP recovery.
- **Track C (Investor Education for Bharat)**: Bilingual Hindi/English parity, audio readouts, plain language tooltips, and Demat rights awareness.
- **Regulatory Integrity**: Built strictly around SEBI and RBI Master Directions for Loan Against Securities (LAS).

---

## 📜 License
Distributed under the **MIT Open Source License** for public good financial literacy and investor resilience. Built for **SEBI • NSDL SANGYAN 2026**.
