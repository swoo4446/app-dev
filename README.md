# 📚 FastAPI 도서 관리 API

FastAPI의 기본 구조와 REST API 동작 방식을 학습하기 위해 제작한  
**도서 관리 API 실습 프로젝트**입니다.

## 🛠 Tech Stack

- Python
- FastAPI
- Uvicorn
- HTML / CSS / JavaScript

## ✨ 주요 기능

- 서버 상태 및 API 정보 조회
- 전체 도서 목록 조회
- 도서 ID 기반 단건 조회
- 제목 키워드 검색
- 저자별 필터링
- 출판 연도 정렬
- `skip`, `limit` 기반 페이지네이션
- 정적 HTML 페이지 연동
- Swagger UI를 활용한 API 테스트

## 🔗 API

| Method | Endpoint | 기능 |
| --- | --- | --- |
| GET | `/health` | 서버 상태 확인 |
| GET | `/info` | API 정보 조회 |
| GET | `/books` | 전체 도서 조회 |
| GET | `/books/{book_id}` | 도서 단건 조회 |
| GET | `/books/search` | 제목 검색 |
| GET | `/books/filter` | 저자 필터 및 정렬 |
| GET | `/books/page` | 페이지네이션 |

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
- Path Parameter / Query Parameter
- REST API 요청·응답 구조
- 리스트 컴프리헨션을 활용한 검색 및 필터링
- `sorted()`를 활용한 데이터 정렬
- `skip`, `limit` 기반 페이지네이션
- FastAPI와 HTML / CSS / JavaScript 연동

sorted()를 활용한 데이터 정렬

skip, limit 기반 페이지네이션

FastAPI와 HTML/CSS/JavaScript 연동
