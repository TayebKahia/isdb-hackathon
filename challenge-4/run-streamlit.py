#!/usr/bin/env python
import os
import sys
import subprocess
import webbrowser
from time import sleep


def main():
    """Run the Streamlit application for the AAOIFI QA Bot"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Set the app.py path
    app_path = os.path.join(script_dir, "app.py")

    # Check if the app.py file exists
    if not os.path.exists(app_path):
        print(f"Error: Could not find {app_path}")
        sys.exit(1)

    print("Starting AAOIFI QA Bot Streamlit application...")
    print("The application will open in your default web browser.")

    # Run Streamlit in a separate process
    try:
        # Start the Streamlit process
        cmd = ["streamlit", "run", app_path]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Wait for the server to start
        print("Waiting for the Streamlit server to start...")
        server_url = None
        for line in process.stdout:
            print(line.strip())
            if "You can now view your Streamlit app in your browser" in line:
                # Look for the URL line
                for _ in range(5):  # Check a few more lines
                    line = next(process.stdout, "").strip()
                    print(line)
                    if line.startswith("http://"):
                        server_url = line
                        break
                break

        if server_url:
            print(f"Opening {server_url} in your browser...")
            webbrowser.open(server_url)
        else:
            print("Streamlit server started, but couldn't detect the URL.")
            print("Please open the URL displayed in your terminal.")

        # Keep the script running until the user interrupts
        print("\nPress Ctrl+C to stop the server and exit...")
        process.wait()

    except KeyboardInterrupt:
        print("\nStopping the Streamlit server...")
        process.terminate()
        process.wait()
        print("Server stopped.")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
