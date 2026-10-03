# 🛡️ LTV-Kavach (एलटीवी कवच)
### Public-Good Investor Resilience & Collateral Guardian for Loan Against Securities (LAS)
**Submission for SEBI • NSDL SANGYAN Investor Resilience Hackathon 2026**
*Track: Financial Habits & Behavioural Resilience (Track D) & Investor Education for Bharat (Track C) / Open Track*

---

## 📌 1. The Core Problem
With digital NBFCs and fintech apps offering instant **Loan Against Securities (LAS)** and **Loan Against Mutual Funds (LAMF)** in under 5 minutes, millions of retail investors in Tier-2/3 cities pledge their long-term portfolios for quick liquidity.

### The Hidden Trap:
* **The Vulnerability**: When markets experience normal volatility, the **Loan-to-Value (LTV)** ratio spikes:
  $$\text{LTV} = \frac{\text{Loan Outstanding}}{\text{Current Market Value of Pledged Securities}}$$
* **The Catastrophe**: Once LTV breaches maintenance thresholds (e.g. 65%–75%), lenders issue emergency margin calls. If unfulfilled within hours, the lender forcefully liquidates the investor's assets at bottom-of-the-market prices, wiping out years of compounding wealth.
* **Why Normal Users Fail**: Retail investors cannot calculate portfolio beta or volatility haircuts in their heads. They realize they are in danger only when the liquidation SMS arrives.

---

## 🚀 2. The Solution: LTV-Kavach
**LTV-Kavach** acts as an intelligent shield and early warning guardian for leveraged retail investors. It does **not** give speculative stock tips or sell financial products; it is 100% focused on **capital preservation and loss prevention**.

### Guided Step-by-Step User Flow:
Rather than overwhelming the user with a single long scrolling page, LTV-Kavach features a **structured left-sidebar navigation** and a **guided 4-step user journey**:

1. **Step 1: Real-Time Loan Health & LTV Radar**:
   * Visual semi-circular speedometer with color-coded safety zones:
     * **Green (<50%)**: Safe & Resilient.
     * **Yellow (50%–65%)**: Caution (Buffer narrowing).
     * **Amber (65%–75%)**: Margin Call Active.
     * **Red (>75%)**: Liquidation Danger.
   * Displays exact **Distance to Margin Call** in percentage drop and rupee buffer.

2. **Step 2: Explainable ML Vulnerability Diagnostic**:
   * Scikit-Learn **Random Forest Classifier** predicting 90-day margin call breach probability ($P(\text{Breach})$).
   * **Explainable AI Attribution**: Breaks down root causes into plain terms (e.g., *78% concentration in high-beta midcaps*, *58% starting leverage*, *thin cash liquidity*).

3. **Step 3: Consequence Crash Stress Simulator**:
   * Interactive slider from 0% to -40% market drawdowns.
   * Real-time recalculation using individual stock betas ($\beta$).
   * Historical benchmark stress tests:
     * **March 2020 COVID Panic (-26%)**
     * **June 4, 2024 Election Volatility (-5.9%)**
     * **2022 Global Rate Tightening (-11%)**

4. **Step 4: Your Resilience & Buffer Action Plan (The Solution)**:
   * **Option 1 (Cash Prepayment)**: Exact rupee amount to pay down to restore a bulletproof 45% LTV.
   * **Option 2 (Safe Collateral Top-Up)**: Exact rupee value of low-volatility Debt MFs or Liquid ETFs to pledge without spending cash.
   * **Option 3 (20% Crash Shield)**: Required liquidity reserve to survive a 20% crash without ever triggering a margin call.

### Complementary Investor Utilities (In Sidebar):
* **"Before You Pledge" Pre-Loan Sandbox**: Test proposed loan borrowing limits and get SEBI-aligned prudent borrowing caps before signing loan agreements.
* **Collateral Roster**: Full breakdown of individual securities, units, market value, individual betas, and NBFC haircuts.
* **NSDL Depository Alert Hub**: Live mock preview of automated depository SMS & WhatsApp alerts.
* **Bharat-First Voice Guidance**: One-click audio narration in everyday Hindi & English.

---

## 🏗️ 3. Tech Stack Architecture

```
┌────────────────────────────────────────────────────────┐
│                   FRONTEND (Web Client)                │
│  • HTML5 + Tailwind CSS (Responsive Slate Dark Theme)  │
│  • SVG Speedometer Dial (Dynamic CSS Transformations)  │
│  • Lucide Icons + Browser Native Web Speech API        │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON
┌───────────────────────────▼────────────────────────────┐
│                  BACKEND (FastAPI Server)              │
│  • src/api.py: REST Endpoints (Analyze, Stress, Rem.)  │
│  • src/risk_engine.py: Quantitative Finance Formulas   │
│  • src/ml_model.py: Explainable Random Forest Model    │
│  • src/vernacular_engine.py: Hindi/English Voice Logic │
│  • src/data_store.py: Indian Assets, Personas, Scenarios│
└────────────────────────────────────────────────────────┘
```

---

## 🎯 4. Mapping to SANGYAN Evaluation Criteria

| Hackathon Criteria | Weight | How LTV-Kavach Delivers |
| :--- | :---: | :--- |
| **Resilience & Safety Impact** | **30%** | Measurably prevents catastrophic forced portfolio liquidations through early warning buffers and crash simulations. |
| **Tier-2/3 Usability (Bharat-First)** | **25%** | Native Hindi/English toggle, browser voice guidance, visual traffic-light meters, zero jargon. |
| **Guardrail Compliance & Trust** | **15%** | **Strictly compliant**: No stock tips, no trading algorithms, no loan broker commissions, no commercial upsells. |
| **Technical Execution** | **15%** | Quantitative beta-weighting, Scikit-Learn Random Forest with feature importance explainability, automated test suite. |
| **Feasibility & Scalability** | **15%** | Readily pluggable into NSDL/CDSL depository pledge APIs and the Account Aggregator (AA) framework. |

---

## 🎬 5. Suggested 3–5 Minute Hackathon Video Script

* **0:00 - 0:45 (The Problem)**: Show how Ramesh, a small business owner in Indore, pledged his shares for quick capital. A routine market dip caused NBFC margin liquidation, wiping out his portfolio.
* **0:45 - 1:30 (Onboarding & LTV Radar)**: Select **Ramesh Gupta** on the dashboard. Point out the LTV Speedometer (64.7% - Amber zone) and explain that a mere 7.6% drop will trigger liquidation.
* **1:30 - 2:15 (Explainable ML Radar)**: Highlight the **Random Forest Vulnerability Score (78/100)**. Explain the root causes: High Beta (1.82) and Single Stock Concentration.
* **2:15 - 3:00 (Stress Testing & Voice Guidance)**: Drag the Market Shock Slider to -10%. Show the LTV jump to 73.1% and the warning turn Red. Click the **Hindi Voice Button** to play the audio warning aloud.
* **3:00 - 3:45 (Actionable Buffer Plan)**: Walk through the 3 remedies: Pay ₹35,000 cash OR pledge ₹52,000 in safe debt funds to make the position 100% crash-proof.
* **3:45 - 4:15 (Depository Alert & Conclusion)**: Open the NSDL Mock Alert modal showing how depositories can protect retail investors at scale. Reiterate compliance with SEBI public-good ethos.

---

## ⚡ 6. How to Run Locally

### One-Command Start:
```bash
cd /home/deepank-singh/Documents/ltv-kavach
./run.sh
```

### Accessing the Prototype:
* **Interactive Dashboard**: [http://localhost:8000](http://localhost:8000)
* **Swagger API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Automated Test Suite**:
  ```bash
  python3 tests/test_risk_engine.py
  ```
