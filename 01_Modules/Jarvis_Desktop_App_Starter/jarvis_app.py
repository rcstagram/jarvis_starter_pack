#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis Standalone Desktop Application (Integrated All-in-One Engine)
Launches the native desktop HUD window with integrated Voice (STT/TTS)
and Vision (OpenCV Motion & Gestures) background engines.
Default: Camera ON & Mic ON.
Supports Voice Commands: '카메라 꺼줘', '카메라 켜줘', '브리핑', '종료' etc.
"""

import os
import sys
import threading
import time
import json
import webview

# Module Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
VOICE_DIR = os.path.join(MODULES_DIR, "Voice_Interface_Starter")
VISION_DIR = os.path.join(MODULES_DIR, "Vision_Interface_Starter")
HUD_DIR = os.path.join(MODULES_DIR, "Jarvis_Visual_HUD")
HUD_HTML = os.path.abspath(os.path.join(HUD_DIR, "index.html"))

if VOICE_DIR not in sys.path:
    sys.path.append(VOICE_DIR)
if VISION_DIR not in sys.path:
    sys.path.append(VISION_DIR)

from tts_engine import speak
from stt_engine import listen_microphone
from vision_engine import JarvisVisionEngine

class JarvisAppManager:
    """통합 자비스 앱 중앙 제어 및 워커 스레드 관리자"""
    def __init__(self):
        self.window = None
        self.is_running = True
        self.camera_active = True   # Default: Camera ON
        self.mic_active = True      # Default: Mic ON
        self.is_speaking = False    # Prevent audio feedback loop
        
        self.vision_engine = JarvisVisionEngine(camera_index=0)
        self.voice_thread = None
        self.vision_thread = None

    def set_window(self, window):
        self.window = window

    def safe_eval_js(self, js_code):
        """Webview JavaScript 안전 실행 (비동기 스레드 대응)"""
        if self.window:
            try:
                self.window.evaluate_js(js_code)
            except Exception as e:
                pass

    def log_to_hud(self, speaker: str, text: str):
        """HUD 자막 및 실시간 로그 창에 메시지 기록"""
        spk = json.dumps(speaker)
        msg = json.dumps(text)
        self.safe_eval_js(f"if (window.addLiveLog) window.addLiveLog({spk}, {msg});")

    def speak_and_log(self, text: str):
        """TTS 음성 출력과 동시에 HUD에 자막 표출 (에코 방지 락 적용)"""
        self.is_speaking = True
        self.log_to_hud("JARVIS", text)
        self.safe_eval_js("if (window.setVoiceState) window.setVoiceState('speaking');")
        try:
            speak(text)
        finally:
            time.sleep(0.3)  # 버퍼 타임
            self.is_speaking = False
            self.safe_eval_js("if (window.setVoiceState) window.setVoiceState('ready');")

    def set_camera_state(self, active: bool):
        """음성 명령 등에 의해 Python에서 카메라 상태를 변경할 때 (Python -> JS 동기화)"""
        self.camera_active = active
        js_bool = "true" if active else "false"
        self.safe_eval_js(f"if (window.setCameraState) window.setCameraState({js_bool});")
        
        if active:
            print("[Jarvis Manager] 📷 카메라 활성화 (Vision ON)")
        else:
            print("[Jarvis Manager] 🔒 카메라 비활성화 (Vision OFF / Privacy Mode)")
            self.vision_engine.stop_camera()

    def set_mic_state(self, active: bool):
        """마이크 음성 비서 ON/OFF 제어"""
        self.mic_active = active
        status_text = "음성 비서 마이크가 활성화되었습니다." if active else "음성 비서 마이크가 일시정지되었습니다."
        self.log_to_hud("SYS", status_text)

    def handle_briefing(self):
        """업무 브리핑 실행"""
        msg = "오늘의 1분 업무 브리핑입니다. 현재 시스템의 모든 신경망 코어가 정상 작동 중이며, 서울 날씨는 맑고 쾌적합니다."
        self.speak_and_log(msg)

    # =========================================================================
    # 음성 비서 백그라운드 워커 루프 (Voice Worker Loop)
    # =========================================================================
    def voice_loop(self):
        print("[Voice Worker] 🎙️ 백그라운드 음성 비서 루프 가동 시작")
        time.sleep(1.5)  # HUD 창 로딩 대기
        
        initial_msg = "자비스 통합 시스템이 가동되었습니다. 카메라와 음성 인식이 모두 준비되었습니다."
        self.speak_and_log(initial_msg)

        while self.is_running:
            if not self.mic_active or self.is_speaking:
                time.sleep(0.3)
                continue

            self.safe_eval_js("if (window.setVoiceState) window.setVoiceState('listening');")
            user_input = listen_microphone(language="ko-KR", timeout=4)
            
            if not user_input or user_input.strip() == "":
                continue

            if not self.is_running:
                break

            print(f"\n[Voice Command Detected]: '{user_input}'")
            self.log_to_hud("USER", user_input)

            clean_cmd = user_input.strip().lower()

            # 1. 카메라 끄기 명령어 ("카메라 꺼줘", "카메라 꺼", "비전 꺼" 등)
            if any(k in clean_cmd for k in ["카메라", "비전", "웹캠", "캠", "화면"]) and \
               any(k in clean_cmd for k in ["꺼", "닫", "중지", "종료", "정지", "off", "stop"]):
                self.set_camera_state(False)
                self.speak_and_log("네, 카메라를 끕니다. 사생활 보호 모드로 전환합니다.")

            # 2. 카메라 켜기 명령어 ("카메라 켜줘", "카메라 켜", "비전 켜" 등)
            elif any(k in clean_cmd for k in ["카메라", "비전", "웹캠", "캠", "화면"]) and \
                 any(k in clean_cmd for k in ["켜", "열", "시작", "가동", "on", "start"]):
                self.set_camera_state(True)
                self.speak_and_log("네, 카메라를 켭니다. 비전 인식 및 모션 감지를 시작합니다.")

            # 3. 마이크 일시정지 명령어
            elif any(k in clean_cmd for k in ["마이크", "음성"]) and \
                 any(k in clean_cmd for k in ["꺼", "중지", "종료", "off", "stop"]):
                self.speak_and_log("음성 인식을 일시 정지합니다. 화면의 마이크 버튼으로 언제든 다시 켜실 수 있습니다.")
                self.set_mic_state(False)

            # 4. 브리핑 요청
            elif any(k in clean_cmd for k in ["브리핑", "날씨", "일정", "뉴스"]):
                self.handle_briefing()

            # 5. 시스템 종료 요청
            elif any(k in clean_cmd for k in ["자비스 종료", "시스템 종료", "앱 종료", "프로그램 끝내", "전체 종료"]) or \
                 clean_cmd in ["종료", "끝내", "exit", "quit"]:
                self.speak_and_log("자비스 시스템을 종료합니다. 좋은 하루 되십시오.")
                self.is_running = False
                if self.window:
                    self.window.destroy()
                break

            # 6. 인사 및 호칭
            elif any(k in clean_cmd for k in ["안녕", "자비스", "하이", "hello", "hi", "반가워"]):
                self.speak_and_log("안녕하세요! 자비스입니다. 말씀하시면 지시사항을 수행하겠습니다.")

            # 7. 일반 명령 피드백
            else:
                resp = f"네, 확인하였습니다. 말씀하신 '{user_input}' 내용을 처리 중입니다."
                self.speak_and_log(resp)

    # =========================================================================
    # 비전 모션 감지 백그라운드 워커 루프 (Vision Worker Loop)
    # =========================================================================
    def vision_loop(self):
        print("[Vision Worker] 📷 백그라운드 비전 & 모션 감지 루프 가동 시작")
        
        def on_vision_event(event_type, details):
            if not self.camera_active or not self.is_running:
                return

            if event_type == "USER_ARRIVED":
                self.log_to_hud("SYS", "사용자 인식됨 (User Arrived)")
                if not self.is_speaking:
                    self.speak_and_log("사용자가 인식되었습니다. 반갑습니다.")

            elif event_type == "GESTURE_DETECTED":
                gesture = details.get("gesture")
                print(f"[Vision Worker] Gesture Event: {gesture}")
                g_json = json.dumps(gesture)
                self.safe_eval_js(f"if (window.updateGesture) window.updateGesture({g_json});")
                
                if gesture == "VICTORY":
                    self.log_to_hud("SYS", "제스처 감지: V 포즈 (1분 브리핑)")
                    self.handle_briefing()
                elif gesture == "OPEN_PALM":
                    self.log_to_hud("SYS", "제스처 감지: 손바닥 (음성 정지)")
                    self.safe_eval_js("if ('speechSynthesis' in window) window.speechSynthesis.cancel();")
                elif gesture == "THUMBS_UP":
                    self.log_to_hud("SYS", "제스처 감지: 엄지 척 (명령 승인)")
                    self.speak_and_log("엄지 척 제스처가 감지되었습니다. 명령을 승인합니다.")

        while self.is_running:
            if self.camera_active:
                try:
                    self.vision_engine.run_detection_loop(callback=on_vision_event, show_window=False)
                except Exception as e:
                    print(f"[Vision Worker Warning] {e}")
                    time.sleep(1.0)
            else:
                time.sleep(0.5)

    def start_workers(self):
        """음성 및 비전 백그라운드 워커 스레드 가동"""
        self.voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
        self.voice_thread.start()

        self.vision_thread = threading.Thread(target=self.vision_loop, daemon=True)
        self.vision_thread.start()

    def shutdown(self):
        """시스템 정상 종료 및 하드웨어 릴리즈"""
        print("[Jarvis System] 🛑 Shutting down workers and releasing hardware...")
        self.is_running = False
        self.camera_active = False
        try:
            self.vision_engine.stop_detection()
        except Exception:
            pass

class JarvisAPI:
    """Python Native API exposed to Javascript inside Desktop Window"""
    def __init__(self, manager: JarvisAppManager):
        self.manager = manager

    def get_status(self):
        return {
            "status": "ONLINE",
            "camera": self.manager.camera_active,
            "mic": self.manager.mic_active,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def on_camera_toggled(self, active: bool):
        """UI 버튼 클릭에 의해 카메라 상태가 변경되었을 때 (JS -> Python 동기화)"""
        print(f"[Jarvis UI] Camera toggled via UI button: {active}")
        self.manager.camera_active = active
        if active:
            print("[Jarvis Manager] 📷 카메라 비전 엔진 활성화 (Vision ON)")
        else:
            print("[Jarvis Manager] 🔒 카메라 비전 엔진 비활성화 (Vision OFF / Privacy Mode)")
            self.manager.vision_engine.stop_camera()
        return True

    def on_mic_toggled(self, active: bool):
        self.manager.set_mic_state(active)
        return True

    def trigger_briefing(self):
        threading.Thread(target=self.manager.handle_briefing, daemon=True).start()
        return True

def launch_desktop_app():
    print("=" * 60)
    print(" 🚀 Launching JARVIS All-in-One Executive Desktop System...")
    print(" 📷 Default Camera: ACTIVE (ON)")
    print(" 🎙️ Default Microphone: ACTIVE (ON)")
    print("=" * 60)

    manager = JarvisAppManager()
    api = JarvisAPI(manager)

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

    manager.set_window(window)
    window.events.closed += manager.shutdown

    # Start background integrated engines
    manager.start_workers()

    # Start native UI event loop
    webview.start(debug=False)

if __name__ == "__main__":
    launch_desktop_app()
