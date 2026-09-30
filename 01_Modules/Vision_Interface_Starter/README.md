# Vision Interface Starter (Jarvis 비전 & 모션 모듈)

이 모듈은 웹캠(FaceTime HD Camera)을 통해 **사용자 얼굴 인식, 착석/부재 감지, 손제스처 및 움직임(Motion)**을 실시간 추적하여 자비스 시스템의 음성 및 브리핑 스킬과 연동합니다.

---

## 🛠️ 주요 기능
1. **사용자 착석/부재 감지 (User Presence Detection)**:
   - OpenCV Cascade Classifier 기반 사용자 얼굴 및 상반신 감지
   - 모니터 앞 다가옴 감지 시 자동 음성 인사 (*"안녕하세요. 자비스 대기 중입니다."*)
2. **모션 및 제스처 추적 (Motion & Gesture Recognition)**:
   - 👋 **손 흔들기 (Wave)**: 모션 백그라운드 프레임 차분법 및 손윤곽선 분석 ➡️ 대기 모드 해제 및 자비스 호출
   - 🖐️ **손바닥 펼치기 (Open Palm)**: 프레임 윤곽선 면적 및 모션 감지 ➡️ 음성 재생 일시정지 / 정지
   - ✌️ **V 포즈 / 손 흔듦 (Victory/Motion)**: 1분 브리핑 시작
3. **비전 루너 (`vision_runner.py`)**:
   - 실시간 비전 백그라운드 스레드 가동 ➡️ 제스처 이벤트 발생 시 TTS 안내 및 스킬 트리거

---

## 🚀 빠른 시작 방법

### 1) 라이브러리 설치
```bash
pip install opencv-python numpy
```

### 2) 비전 모듈 단독 실행 테스트
```bash
python 01_Modules/Vision_Interface_Starter/vision_engine.py
```

### 3) 비전-음성 통합 실행기 구동
```bash
python 01_Modules/Vision_Interface_Starter/vision_runner.py
```
