#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Standalone Desktop Application (Python + Native Window)
Launches a standalone desktop application window for Jarvis HOLO-OS.
"""

import webview
import os
import sys
import threading
import time

# Module Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HUD_DIR = os.path.join(BASE_DIR, "..", "Jarvis_Visual_HUD")
HUD_HTML = os.path.abspath(os.path.join(HUD_DIR, "index.html"))

class JarvisAPI:
    """Python Native API exposed to Javascript inside Desktop Window"""
    def __init__(self):
        pass

    def get_status(self):
        return {
            "status": "ONLINE",
            "mode": "Desktop App Native Window",
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def speak_text(self, text):
        print(f"[Jarvis Desktop App] Speaking: {text}")
        # Run TTS async in Python if needed
        return True

def launch_desktop_app():
    print("=" * 60)
    print(" 🚀 Launching Jarvis Native Desktop Application Window...")
    print("=" * 60)

    api = JarvisAPI()

    # Create PyWebView Standalone Desktop Window
    window = webview.create_window(
        title="JARVIS HOLO-OS :: Executive Assistant",
        url=HUD_HTML,
        width=1380,
        height=880,
        resizable=True,
        fullscreen=False,
        js_api=api,
        min_size=(900, 600)
    )

    webview.start(debug=False)

if __name__ == "__main__":
    launch_desktop_app()
