import subprocess
import threading
import time
from launch_check import run_launch_check
from scheduler import start_scheduler

def launch_dashboard():
    """Launch Streamlit dashboard in a separate thread."""
    subprocess.Popen(["python", "-m", "streamlit", "run", "dashboard.py"])

def launch_scheduler():
    """Start the signal bot scheduler."""
    start_scheduler()

def main():
    print("🚀 Starting Zerodha AI Bot...\n")

    # Step 1: Run diagnostics + auto-correct
    run_launch_check()

    # Step 2: Launch dashboard
    print("📊 Launching dashboard...")
    threading.Thread(target=launch_dashboard).start()

    # Step 3: Start scheduler
    print("📅 Starting scheduler...")
    launch_scheduler()

if __name__ == "__main__":
    main()
