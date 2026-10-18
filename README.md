# Faceoff (faceoff.nhlanalytica.com)

NHL 일일 픽뎀 게임 + 공유 카드 생성기. Flask + SQLite.

## 로컬 실행
    pip install -r requirements.txt
    flask --app app run

## 구조
- app.py: API, 채점, 리더보드 (`/api/slate`, `/api/me`, `/api/pick`, `/api/leaderboard`)
- nhl.py: NHL 공개 API(api-web.nhle.com) 클라이언트
- model.py: 승률 모델. `win_prob()`만 IR 기반으로 바꾸면 나머지는 그대로 동작
- static/index.html: 프론트엔드 (게임, 리더보드, 선수 카드)

## 데이터 흐름
- 누군가 페이지를 열면 해당 날짜 일정을 최대 60초에 한 번 NHL API에서 갱신
- 경기가 처음 등록될 때 모델 확률을 계산해 고정 (나중에 안 바뀜)
- 경기가 FINAL/OFF가 되면 픽 자동 채점
- 방문자가 없어도 채점되도록 cron 추가 권장:
      */5 * * * * cd /path/to/faceoff && flask --app app sync

## 배포
SQLite 파일이 유지돼야 하므로 Vercel(서버리스)은 안 맞음.
Render/Railway/Fly.io(영구 디스크) 또는 nhlanalytica.com과 같은 서버 권장.
    gunicorn -w 2 -b 0.0.0.0:8000 app:app
환경변수: FACEOFF_DB (DB 경로), FACEOFF_SEASON_START (기본 2026-10-01)
DNS에 faceoff 서브도메인 CNAME 추가.
