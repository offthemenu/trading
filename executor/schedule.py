# schedule.py
import schedule
import time
from simulator.run_simulation import run_simulated_bot  # Or executor.run_live

schedule.every().day.at("22:25").do(run_simulated_bot)

while True:
    schedule.run_pending()
    time.sleep(1)
