# 1. 목적 (Purpose)
macOS 웹캠으로 입력되는 사용자의 착석/부재 및 4종 주요 손제스처(Wave, ThumbsUp, OpenPalm, Victory)를 감지하여 자비스 행동 이벤트로 자동 정규화 처리합니다.

# 2. 입력 (Input)
- `웹캠 프레임 데이터` 및 `비전 랜드마크 이벤트`

# 3. 절차 (Procedure)
1. 실시간 영상 프레임에서 사용자 얼굴 존재 여부(Presence)를 1초 단위 감지합니다.
2. 손 윤곽선 및 움직임 베그라운드 랜드마크 분석을 통해 제스처 타입(`USER_ARRIVED`, `VICTORY`, `OPEN_PALM`, `THUMBS_UP`)을 파싱합니다.
3. 2.5초 지연(Cooldown)을 두어 동일 제스처의 연속 중복 실행을 방지합니다.
4. 매핑된 이벤트를 `tts_engine.py` 및 브리핑 스킬(`SKILLS/skill_voice_briefing.md`)로 전달합니다.

# 4. 출력 (Output)
- `비전 이벤트 파싱 결과` 및 `자동 트리거 실행 로그`

# 5. 실패 처리 (Fallback)
- 조명 부족 또는 카메라 차단 시: "웹캠 영상 수신이 불완전합니다. 조명을 확보해 주세요."라고 로그를 남깁니다.
