import subprocess
import time
import sys
import os
import signal

# Start FastAPI (Uvicorn) in the background
uvicorn_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "src.api.fastapi_app:app", "--reload"]
)

# Wait 10 seconds to ensure FastAPI is up
print("Waiting 10 seconds for FastAPI backend to start...")
time.sleep(10)

try:
    # Start Streamlit (this will block until Streamlit exits)
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "src/app/streamlit_app.py"]
    )
finally:
    print("Shutting down FastAPI backend...")
    if os.name == "nt":
        uvicorn_proc.send_signal(signal.CTRL_BREAK_EVENT)
    else:
        uvicorn_proc.terminate()
    uvicorn_proc.wait() 