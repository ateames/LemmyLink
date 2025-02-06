# Starts the bot and the bidirectional sync processes in separate threads
import subprocess
import sys
import time

# Start both processes
proc_main = subprocess.Popen([sys.executable, "LemmyLink/main.py"])
proc_sync = subprocess.Popen([sys.executable, "LemmyLink/bidirectional_sync.py"])

try:
    # Keep the main thread alive while both processes run.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminating both processes...")
    proc_main.terminate()
    proc_sync.terminate()
    proc_main.wait()
    proc_sync.wait()
