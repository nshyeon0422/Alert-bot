# Alert Bot

웹사이트에 키워드가 포함된 새 글이 올라오면 텔레그램으로 알림을 보내는 봇입니다. 라즈베리파이 Zero 2에서 동작하도록 가볍게 구성했습니다.

## 설정
1) Python 3.10+ 환경을 준비합니다.
2) 의존성 설치 후 `.env`를 설정합니다.

필수 환경 변수:
- `TARGET_URL`: 모니터링할 웹사이트 주소
- `KEYWORDS`: 쉼표로 구분한 키워드 목록
- `USE_KEYWORDS`: 키워드 필터 사용 여부(true/false)
- `SEED_EXISTING`: 첫 실행 시 기존 글을 저장만 하고 알림을 보내지 않음(true/false)
- `MAX_ITEMS`: DB에 유지할 최대 글 개수
- `TELEGRAM_BOT_TOKEN`: 텔레그램 봇 토큰
- `TELEGRAM_CHAT_ID`: 알림을 받을 채팅 ID

선택 환경 변수:
- `ITEM_SELECTOR`, `TITLE_SELECTOR`, `LINK_SELECTOR`, `CONTENT_SELECTOR`: CSS 선택자로 글 목록 추출
- `POLL_INTERVAL_SECONDS`: 폴링 간격(초)
- `VERIFY_SSL`, `CA_BUNDLE_PATH`: 인증서 문제 대응
- `HTTP_PROXY`, `HTTPS_PROXY`: 프록시 설정
- `RETRY_ON_403`, `USER_AGENT`, `ACCEPT_LANGUAGE`, `REFERER`, `COOKIE`: 403 대응 헤더

## 실행
- `.env.example`을 복사해 `.env`를 만든 뒤 값을 채웁니다.
- 아래 명령으로 실행합니다.

```
python -m alertbot.main
```

## 동작 방식
- 대상 페이지를 주기적으로 가져와 글 목록을 파싱합니다.
- `USE_KEYWORDS=true`일 때만 키워드가 포함된 글을 전송합니다.
- 이미 알림을 보낸 글은 SQLite에 저장되어 중복 전송되지 않습니다.
- 시작 시 연결 확인 메시지를 전송합니다.
- `SEED_EXISTING=true`이면 첫 실행 시 기존 글은 저장만 하고 알림을 보내지 않습니다.
- DB는 `MAX_ITEMS` 개수만 유지되도록 주기적으로 정리합니다.

## SSL/403 참고
- `VERIFY_SSL=false`로 설정하면 인증서 검증을 비활성화합니다(보안상 위험하므로 테스트 목적 권장).
- 403이 발생하면 사용자 에이전트/헤더를 적용해 재시도합니다. 사이트 정책에 따라 접근 허용이 필요할 수 있습니다.
