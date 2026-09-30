# Voice Interface Starter (Jarvis 음성 모듈)

이 모듈은 자비스 개인 비서 시스템에 **음성 인식(STT)** 및 **음성 합성(TTS)** 기능을 제공하여, 음성 명령 수신과 음성 응답 브리핑을 실시간 처리합니다.

---

## 🛠️ 주요 기능
1. **TTS (Text-to-Speech)**:
   - macOS 내장 `say` 명령어 지원 (별도 의존성 없이 즉시 작동)
   - `edge-tts` (Microsoft Edge 신경망 한국어 음성: `ko-KR-SunHiNeural` / `ko-KR-InJoonNeural`) 지원
2. **STT (Speech-to-Text)**:
   - `faster-whisper` / `whisper.cpp` / Python `SpeechRecognition` 연동
3. **Voice Runner (`voice_runner.py`)**:
   - 마이크 입력 감지 ➡️ 자비스 파이프라인 연동 ➡️ 음성 브리핑 재생 루프 지원

---

## 🚀 빠른 시작 방법

### 1) 필수 라이브러리 설치 (선택 - edge-tts / whisper 구동 시)
```bash
pip install edge-tts speechrecognition faster-whisper pyaudio
```

### 2) TTS 테스트 실행 (macOS `say` / `edge-tts`)
```bash
python 01_Modules/Voice_Interface_Starter/tts_engine.py --text "안녕하세요, 자비스 음성 엔진 테스트입니다."
```

### 3) 음성 인터페이스 메인 실행기 구동
```bash
python 01_Modules/Voice_Interface_Starter/voice_runner.py
```
