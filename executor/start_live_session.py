import os
import subprocess
from datetime import datetime
from pathlib import Path

# === Settings ===
VENV_ACTIVATE_PATH = Path(__file__).resolve().parent.parent / '.venv' / 'bin' / 'activate'
LOGS_DIR = Path(__file__).resolve().parent.parent / 'logs'

today = datetime.today().strftime("%Y-%m-%d")
log_file = LOGS_DIR / f"session_live_{today}.log"
LOGS_DIR.mkdir(exist_ok=True)

# === Command ===
# (1) Source venv
# (2) Call: python -m executor.run_live_ibkr
command = f"source {VENV_ACTIVATE_PATH} && python -m executor.run_live_ibkr"

print(f"🚀 Starting live trading session...")
print(f"🔵 Logging output to {log_file}")

# === Open subprocess and pipe logs ===
with open(log_file, "w") as f:
    process = subprocess.Popen(
        ["bash", "-c", command],
        stdout=f,
        stderr=subprocess.STDOUT
    )
    process.communicate()

print("✅ Live session finished. Check log file for details.")
