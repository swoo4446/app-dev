# 📚 FastAPI 도서 관리 API

FastAPI의 기본 구조와 REST API 동작 방식을 학습하기 위해 제작한  
**도서 관리 API 실습 프로젝트**입니다.

도서 조회부터 등록, 데이터 검증, 예외 처리까지 구현하고  
HTML / CSS / JavaScript를 활용한 웹 화면과 API를 연동했습니다.

## 🛠 Tech Stack

- Python
- FastAPI
- Pydantic
- HTML / CSS / JavaScript
- Swagger UI

## ✨ 주요 기능

### 📖 도서 조회

- 전체 도서 목록 조회
- 도서 ID 기반 단건 조회
- 제목 키워드 검색
- 저자별 필터링
- 출판 연도 정렬
- `skip`, `limit` 기반 페이지네이션

### ✏️ 도서 등록

- POST 요청을 통한 도서 등록
- 등록 완료 후 목록 자동 갱신
- 태그 및 출판사 정보 등록
- Pydantic 모델을 활용한 요청 데이터 검증
- 제목 중복 등록 방지

### ⚠️ 예외 및 상태 코드 처리

- `201 Created` : 도서 등록 성공
- `404 Not Found` : 존재하지 않는 도서 조회
- `409 Conflict` : 중복 도서 등록
- `422 Unprocessable Entity` : 입력값 검증 실패
- API 응답 상태에 따른 화면 메시지 처리

## 🔗 API

| Method | Endpoint | 기능 |
| --- | --- | --- |
| GET | `/health` | 서버 상태 확인 |
| GET | `/info` | API 정보 조회 |
| GET | `/books` | 전체 도서 조회 |
| GET | `/books/{book_id}` | 도서 단건 조회 |
| GET | `/books/search` | 제목 검색 |
| GET | `/books/filter` | 저자 필터 및 연도 정렬 |
| GET | `/books/page` | 페이지네이션 |
| POST | `/books` | 신규 도서 등록 |

## 🧩 데이터 모델

도서 등록 시 Pydantic을 활용하여 입력 데이터를 검증합니다.

- `title` : 1~20자
- `author` : 1~20자
- `year` : 1800~2026
- `tags` : 태그 목록
- `publisher` : 출판사 정보 (선택)
- 제목의 앞뒤 공백 제거 및 공백 제목 검증

## 🖥 Web UI

API 기능을 직접 확인할 수 있도록 정적 HTML 페이지를 구성했습니다.

### 1일차 — 조회

- 서버 상태 확인
- 전체 도서 목록
- 단건 조회
- 제목 검색
- 저자 필터 및 정렬
- 페이지네이션

### 2일차 — 등록과 검증

- 도서 등록 폼
- 입력값 검증 오류 표시
- 등록 후 목록 자동 갱신
- 404 상태 코드 처리
- 태그·출판사 입력
- 상태 코드 통합 처리

## 🚀 실행 방법

```bash
pip install fastapi uvicorn
python -m uvicorn main:app --reload
```

실행 후 Swagger UI에서 API를 테스트할 수 있습니다.

```text
http://127.0.0.1:8000/docs
```

## 📌 학습 내용

- FastAPI 기본 라우팅
- GET / POST 요청 처리
- Path Parameter / Query Parameter
- REST API 요청·응답 구조
- Pydantic `BaseModel`을 활용한 데이터 모델링
- `Field`를 활용한 입력값 검증
- `field_validator`를 활용한 사용자 정의 검증
- 중첩 모델(Nested Model) 처리
- HTTP 상태 코드와 `HTTPException` 활용
- `response_model`을 활용한 응답 구조 정의
- 리스트 컴프리헨션을 활용한 검색 및 필터링
- `sorted()`를 활용한 데이터 정렬
- `skip`, `limit` 기반 페이지네이션
- Fetch API를 활용한 프론트엔드 ↔ 백엔드 통신
- FastAPI와 HTML / CSS / JavaScript 연동
