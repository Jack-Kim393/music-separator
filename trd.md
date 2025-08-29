# 기술 요구사항 명세서 (TRD): Music Separator UI

## 1. 시스템 아키텍처

단순성과 빠른 구현을 위해 파이썬 기반의 백엔드 서버와 경량 프론트엔드로 구성한다.

*   **프론트엔드 (Frontend)**: 순수 HTML, CSS, JavaScript를 사용한 단일 페이지 애플리케이션(SPA). 파일 업로드, 상태 폴링, 결과 표시 등 모든 사용자 인터랙션을 처리한다.
*   **백엔드 (Backend)**: Flask 또는 FastAPI를 사용한 경량 파이썬 웹 서버.
    *   프론트엔드로부터 오디오 파일을 받아 처리 요청을 접수한다.
    *   기존의 `music_separator.py` 스크립트를 백그라운드 프로세스로 실행하여 실제 음원 분리를 수행한다.
    *   분리 작업의 진행 상태를 프론트엔드에 알려주고, 완료된 파일의 경로를 제공한다.

## 2. 기술 스택

*   **백엔드**: Python, Flask (또는 FastAPI), Spleeter
*   **프론트엔드**: HTML5, CSS3, JavaScript (Fetch API, DOM 조작)
*   **API 통신**: RESTful API (JSON 형식)

## 3. API 엔드포인트 명세

*   **`POST /api/upload`**: 음원 파일을 업로드하고 분리 작업을 시작한다.
    *   **Request**: `multipart/form-data` 형식의 오디오 파일
    *   **Response**: `202 Accepted`, `{ "task_id": "고유_작업_ID" }`

*   **`GET /api/status/<task_id>`**: 특정 작업의 진행 상태를 확인한다.
    *   **Response**: `{ "status": "processing" | "complete" | "error", "message": "상태 메시지" }`

*   **`GET /api/tracks`**: 분리가 완료된 모든 트랙의 목록을 가져온다.
    *   **Response**:
        ```json
        [
          {
            "original_title": "Diamond_Boy",
            "tracks": [
              { "name": "vocals", "url": "/separated_music/Diamond_Boy/vocals.wav" },
              { "name": "accompaniment", "url": "/separated_music/Diamond_Boy/accompaniment.wav" }
            ]
          }
        ]
        ```

*   **`/separated_music/*`**: 분리된 오디오 파일에 접근하기 위한 정적 파일 서빙 경로.

## 4. 데이터 흐름

1.  사용자가 프론트엔드 UI를 통해 파일을 업로드한다.
2.  프론트엔드는 백엔드의 `POST /api/upload`로 파일을 전송한다.
3.  백엔드는 파일을 저장하고, Spleeter를 사용한 분리 작업을 백그라운드로 시작시킨 후 `task_id`를 즉시 반환한다.
4.  프론트엔드는 받은 `task_id`를 이용해 `GET /api/status/<task_id>`를 주기적으로 호출(폴링)하여 작업 상태를 확인한다.
5.  상태가 'complete'가 되면, 프론트엔드는 `GET /api/tracks`를 호출하여 전체 트랙 목록을 갱신한다.
6.  화면에 표시된 트랙의 URL을 통해 사용자는 파일을 재생하거나 다운로드한다.

## 5. 오류 처리

*   **파일 업로드 오류**: 지원하지 않는 파일 형식이거나 파일 크기가 너무 클 경우 오류를 반환한다.
*   **음원 분리 오류**: Spleeter 처리 중 발생하는 예외를 감지하여 'error' 상태와 메시지를 반환한다.
*   **API 통신 오류**: 네트워크 문제 등으로 API 요청이 실패할 경우 재시도 로직을 구현하거나 사용자에게 알린다.
