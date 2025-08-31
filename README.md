# 🎵 Music Separator

이 프로젝트는 Deezer의 Spleeter 라이브러리를 사용하여 음악 파일에서 보컬과 반주를 분리하는 웹 애플리케이션입니다.

## 기능

-   **웹 UI 제공**: 사용하기 쉬운 웹 인터페이스를 통해 파일을 업로드하고 결과를 확인할 수 있습니다.
-   **음원 분리**: 지정된 음악 파일에서 보컬(목소리)과 반주(악기) 트랙을 분리합니다.
-   **실시간 상태 확인**: 파일 업로드부터 음원 분리 완료까지의 과정을 실시간으로 확인할 수 있습니다.
-   **즉시 재생 및 다운로드**: 분리된 트랙을 웹에서 바로 재생하거나 다운로드할 수 있습니다.

## Docker를 사용하여 실행하기

Docker와 Docker Compose가 설치되어 있다면, 다음 명령어로 모든 서비스를 한 번에 실행할 수 있습니다.

1.  **Docker 이미지 빌드 및 컨테이너 실행:**

    ```bash
    docker-compose up --build -d
    ```

2.  **웹 브라우저 접속:**

    웹 브라우저를 열고 주소창에 `http://localhost`를 입력하여 접속합니다.

3.  **서비스 종료:**

    ```bash
    docker-compose down
    ```

### Docker Compose 서비스 설명

*   **`nginx`**: 웹 서버. 정적 파일(HTML, CSS, JS)을 서빙하고, API 요청을 `api` 서비스로 전달하는 리버스 프록시 역할을 합니다.
*   **`api`**: Flask 웹 애플리케이션. 파일 업로드 및 상태 확인 등 핵심적인 API 로직을 처리합니다.
*   **`worker`**: Celery 워커. `api` 서비스로부터 음원 분리 작업을 받아 백그라운드에서 비동기적으로 처리합니다.
*   **`redis`**: 메시지 브로커. `api`와 `worker` 간의 작업 큐를 관리합니다.

## 폴더 구조

```
music-separator/
├── .venv/                  # 파이썬 가상 환경
├── static/
│   ├── css/style.css       # UI 스타일시트
│   └── js/main.js          # 프론트엔드 로직
├── templates/
│   └── index.html          # 메인 웹페이지
├── uploads/                # 사용자가 업로드한 원본 파일 저장소
├── separated_music/        # 분리된 음원 파일이 저장되는 폴더
├── app.py                  # 웹 서버 실행 파일 (Flask)
├── Dockerfile              # Docker 이미지 생성을 위한 설정 파일
├── docker-compose.yml      # Docker 서비스 관리를 위한 설정 파일
├── requirements.txt        # 프로젝트 의존성 목록
└── README.md               # 프로젝트 설명 파일
```

## 주요 의존성

-   `spleeter`: 핵심 음원 분리 라이브러리
-   `Flask`: 웹 서버 프레임워크
-   `Celery`: 비동기 작업 큐
-   `Redis`: Celery 메시지 브로커
-   `gunicorn`: WSGI 서버

*   `requirements.txt` 파일을 통해 필요한 모든 라이브러리를 설치할 수 있습니다.

## 로컬 환경에서 실행하기 (참고용)

1.  **가상 환경 활성화** (터미널에서 최초 한 번 실행):
    ```bash
    # Windows
    .venv\Scripts\activate
    
    # macOS/Linux
    source .venv/bin/activate
    ```

2.  **필요한 라이브러리 설치:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **웹 서버 실행**:
    프로젝트 루트 폴더에서 아래 명령어를 실행하여 웹 서버를 시작합니다.
    ```bash
    python app.py
    ```

4.  **웹 브라우저 접속**:
    웹 브라우저를 열고 주소창에 `http://127.0.0.1:5000` 또는 `http://localhost:5000` 을 입력하여 접속합니다.