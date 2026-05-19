import sys
import os
import subprocess
from pathlib import Path
import json

def main():
    print("NEXUS AI TRADER v3.0 - Setup Script")
    print("====================================")
    
    # 1. Check Python 3.11 is installed
    if sys.version_info < (3, 11) or sys.version_info >= (3, 12):
        print("ERROR: Python 3.11.x is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print("✅ Python 3.11.x detected.")
    
    # 2. Virtual environment setup (managed by START_BOT.bat, assuming we are inside it)
    print("✅ Running in environment:", sys.prefix)
    
    # 4. Install all packages from requirements.txt
    print("Installing requirements from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements.")
        sys.exit(1)
        
    # 5. Install neo-api-client from GitHub
    print("Installing neo-api-client from GitHub...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "git+https://github.com/Kotak-Neo/kotak-neo-api.git"
        ])
        print("✅ neo-api-client installed.")
    except subprocess.CalledProcessError:
        print("❌ Failed to install neo-api-client.")
        sys.exit(1)
        
    # 6. Create all required folders
    print("Creating required folders...")
    folders = ["data", "logs", "reviews", "data/charts", "engine", "utils"]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created folder: {folder}")
        
    # 7. Create empty JSON files with correct structure
    print("Creating initial JSON data files...")
    json_files = {
        "data/trade_memory.json": [],
        "data/lifetime_stats.json": {},
        "data/learned_rules.json": [],
        "data/market_memory.json": {},
        "data/daily_allocation.json": {},
        "data/optimal_params.json": {}
    }
    
    for filepath, default_content in json_files.items():
        if not Path(filepath).exists():
            with open(filepath, 'w') as f:
                json.dump(default_content, f, indent=4)
            print(f"✅ Created file: {filepath}")
            
    # 8. Print completion message
    print("\nSetup complete! Edit config.py then run START_BOT.bat")

if __name__ == "__main__":
    main()
