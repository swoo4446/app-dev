from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from schemas import BookResponse, BookCreate, ExternalBook, WeatherResponse, GoogleBooks
from external_api import fetch_books, fetch_books_multi, fetch_weather, load_fallback_books
import httpx
from external_api import fetch_books, fetch_weather, load_fallback_books
import time

tags_metadata = [
    {"name": "도서", "description": "도서 등록, 조회, 검색"},
    {"name": "외부 연동", "description": "Google Books와 날씨 API 연동"},
    {"name": "시스템", "description": "서버 상태 확인"},
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="도서 관리 API",
    description="도서를 등록·조회하고 외부 검색으로 정보를 가져오는 API",
    version="1.0.0",
    contact={"name": "이성우", "email": "swoo4446@gmail.com"},
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# 샘플 도서 데이터
books = [
    {"id": 1, "title": "파이썬 입문", "author": "김철수", "year": 2021},
    {"id": 2, "title": "FastAPI 실전", "author": "이영희", "year": 2023},
    {"id": 3, "title": "파이썬 웹개발", "author": "김철수", "year": 2022},
    {"id": 4, "title": "데이터 분석 기초", "author": "박민수", "year": 2020},
    {"id": 5, "title": "FastAPI로 배우는 백엔드", "author": "이영희", "year": 2024},
]


@app.get("/", tags=["시스템"], summary="API 기본 정보 조회")
def read_root():
    """API 기본 정보를 반환합니다."""
    return {"message": "도서 관리 API"}


@app.get("/health", tags=["시스템"], summary="서버 상태 확인")
def health():
    """서버 상태를 확인합니다."""
    return {"status": "ok"}


@app.get("/info", tags=["시스템"], summary="API 정보 조회")
def info():
    """API 이름과 버전을 반환합니다."""
    return {
        "name": "도서 관리 API",
        "version": "0.1.0",
    }


@app.get("/books", response_model=list[BookResponse], tags=["도서"], summary="도서 목록 조회")
def list_books():
    """전체 도서 목록을 조회합니다."""
    return books


@app.get("/books/search", tags=["도서"], summary="도서 검색")
def search_books(keyword: str = ""):
    """
    제목에 키워드가 포함된 도서를 검색합니다.

    - **keyword**: 도서 제목에 포함할 검색 키워드

    발생 가능한 오류 상태 코드는 없습니다.
    """
    if not keyword:
        return books

    return [book for book in books if keyword in book["title"]]


@app.get("/books/filter", tags=["도서"], summary="도서 필터링 및 정렬")
def filter_books(author: str = "", sort: str = ""):
    """
    저자로 도서를 필터링하고 출판 연도로 정렬합니다.

    - **author**: 필터링할 저자명
    - **sort**: 정렬 기준. 예: year

    발생 가능한 오류 상태 코드는 없습니다.
    """
    result = books

    if author:
        #리스트 컴프리헨션 - for+if > 리스트
        result = [book for book in result if book["author"] == author]

    if sort == "year":
        result = sorted(result, key=lambda book: book["year"])

    return result


@app.get("/books/page", tags=["도서"], summary="도서 목록 페이지 조회")
def page_books(skip: int = 0, limit: int = 2):
    """
    도서 목록을 페이지 단위로 조회합니다.

    - **skip**: 건너뛸 도서 수
    - **limit**: 조회할 도서 수

    발생 가능한 오류 상태 코드는 없습니다.
    """
    return books[skip:skip + limit]


@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="도서 등록",
    response_description="등록된 도서 정보", tags=["도서"],
    responses={
        409: {"description": "이미 등록된 제목입니다"}
    }
)
def create_book(book: BookCreate):
    """
    새 도서를 등록합니다.

    - **book**: 등록할 도서 정보

    동일한 제목의 도서가 있으면 409 상태 코드를 반환합니다.
    """
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(status_code=409, detail="이미 등록된 제목입니다")
    new_id = max([b["id"] for b in books], default=0) + 1

    new_book = {
        "id": new_id, **book.model_dump()
    }

    books.append(new_book)

    return new_book


@app.get(
    "/weather",
    response_model=WeatherResponse,
    tags=["외부 연동"],
    summary="날씨 정보 조회"
)
async def weather(latitude: float = 36.8, longitude: float = 127.1):
    """
    지정한 위치의 날씨 정보를 조회합니다.

    - **latitude**: 조회할 위치의 위도
    - **longitude**: 조회할 위치의 경도

    발생 가능한 오류 상태 코드는 없습니다.
    """
    return await fetch_weather(latitude, longitude)


#endpoint
@app.get(
    "/book/googleBooks",
    response_model=list[GoogleBooks],
    tags=["외부 연동"],
    summary="외부 도서 검색"
)
async def search_books_external(keyword: str, limit: int = 5):
    """
    외부 도서 정보를 검색합니다.

    - **keyword**: 검색할 도서 키워드
    - **limit**: 조회할 도서 수

    발생 가능한 오류 상태 코드는 없습니다.
    """
    return await fetch_books(keyword, limit)


# 리터럴 경로이므로 /books/{book_id}보다 먼저 선언한다
@app.get(
    "/books/external",
    response_model=list[ExternalBook],
    tags=["외부 연동"],
    summary="외부 도서 검색",
    responses={
        504: {"description": "외부 API 응답이 지연됩니다"},
        502: {"description": "외부 API가 오류를 반환했습니다"}
    }
)
async def search_external_books(keyword: str, limit: int = 5, fallback: bool = False):
    """
    외부 API에서 도서 정보를 검색합니다.

    - **keyword**: 검색할 도서 키워드
    - **limit**: 조회할 도서 수
    - **fallback**: 외부 API 오류 발생 시 대체 데이터 사용 여부

    외부 API 응답 지연 시 504 상태 코드, 외부 API 오류 또는 연결 실패 시 502 상태 코드를 반환합니다.
    """
    try:
        return await fetch_books(keyword, limit)
    except httpx.TimeoutException:
        if fallback:
            return load_fallback_books()
        raise HTTPException(status_code=504, detail="외부 API 응답이 지연됩니다")
    except httpx.HTTPStatusError:
        if fallback:
            return load_fallback_books()
        raise HTTPException(status_code=502, detail="외부 API가 오류를 반환했습니다")
    except httpx.RequestError:
        if fallback:
            return load_fallback_books()
        raise HTTPException(status_code=502, detail="외부 API에 연결할 수 없습니다")


@app.post(
    "/books/from-external",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["외부 연동"],
    summary="외부 도서 등록",
    responses={
        409: {"description": "이미 등록된 제목입니다"}
    }
)
def create_from_external(book: ExternalBook):
    """
    외부 도서 정보를 등록합니다.

    - **book**: 등록할 외부 도서 정보

    동일한 제목의 도서가 있으면 409 상태 코드를 반환합니다.
    """
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(status_code=409, detail="이미 등록된 제목입니다")
    year = 2000
    if book.published_date[:4].isdigit():
        year = int(book.published_date[:4])
    new_id = max([b["id"] for b in books], default=0) + 1
    new_book = {
        "id": new_id,
        "title": book.title,
        "author": book.authors[0] if book.authors else "미상",
        "year": year,
        "tags": ["외부검색"],
        "publisher": None,
    }
    books.append(new_book)
    return new_book


@app.get(
    "/books/external/multi",
    tags=["외부 연동"],
    summary="다중 외부 도서 검색"
)
async def search_multi(keywords: str = "python,fastapi,django"):
    """
    여러 키워드로 외부 도서 정보를 검색합니다.

    - **keywords**: 쉼표로 구분한 도서 검색 키워드

    발생 가능한 오류 상태 코드는 없습니다.
    """
    words = [w.strip() for w in keywords.split(",") if w.strip()]

    start = time.perf_counter()
    results = await fetch_books_multi(words)
    elapsed = round(time.perf_counter() - start, 2)

    return {"elapsed_seconds": elapsed, "results": results}


@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["도서"],
    summary="도서 단건 조회",
    responses={
        404: {"description": "도서를 찾을 수 없습니다."}
    }
)
def read_book(book_id: int):
    """
    ID를 이용해 특정 도서를 조회합니다.

    - **book_id**: 조회할 도서의 ID

    해당 번호의 도서가 없으면 404 상태 코드를 반환합니다.
    """
    for book in books:
       if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")