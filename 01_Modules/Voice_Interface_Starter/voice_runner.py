#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Voice Interface Starter - Voice Runner
Main Interactive Loop for Voice Command & Response
"""

import sys
import os

# Add module path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tts_engine import speak
from stt_engine import listen_microphone

def run_voice_loop():
    print("=" * 60)
    print(" 🤖 Jarvis Voice Personal Assistant Interface")
    print("=" * 60)
    
    welcome_text = "안녕하세요. 자비스 개인 비서 음성 인터페이스가 가동되었습니다. 말씀하십시오."
    print(f"\n[Jarvis Voice]: {welcome_text}")
    speak(welcome_text)

    while True:
        try:
            user_input = listen_microphone()
            if not user_input or user_input.strip() == "":
                continue

            if any(cmd in user_input.lower() for cmd in ["종료", "끝내", "exit", "quit", "안녕"]):
                farewell = "음성 인터페이스를 종료합니다. 오늘도 좋은 하루 되십시오."
                print(f"[Jarvis Voice]: {farewell}")
                speak(farewell)
                break

            # Process voice command
            response_text = f"네, 수신하였습니다. '{user_input}' 지시사항을 처리 중입니다."
            print(f"[Jarvis Voice]: {response_text}")
            speak(response_text)

        except KeyboardInterrupt:
            print("\n[Jarvis Voice] 사용자에 의해 종료되었습니다.")
            break

if __name__ == "__main__":
    run_voice_loop()
