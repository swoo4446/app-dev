from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from schemas import BookResponse, BookCreate, WeatherResponse, GoogleBooks
from external_api import fetch_weather, fetch_books
import httpx

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

@app.get("/books", response_model=list[BookResponse])
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
        #리스트 컴프리헨션 - for+if > 리스트
        result = [book for book in result if book["author"] == author]

    if sort == "year":
        result = sorted(result, key=lambda book: book["year"])

    return result

@app.get("/books/page")
def page_books(skip: int = 0, limit: int = 2):
    """도서 목록을 페이지 단위로 조회합니다."""
    return books[skip:skip + limit]

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    for b in books:
        if b["title"] == book.title:
            raise HTTPException(status_code=409, detail="이미 등록된 제목입니다")
    new_id = max([b["id"] for b in books], default=0) + 1

    new_book = {
        "id": new_id, **book.model_dump()
    }

    books.append(new_book)

    return new_book

@app.get("/weather", response_model=WeatherResponse)
async def weather(latitude: float = 36.8, longitude: float = 127.1):
     return await fetch_weather(latitude, longitude)

#endpoint
@app.get("/book/googleBooks", response_model=list[GoogleBooks])
async def search_books_external(keyword:str, limit:int = 5):
    return await fetch_books(keyword,limit)

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int):
    """ID를 이용해 특정 도서를 조회합니다."""
    for book in books:
       if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")