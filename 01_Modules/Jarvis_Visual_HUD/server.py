#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Sci-Fi Visual Interactive HUD - Local Web Server
Supports real-time live data streaming (/api/data) for instant UI auto-refresh without page reload.
"""

import http.server
import socketserver
import os
import sys
import json
import time
import webbrowser

PORT = 8088

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(DIRECTORY, "..", "..", "LOGS")

class JarvisHUDHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            # Read latest logs & status
            vision_status = "USER_ARRIVED"
            gesture = "V_POSE (1-MIN BRIEFING)"
            
            # Check vision log if exists
            v_log = os.path.join(LOG_DIR, "vision_runner_stdout.log")
            if os.path.exists(v_log):
                try:
                    with open(v_log, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        for line in reversed(lines[-20:]):
                            if "GESTURE_DETECTED" in line:
                                gesture = line.strip().split("GESTURE_DETECTED:")[-1].strip()
                                break
                except Exception:
                    pass

            response_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "presence": vision_status,
                "gesture": gesture,
                "fps": 30,
                "tasks": [
                    {"num": "01", "title": "AILO-H Core Pipeline Review", "status": "DONE"},
                    {"num": "02", "title": "Neural Human Voice Engine", "status": "DONE"},
                    {"num": "03", "title": "Real-time Live Sync Module", "status": "ACTIVE"}
                ]
            }
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return
            
        super().do_GET()

def start_server():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), JarvisHUDHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(" 🤖 JARVIS Sci-Fi Visual Interactive HUD Dashboard (Real-time Stream Engine)")
        print(f" 🚀 Running at: {url}")
        print("=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Jarvis HUD] Web server stopped.")
            httpd.server_close()

if __name__ == "__main__":
    start_server()
