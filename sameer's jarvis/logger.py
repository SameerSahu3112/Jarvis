import os
from datetime import datetime

# Always create logs/ next to this file, no matter where you run Jarvis from
base_folder = os.path.dirname(os.path.abspath(__file__))
log_folder = os.path.join(base_folder, "logs")
os.makedirs(log_folder, exist_ok=True)
log_path = os.path.join(log_folder, "jarvis.log")

def log(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"{time} | {message}\n")