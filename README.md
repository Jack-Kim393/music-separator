# 🎵 Music Separator

이 프로젝트는 Deezer의 Spleeter 라이브러리를 사용하여 음악 파일에서 보컬과 반주를 분리하는 웹 애플리케이션입니다.

## 기능

-   **웹 UI 제공**: 사용하기 쉬운 웹 인터페이스를 통해 파일을 업로드하고 결과를 확인할 수 있습니다.
-   **음원 분리**: 지정된 음악 파일에서 보컬(목소리)과 반주(악기) 트랙을 분리합니다.
-   **실시간 상태 확인**: 파일 업로드부터 음원 분리 완료까지의 과정을 실시간으로 확인할 수 있습니다.
-   **즉시 재생 및 다운로드**: 분리된 트랙을 웹에서 바로 재생하거나 다운로드할 수 있습니다.

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
├── music_separator.py      # 핵심 음원 분리 스크립트
├── requirements.txt        # 프로젝트 의존성 목록
└── README.md               # 프로젝트 설명 파일
```

## 주요 의존성

-   `spleeter`: 핵심 음원 분리 라이브러리
-   `Flask`: 웹 서버 프레임워크

*   `requirements.txt` 파일을 통해 필요한 모든 라이브러리를 설치할 수 있습니다.

```bash
pip install -r requirements.txt
```

## 사용법 (Web UI)

1.  **가상 환경 활성화** (터미널에서 최초 한 번 실행):
    ```bash
    # Windows
    .venv\Scripts\activate
    
    # macOS/Linux
    source .venv/bin/activate
    ```

2.  **웹 서버 실행**:
    프로젝트 루트 폴더에서 아래 명령어를 실행하여 웹 서버를 시작합니다.
    ```bash
    python app.py
    ```

3.  **웹 브라우저 접속**:
    웹 브라우저를 열고 주소창에 `http://127.0.0.1:5000` 또는 `http://localhost:5000` 을 입력하여 접속합니다.

4.  **음원 분리**:
    -   웹페이지의 '파일 선택' 버튼을 누르거나 파일을 드래그 앤 드롭하여 음원을 업로드합니다.
    -   업로드가 완료되면 자동으로 음원 분리가 시작되며, 진행 상태가 표시됩니다.
    -   완료 후, 결과 목록에서 분리된 트랙을 바로 듣거나 다운로드할 수 있습니다.

---

### 기존 CLI 사용법 (참고용)

웹 UI 없이 기존의 커맨드 라인 스크립트를 직접 실행할 수도 있습니다.

```bash
python .venv/music_separator.py -i "Diamond_Boy.mp3"
```
