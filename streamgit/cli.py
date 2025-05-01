import subprocess
import os
import sys

def main():
    # Get the absolute path to app.py regardless of where CLI is called from
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_dir, "..", "app.py")
    app_path = os.path.abspath(app_path)

    # Launch Streamlit app properly using subprocess
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Failed to launch Streamlit app.")
        print(e)
        sys.exit(1)
