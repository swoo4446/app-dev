from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="도서 관리 API",
    description="FastAPI를 활용한 도서 조회, 검색, 필터링 및 페이지네이션 실습",
    version="0.1.0",
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


@app.get("/")
def read_root():
    """API 기본 정보를 반환합니다."""
    return {"message": "도서 관리 API"}


@app.get("/health")
def health():
    """서버 상태를 확인합니다."""
    return {"status": "healthy"}


@app.get("/info")
def info():
    """API 이름과 버전을 반환합니다."""
    return {
        "name": "도서 관리 API",
        "version": "0.1.0",
    }


@app.get("/books")
def list_books():
    """전체 도서 목록을 조회합니다."""
    return books


@app.get("/books/search")
def search_books(keyword: str = ""):
    """제목에 키워드가 포함된 도서를 검색합니다."""
    if not keyword:
        return books

    return [book for book in books if keyword in book["title"]]


@app.get("/books/filter")
def filter_books(author: str = "", sort: str = ""):
    """저자로 필터링하고 출판 연도로 정렬합니다."""
    result = books

    if author:
        result = [book for book in result if book["author"] == author]

    if sort == "year":
        result = sorted(result, key=lambda book: book["year"])

    return result


@app.get("/books/page")
def page_books(skip: int = 0, limit: int = 2):
    """도서 목록을 페이지 단위로 조회합니다."""
    return books[skip:skip + limit]


@app.get("/books/{book_id}")
def read_book(book_id: int):
    """ID를 이용해 특정 도서를 조회합니다."""
    for book in books:
        if book["id"] == book_id:
            return book

    return {"error": "Book not found"}