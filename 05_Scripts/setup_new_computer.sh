#!/usr/bin/env bash
# =====================================================================
# JARVIS SYSTEM :: New Computer Auto-Installer & Boot Script (macOS/Linux)
# =====================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "============================================================"
echo " 🤖 JARVIS SYSTEM :: New Computer Auto-Setup & Booting"
echo "============================================================"
echo "Project Path: $PROJECT_ROOT"
echo ""

# 1. Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3가 설치되어 있지 않습니다. Python 3.10 이상을 설치해 주세요."
    exit 1
fi
echo "[1/4] ✅ Python3 감지 완료: $(python3 --version)"

# 2. Check macOS Homebrew & PortAudio
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "[2/4] 🍏 macOS 환경 감지. 마이크 음성 라이브러리(portaudio) 점검..."
    if command -v brew &> /dev/null; then
        brew list portaudio &> /dev/null || brew install portaudio
        brew list flac &> /dev/null || brew install flac
        echo "       ✅ portaudio 및 flac 오디오 라이브러리 준비 완료."
    else
        echo "       [WARN] Homebrew가 설치되어 있지 않습니다. pyaudio 및 flac 수동 설치가 필요할 수 있습니다."
    fi
else
    echo "[2/4] 🐧 Linux/Unix 환경 감지."
fi

# 3. Install Python Dependencies
echo "[3/4] 📦 파이썬 필수 의존성 패키지 일괄 설치 중..."
python3 -m pip install --break-system-packages -r requirements.txt || pip3 install -r requirements.txt

# 4. Ensure Directory Structure
echo "[4/4] 🗂️ 자비스 시스템 폴더 정렬 확인..."
mkdir -p LOGS CAPSULES TASKS TASKS/PROJECTS

echo ""
echo "============================================================"
echo " 🎉 모든 설정 및 설치가 완벽하게 완료되었습니다!"
echo "============================================================"
echo "구동할 자비스 모드를 선택하세요:"
echo " 1) 🚀 올인원 통합 데스크톱 앱 실행 (GUI + 음성 + 카메라 자동 가동) [추천]"
echo " 2) 🌐 SF 비주얼 대시보드 웹 서버 실행 (http://localhost:8088)"
echo " 3) 🎙️ 실시간 음성 비서 단독 실행 (Voice Runner)"
echo " 4) 📷 비전 & 모션 감지기 단독 실행 (Vision Runner)"
echo " 0) 종료"
echo "------------------------------------------------------------"

read -p "선택 (1/2/3/4/0) [기본값: 1]: " choice
choice=${choice:-1}

case "$choice" in
    1)
        echo "🚀 자비스 데스크톱 앱을 실행합니다..."
        python3 01_Modules/Jarvis_Desktop_App_Starter/jarvis_app.py
        ;;
    2)
        echo "🌐 비주얼 대시보드 웹 서버를 실행합니다..."
        python3 01_Modules/Jarvis_Visual_HUD/server.py
        ;;
    3)
        echo "🎙️ 음성 비서를 실행합니다..."
        python3 01_Modules/Voice_Interface_Starter/voice_runner.py
        ;;
    4)
        echo "📷 비전 모션 감지기를 실행합니다..."
        python3 01_Modules/Vision_Interface_Starter/vision_runner.py
        ;;
    0)
        echo "자비스 설정을 종료합니다."
        ;;
    *)
        echo "기본값(1): 자비스 데스크톱 앱을 실행합니다..."
        python3 01_Modules/Jarvis_Desktop_App_Starter/jarvis_app.py
        ;;
esac
