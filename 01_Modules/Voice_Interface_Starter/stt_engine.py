#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Voice Interface Starter - STT Engine
Converts microphone audio or audio files to Korean text.
"""

import sys
import argparse

def listen_microphone(language: str = "ko-KR", timeout: int = 5) -> str:
    """마이크를 통해 음성 수신 후 텍스트 변환"""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("[STT Engine] 🎙️ 음성 입력 대기 중... (말씀해주세요)")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=timeout)
            print("[STT Engine] 🔄 음성 처리 중...")
            text = r.recognize_google(audio, language=language)
            print(f"[STT Engine] 📝 인식된 텍스트: {text}")
            return text
    except ImportError:
        print("[STT Warning] speech_recognition or pyaudio package not installed.", file=sys.stderr)
        print("[STT Fallback] 텍스트 입력 모드로 전환합니다.")
        return input("입력할 명령어를 입력하세요 > ")
    except Exception as e:
        print(f"[STT Error] 음성 인식 실패 ({e})", file=sys.stderr)
        return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jarvis STT Engine Test")
    parser.add_argument("--timeout", type=int, default=5, help="듣기 대기 시간(초)")
    args = parser.parse_args()

    result = listen_microphone(timeout=args.timeout)
    print(f"\n[최종 인식 결과]: {result}")
