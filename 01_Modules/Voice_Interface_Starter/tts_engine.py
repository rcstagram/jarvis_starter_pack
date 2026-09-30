#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Voice Interface Starter - TTS Engine
Supports macOS native `say` command & `edge-tts` fallback
"""

import sys
import os
import subprocess
import argparse
import asyncio

def speak_macos_say(text: str, voice: str = "Yuna") -> bool:
    """macOS 내장 say 명령어를 사용하여 음성 출력 (의존성 0)"""
    try:
        # macOS say command with Yuna voice or default
        cmd = ["say", "-v", voice, text]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        try:
            # Fallback without specifying voice
            cmd = ["say", text]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            print(f"[TTS Error] macOS say failed: {e}", file=sys.stderr)
            return False

async def speak_edge_tts_async(text: str, voice: str = "ko-KR-SunHiNeural", output_file: str = "/tmp/jarvis_tts.mp3") -> bool:
    """edge-tts를 사용하여 신경망 음성 파일 생성 후 재생"""
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        
        # macOS afplay or system mp3 player
        if sys.platform == "darwin":
            subprocess.run(["afplay", output_file], check=True)
        else:
            subprocess.run(["mpg123", output_file], check=True)
        return True
    except ImportError:
        print("[TTS Warning] edge-tts package not installed. Falling back to macOS say...", file=sys.stderr)
        return speak_macos_say(text)
    except Exception as e:
        print(f"[TTS Error] edge-tts failed: {e}. Falling back to macOS say...", file=sys.stderr)
        return speak_macos_say(text)

def speak(text: str, engine: str = "edge") -> bool:
    """
    통합 음성 출력 함수
    engine: 'edge' (고품질 사람 신경망 음성) | 'say' (macOS 기본)
    """
    clean_text = text.replace("*", "").replace("#", "").replace("`", "")
    if engine == "say":
        return speak_macos_say(clean_text)
    else:
        return asyncio.run(speak_edge_tts_async(clean_text))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jarvis TTS Engine Test")
    parser.add_argument("--text", type=str, default="안녕하세요, 자비스 음성 비서 엔진이 준비되었습니다.", help="재생할 텍스트")
    parser.add_argument("--engine", type=str, choices=["auto", "say", "edge"], default="auto", help="TTS 엔진 선택")
    args = parser.parse_args()

    print(f"[TTS Engine] Processing: '{args.text}' (Engine: {args.engine})")
    success = speak(args.text, engine=args.engine)
    if success:
        print("[TTS Engine] Playback completed successfully.")
    else:
        print("[TTS Engine] Playback failed.")
