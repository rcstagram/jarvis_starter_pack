# 1. 목적 (Purpose)
macOS 독채 윈도우 창(Native App Window) 형태의 Python 데스크톱 애플리케이션(`01_Modules/Jarvis_Desktop_App_Starter/jarvis_app.py`)을 구동하고 윈도우 프레임 및 Python 백엔드 API를 제어합니다.

# 2. 입력 (Input)
- `앱 제어 명령`: `LAUNCH_APP`, `TOGGLE_CAMERA`, `SPEAK_TEXT`, `MINIMIZE_WINDOW`

# 3. 절차 (Procedure)
1. `python3 01_Modules/Jarvis_Desktop_App_Starter/jarvis_app.py`를 실행하여 1380x880 크기의 독립 윈도우 프레임을 오픈합니다.
2. `pywebview` Cocoa WebKit 엔진을 통해 3D 파티클 코어, 실시간 자막 배너, 비전 피드를 렌더링합니다.
3. 앱 내부 버튼 클릭 및 음성 지시 발생 시 Python `JarvisAPI` 클래스를 통해 백엔드 처리 결과를 프레임으로 전달합니다.

# 4. 출력 (Output)
- 독립 실행 윈도우 창(Jarvis Desktop App) 및 로컬 이벤트 바인딩

# 5. 실패 처리 (Fallback)
- GUI 윈도우 라이브러리 부재 시: `pip install pywebview` 설치 유도 및 터미널 모드 안내.
