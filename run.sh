#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🛡️  STARTING LTV-KAVACH: INVESTOR RESILIENCE GUARDIAN"
echo "    SEBI / NSDL SANGYAN Hackathon Prototype"
echo "=========================================================="

# Ensure local packages are in PYTHONPATH
export PYTHONPATH="$DIR/packages:$DIR:$PYTHONPATH"

# Run tests first
echo "[1/2] Running automated risk validation suite..."
python3 tests/test_risk_engine.py

# Launch application
echo "[2/2] Launching LTV-Kavach Server on http://localhost:8000 ..."
python3 app.py
