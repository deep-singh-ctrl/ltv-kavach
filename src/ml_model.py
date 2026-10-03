"""
Lightweight, Explainable Machine Learning Classifier for Loan Vulnerability.
Predicts the 90-day Margin Call / Default Breach Probability and isolates key risk drivers.
"""

import os
import sys

# Ensure local packages are on path
pkg_path = "/home/deepank-singh/Documents/ltv-kavach/packages"
if pkg_path not in sys.path:
    sys.path.insert(0, pkg_path)

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib

MODEL_PATH = "/home/deepank-singh/Documents/ltv-kavach/models/loan_vulnerability_rf.joblib"
METADATA_PATH = "/home/deepank-singh/Documents/ltv-kavach/models/model_metadata.joblib"

FEATURE_NAMES = [
    "starting_ltv",
    "portfolio_beta",
    "hhi_concentration",
    "annual_volatility",
    "top1_holding_share",
    "buffer_liquidity_ratio"
]

class LoanVulnerabilityModel:
    def __init__(self):
        self.model = None
        self.metadata = {}
        self.load_or_train()

    def generate_synthetic_loan_dataset(self, n_samples: int = 5000, random_state: int = 42):
        """
        Synthesizes realistic Indian LAS loan portfolios based on historical market regimes.
        A loan breaches if realistic simulated 90-day drawdowns push LTV >= maintenance threshold.
        """
        rng = np.random.RandomState(random_state)
        
        # 1. Starting LTV (between 25% and 70%)
        starting_ltv = rng.uniform(0.25, 0.70, n_samples)
        
        # 2. Portfolio Beta (0.6 to 2.4)
        portfolio_beta = rng.uniform(0.60, 2.40, n_samples)
        
        # 3. Top 1 Holding Share (15% to 90%)
        top1_share = rng.uniform(0.15, 0.90, n_samples)
        
        # 4. HHI Concentration (1000 to 8500)
        hhi = (top1_share ** 2 * 10000) + rng.uniform(500, 2000, n_samples)
        hhi = np.clip(hhi, 1000, 10000)
        
        # 5. Annual Volatility (12% to 55%)
        annual_vol = 0.12 + (portfolio_beta * 0.14) + (top1_share * 0.10) + rng.normal(0, 0.03, n_samples)
        annual_vol = np.clip(annual_vol, 0.10, 0.65)
        
        # 6. Buffer Liquidity Ratio (Cash Buffer / Loan Amount, 0.0 to 0.40)
        buffer_ratio = rng.exponential(scale=0.08, size=n_samples)
        buffer_ratio = np.clip(buffer_ratio, 0.0, 0.50)

        # Ground Truth Simulation:
        # 90-day market drawdown probability (Nifty ~ Normal(-0.02, 0.08), with fat tails)
        nifty_drawdown = rng.normal(-0.02, 0.08, n_samples) - rng.exponential(scale=0.03, size=n_samples)
        portfolio_drawdown = nifty_drawdown * portfolio_beta * (1.0 + (top1_share * 0.3))
        # Clip max drop to -85%
        portfolio_drawdown = np.clip(portfolio_drawdown, -0.85, 0.30)
        
        # Effective LTV after 90 days = Starting_LTV / (1 + Drawdown)
        effective_ltv = starting_ltv / np.maximum(1.0 + portfolio_drawdown, 0.15)
        
        # Effective buffer relief: buffer reduces effective loan burden
        effective_ltv = effective_ltv * (1.0 - (buffer_ratio * 0.6))
        
        # Breach if LTV exceeds 0.65 (margin call threshold)
        y = (effective_ltv >= 0.65).astype(int)

        X = np.column_stack([
            starting_ltv,
            portfolio_beta,
            hhi,
            annual_vol,
            top1_share,
            buffer_ratio
        ])

        return X, y

    def train(self):
        """Trains and saves the Random Forest Classifier with feature importances."""
        X, y = self.generate_synthetic_loan_dataset(n_samples=6000)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = RandomForestClassifier(
            n_estimators=100,
            max_depth=7,
            min_samples_leaf=10,
            random_state=42,
            n_jobs=1  # serial mode to avoid sandbox permission errors
        )
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1]

        acc = float(accuracy_score(y_test, y_pred))
        auc = float(roc_auc_score(y_test, y_prob))

        feature_importances = {
            name: round(float(imp) * 100.0, 2)
            for name, imp in zip(FEATURE_NAMES, clf.feature_importances_)
        }

        self.model = clf
        self.metadata = {
            "accuracy": round(acc * 100.0, 2),
            "roc_auc": round(auc, 3),
            "n_samples": len(X),
            "feature_importances": feature_importances,
            "trained_at": "October 2026",
            "model_type": "Explainable Random Forest Classifier"
        }

        # Save artifacts
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.metadata, METADATA_PATH)
        print(f"[ML Model] Successfully trained! Test Accuracy: {self.metadata['accuracy']}% | ROC-AUC: {self.metadata['roc_auc']}")

    def load_or_train(self):
        """Loads cached model or triggers training if not present."""
        if os.path.exists(MODEL_PATH) and os.path.exists(METADATA_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
                self.metadata = joblib.load(METADATA_PATH)
                print("[ML Model] Loaded cached Random Forest model.")
                return
            except Exception as e:
                print(f"[ML Model] Failed loading cached model ({e}), retraining...")

        self.train()

    def predict_vulnerability(
        self,
        starting_ltv: float,
        portfolio_beta: float,
        hhi_concentration: float,
        annual_volatility: float,
        top1_holding_share: float,
        buffer_liquidity_ratio: float
    ):
        """
        Evaluates risk score (0-100), breach probability, and explainable drivers.
        """
        if self.model is None:
            self.load_or_train()

        features = np.array([[
            starting_ltv,
            portfolio_beta,
            hhi_concentration,
            annual_volatility,
            top1_holding_share,
            buffer_liquidity_ratio
        ]])

        breach_prob = float(self.model.predict_proba(features)[0, 1])
        vulnerability_score = int(round(breach_prob * 100.0))

        # Determine Risk Grade
        if vulnerability_score < 25:
            grade = "LOW"
            badge_color = "green"
            grade_description = "Resilient structure. Very low probability of margin distress."
        elif vulnerability_score < 55:
            grade = "MODERATE"
            badge_color = "yellow"
            grade_description = "Manageable risk. Normal market dips are absorbed, but stay alert."
        elif vulnerability_score < 80:
            grade = "HIGH"
            badge_color = "orange"
            grade_description = "Vulnerable loan. Tightly leveraged against market swings."
        else:
            grade = "CRITICAL"
            badge_color = "red"
            grade_description = "Extreme danger! Near-certain liquidation trigger during next correction."

        # Explainable Driver Breakdown (Plain-language contribution attribution)
        drivers = []
        if starting_ltv >= 0.55:
            drivers.append({
                "factor": "Aggressive Starting Leverage",
                "severity": "High",
                "detail": f"Current LTV of {round(starting_ltv*100, 1)}% leaves almost zero margin for market fluctuations."
            })
        elif starting_ltv >= 0.45:
            drivers.append({
                "factor": "Elevated Leverage",
                "severity": "Medium",
                "detail": f"Current LTV of {round(starting_ltv*100, 1)}% is above the conservative 40% threshold."
            })

        if portfolio_beta >= 1.5:
            drivers.append({
                "factor": "High-Beta Asset Volatility",
                "severity": "High",
                "detail": f"Portfolio Beta of {round(portfolio_beta, 2)} means your collateral swings {round((portfolio_beta-1)*100)}% harder than the Nifty."
            })
        elif portfolio_beta >= 1.2:
            drivers.append({
                "factor": "Moderate Beta",
                "severity": "Medium",
                "detail": f"Portfolio Beta of {round(portfolio_beta, 2)} introduces extra sensitivity to market dips."
            })

        if top1_holding_share >= 0.40 or hhi_concentration >= 3000:
            drivers.append({
                "factor": "Single Stock Concentration",
                "severity": "High",
                "detail": f"Top holding accounts for {round(top1_holding_share*100, 1)}% of total collateral. A drop in one stock threatens the entire loan."
            })

        if buffer_liquidity_ratio < 0.10:
            drivers.append({
                "factor": "Thin Emergency Buffer",
                "severity": "High",
                "detail": "Borrower has less than 10% emergency cash buffer to answer sudden margin calls."
            })

        if not drivers:
            drivers.append({
                "factor": "Balanced Collateral Base",
                "severity": "Low",
                "detail": "Diversified holdings and healthy leverage provide sufficient shock absorption."
            })

        return {
            "vulnerability_score": vulnerability_score,
            "breach_probability_pct": round(breach_prob * 100.0, 1),
            "risk_grade": grade,
            "badge_color": badge_color,
            "grade_description": grade_description,
            "drivers": drivers,
            "model_metadata": self.metadata
        }

# Global singleton
ml_engine = LoanVulnerabilityModel()
