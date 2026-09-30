#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Vision Interface Starter - Vision Runner
Integrates Vision Detection events with TTS voice responses and skills.
"""

import sys
import os

# Add module path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Voice_Interface_Starter"))

from vision_engine import JarvisVisionEngine
try:
    from tts_engine import speak
except ImportError:
    def speak(text):
        print(f"[Speech Mock]: {text}")

def on_vision_event(event_type, details):
    """비전 이벤트 발생 시 실행할 핸들러"""
    if event_type == "USER_ARRIVED":
        msg = "안녕하세요. 자비스 개인 비서가 인식되었습니다. 대기 중입니다."
        print(f"\n🤖 [Jarvis Vision]: {msg}")
        speak(msg)
        
    elif event_type == "USER_DEPARTED":
        msg = "사용자 부재가 감지되었습니다."
        print(f"\n🤖 [Jarvis Vision]: {msg}")
        
    elif event_type == "GESTURE_DETECTED":
        gesture = details.get("gesture")
        if gesture == "VICTORY":
            msg = "V 포즈가 감지되었습니다. 오늘의 1분 업무 브리핑을 시작합니다."
            print(f"\n🤖 [Jarvis Vision]: {msg}")
            speak(msg)
        elif gesture == "OPEN_PALM":
            msg = "손바닥 제스처가 감지되었습니다. 진행 중인 음성을 정지합니다."
            print(f"\n🤖 [Jarvis Vision]: {msg}")
            speak(msg)
        elif gesture == "THUMBS_UP":
            msg = "엄지 척 제스처가 감지되었습니다. 명령을 승인합니다."
            print(f"\n🤖 [Jarvis Vision]: {msg}")
            speak(msg)

def main():
    print("=" * 60)
    print(" 📷 Jarvis Vision & Motion Interface Engine Running")
    print("=" * 60)
    
    engine = JarvisVisionEngine()
    engine.run_detection_loop(callback=on_vision_event, show_window=False)

if __name__ == "__main__":
    main()
