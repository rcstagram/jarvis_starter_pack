# 1. 목적 (Purpose)
SF 영화 스타일의 자비스 3D 파티클 AI 코어, 실시간 카메라 비전 뷰어, 주파수 비주얼라이저가 결합된 Fullscreen Visual Interactive HUD 대시보드를 구동 및 제어합니다.

# 2. 입력 (Input)
- `HUD 제어 명령`: `START_SERVER`, `SWITCH_STATE (ready | listening | speaking)`, `UPDATE_BRIEFING_CARD`

# 3. 절차 (Procedure)
1. `01_Modules/Jarvis_Visual_HUD/server.py`를 실행하여 로컬 포트 `8080`에 웹 서버를 바인딩합니다.
2. 사용자의 마이크 및 카메라 웹캠 장치를 동적으로 연결합니다.
3. 음성 발화 및 비전 제스처 수신 시 3D 파티클 구체의 색상 및 맥동 상태를 동적으로 전환합니다.
4. 실시간 음성 자막 및 브리핑 카드를 우측 HUD 패널에 동기화합니다.

# 4. 출력 (Output)
- `http://localhost:8080` 대시보드 URL 및 인터랙티브 UI 상태 파이프라인

# 5. 실패 처리 (Fallback)
- 포트 점유 중 시 다른 사용 가능한 포트(예: 8081)로 자동 폴백 및 로그를 출력합니다.
