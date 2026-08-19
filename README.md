# FastAPI 도서 관리 API

## 프로젝트 요약

 FastAPI로 **도서 CRUD와 검색·필터링·페이지네이션을 구현하고 Google Books와 Open-Meteo 같은 외부 API 연동까지 확장한 백엔드 학습 프로젝트**입니다.

 도서 데이터는 `books_data.json`에 저장하며 Pydantic으로 요청과 응답 데이터를 검증합니다. API는 기능별 Router로 분리되어 있고 Swagger UI와 정적 HTML 페이지에서 동작을 확인할 수 있습니다.

주요 기능은 다음과 같습니다.

- 도서 조회, 등록, 전체 수정, 부분 수정, 삭제
- 제목 검색, 저자 필터링, 출판 연도 정렬, 페이지네이션
- Pydantic 기반 데이터 검증
- JSON 파일 기반 데이터 저장
- Google Books 도서 검색
- Open-Meteo 날씨 조회
- 404, 409, 502, 504 등 상황별 예외 처리
- OpenAPI 및 Swagger UI를 활용한 API 문서화

---

## 프로젝트 구조

```text
app-dev/
├── main.py                 # FastAPI 앱 생성 및 Router 등록
├── database.py             # 도서 데이터 로드·저장
├── schemas.py              # Pydantic 요청·응답 모델
├── external_api.py         # Google Books / Open-Meteo 호출
├── books_data.json         # 저장된 도서 데이터
├── sample_books.json       # 외부 API 실패 시 사용할 예비 데이터
├── routers/
│   ├── books.py            # 도서 CRUD·검색·필터·페이지네이션
│   ├── external.py         # 외부 도서 검색·날씨 조회
│   └── system.py           # 루트·헬스체크·앱 정보
├── static/                 # API 기능 확인용 HTML 페이지
│   ├── index.html
│   └── 01-status.html ~ 12-final.html
└── etc/                    # 학습 관련 보조 문서
```

 `main.py`에서는 FastAPI 앱을 생성하고 각 Router와 정적 파일 경로를 연결합니다.
 `routers/books.py`는 도서 CRUD와 검색 기능을 담당하고 `routers/external.py`는 Google Books와 날씨 API 같은 외부 서비스 연동을 처리합니다.

 `database.py`는 JSON 파일에서 도서 데이터를 읽고 저장하며 `schemas.py`에는 도서와 출판사, 날씨, 외부 도서 등 API에서 사용하는 Pydantic 모델과 검증 규칙이 정의되어 있습니다.

---

## 실행 방법

먼저 가상환경을 생성합니다.

```bash
python -m venv .venv
```

Windows에서는 다음 명령어로 활성화합니다.

```bash
.venv\Scripts\activate
```

macOS 또는 Linux에서는 다음 명령어를 사용합니다.

```bash
source .venv/bin/activate
```

프로젝트에서 사용하는 주요 패키지를 설치합니다.

```bash
pip install fastapi uvicorn pydantic httpx python-dotenv
```

외부 API 기능을 사용하려면 프로젝트 루트에 `.env` 파일을 생성합니다.

```env
GOOGLE_BOOKS_API_KEY=발급받은_API_KEY
EXTERNAL_TIMEOUT=5.0
```

`GOOGLE_BOOKS_API_KEY`는 Google Books API 요청에 사용하며, `EXTERNAL_TIMEOUT`은 외부 API의 최대 응답 대기 시간을 지정합니다. 별도로 설정하지 않으면 `5.0`초를 사용합니다.

서버는 다음 명령어로 실행합니다.

```bash
python -m uvicorn main:app --reload
```

서버가 실행되면 다음 주소에서 주요 기능을 확인할 수 있습니다.

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI 명세: `http://127.0.0.1:8000/openapi.json`
- 정적 학습 화면: `http://127.0.0.1:8000/static/index.html`
- 서버 상태 확인: `http://127.0.0.1:8000/health`

---

## 주요 API

### 시스템 API

| Method | Endpoint | 설명 |
| --- | --- | --- |
| `GET` | `/` | API 기본 메시지 |
| `GET` | `/health` | 서버 상태 확인 |
| `GET` | `/info` | API 이름과 버전 확인 |

### 도서 API

| Method | Endpoint | 설명 |
| --- | --- | --- |
| `GET` | `/books` | 전체 도서 목록 조회 |
| `POST` | `/books` | 신규 도서 등록 |
| `GET` | `/books/search?keyword=...` | 제목 키워드 검색 |
| `GET` | `/books/filter?author=...&sort=year` | 저자 필터 및 연도 정렬 |
| `GET` | `/books/page?skip=0&limit=2` | 페이지네이션 |
| `GET` | `/books/{book_id}` | 도서 단건 조회 |
| `PUT` | `/books/{book_id}` | 도서 정보 전체 수정 |
| `PATCH` | `/books/{book_id}` | 전달한 필드만 부분 수정 |
| `DELETE` | `/books/{book_id}` | 도서 삭제 |

### 외부 API 연동

| Method | Endpoint | 설명 |
| --- | --- | --- |
| `GET` | `/weather` | 위도·경도 기준 현재 날씨 조회 |
| `GET` | `/books/external` | Google Books 도서 검색 |
| `GET` | `/books/external/multi` | 여러 키워드 동시 검색 |
| `POST` | `/books/from-external` | 외부 검색 결과를 도서 목록에 등록 |

 외부 API 호출이 지연되거나 연결에 실패하면 `502`, `504` 상태 코드를 반환합니다. `/books/external`에서 `fallback=true` 옵션을 사용하면 오류 발생 시 `sample_books.json`에 저장된 예비 데이터를 사용할 수 있습니다.

---

## 데이터 모델과 검증

 도서 등록 요청은 `BookCreate` 모델을 기준으로 검증합니다.

```json
{
  "title": "처음 시작하는 FastAPI",
  "author": "홍길동",
  "year": 2024,
  "tags": ["python", "web"],
  "publisher": {
    "name": "믿음",
    "city": "서울"
  }
}
```

 주요 검증 규칙은 다음과 같습니다.

| 필드 | 검증 규칙 |
| --- | --- |
| `title` | 1~100자, 앞뒤 공백 제거, 공백만 입력 불가 |
| `author` | 1~50자 |
| `year` | 1900~2026 |
| `tags` | 문자열 목록 |
| `publisher` | 선택 입력, 출판사명과 도시를 중첩 모델로 관리 |

등록된 도서에는 `id`가 추가되고 `books_data.json`에 저장됩니다.

---

## 주요 HTTP 상태 코드

| 상태 코드 | 의미 | 사용 예 |
| --- | --- | --- |
| `200 OK` | 요청 성공 | 조회, 수정 |
| `201 Created` | 리소스 생성 성공 | 도서 등록 |
| `204 No Content` | 삭제 성공 | 도서 삭제 |
| `404 Not Found` | 리소스를 찾을 수 없음 | 존재하지 않는 도서 조회 |
| `409 Conflict` | 중복 데이터 | 같은 제목의 도서 등록 |
| `422 Unprocessable Entity` | 요청 데이터 검증 실패 | 필드 형식 또는 범위 오류 |
| `502 Bad Gateway` | 외부 API 연결 또는 응답 오류 | 외부 서비스 장애 |
| `504 Gateway Timeout` | 외부 API 응답 지연 | Timeout 초과 |

---

## 학습 포인트

 이 프로젝트에서는 FastAPI의 기본 API 구현부터 외부 서비스 연동까지 단계적으로 확인했습니다.

 특히, `APIRouter`를 활용한 기능별 라우터 분리, `GET`, `POST`, `PUT`, `PATCH`, `DELETE`를 이용한 REST API 구성, Path Parameter와 Query Parameter 처리, Pydantic 기반 요청·응답 검증을 연습할 수 있습니다. 또한, JSON 파일을 이용한 간단한 데이터 영속화, `HTTPException`을 이용한 예외 처리, `httpx.AsyncClient`와 `asyncio.gather()`를 활용한 비동기 외부 API 호출도 포함되어 있습니다.

 FastAPI가 자동으로 생성하는 OpenAPI 명세와 Swagger UI를 확인할 수 있으며 `StaticFiles`와 Fetch API를 사용해 정적 HTML 화면에서 백엔드 API를 호출하는 흐름도 살펴볼 수 있습니다.

---

## 참고

 현재 프로젝트는 데이터베이스 대신 JSON 파일을 사용하는 구조입니다. `books_data.json`은 실행 중 변경될 수 있으며 `.gitignore`에 포함되어 있습니다.

 외부 API 기능을 사용하려면 `.env`에 필요한 환경변수를 설정한 뒤 서버를 실행하셔야 합니다.