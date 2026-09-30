#!/usr/bin/env bash
# =====================================================================
# JARVIS SYSTEM :: One-Click Launch Script (All-in-One Integrated Engine)
# =====================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo " 🤖 Starting JARVIS All-in-One Integrated Desktop Assistant"
echo " 📷 Camera: Default ON (Voice Controllable)"
echo " 🎙️ Voice: Default ON (STT/TTS Active)"
echo "============================================================"
echo ""

# Launch integrated Jarvis Desktop App
python3 01_Modules/Jarvis_Desktop_App_Starter/jarvis_app.py
