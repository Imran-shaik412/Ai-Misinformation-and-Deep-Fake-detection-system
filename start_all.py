import subprocess
import time
import sys
import os

def start_backend():
    print("🚀 Starting FastAPI Backend (http://localhost:8000)...")
    return subprocess.Popen([sys.executable, "main.py"], cwd="backend")

def start_frontend():
    print("🎨 Starting Frontend Server (http://localhost:3000)...")
    # Using python's built-in http server for simplicity
    return subprocess.Popen([sys.executable, "-m", "http.server", "3000"], cwd="frontend")

if __name__ == "__main__":
    be_proc = None
    fe_proc = None
    try:
        be_proc = start_backend()
        # Give backend a moment to start
        time.sleep(2)
        fe_proc = start_frontend()
        
        print("\n✅ CyberDefense AI System is LIVE!")
        print("-" * 40)
        print("Backend:  http://localhost:8000")
        print("Frontend: http://localhost:3000")
        print("-" * 40)
        print("\nPress Ctrl+C to stop both servers.")
        
        while True:
            # Check if processes are still running
            if be_proc.poll() is not None:
                print("❌ Backend stopped unexpectedly.")
                break
            if fe_proc.poll() is not None:
                print("❌ Frontend stopped unexpectedly.")
                break
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down CyberDefense AI...")
    finally:
        if be_proc: be_proc.terminate()
        if fe_proc: fe_proc.terminate()
        print("Done.")
        sys.exit(0)
