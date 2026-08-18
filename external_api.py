from schemas import WeatherResponse, ExternalBook, GoogleBooks
from schemas import ExternalBook, WeatherResponse
from dotenv import load_dotenv
from pathlib import Path
import httpx
import os
import json
import asyncio
# import requests

load_dotenv()
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
if not GOOGLE_BOOKS_API_KEY:
    print("경고: GOOGLE_BOOKS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
EXTERNAL_TIMEOUT = float(os.getenv("EXTERNAL_TIMEOUT", "5.0"))

async def fetch_weather(latitude: float, longitude: float) -> WeatherResponse:
    async with httpx.AsyncClient(timeout=EXTERNAL_TIMEOUT) as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m",
            },
        )
        response.raise_for_status()
        data = response.json()

    return WeatherResponse(
        latitude=data["latitude"],
        longitude=data["longitude"],
        temperature=data["current"]["temperature_2m"],
        time=data["current"]["time"],
    )

async def fetch_books(keyword: str, limit: int = 5) -> list[ExternalBook]:
    async with httpx.AsyncClient(timeout=EXTERNAL_TIMEOUT) as client:
        response = await client.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": keyword, "maxResults": limit, "key": GOOGLE_BOOKS_API_KEY},
        )
        response.raise_for_status()
        data = response.json()

    result = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        result.append(
            ExternalBook(
                title=info.get("title", "제목 없음"),
                authors=info.get("authors", []),
                published_date=info.get("publishedDate", ""),
            )
        )
    return result

async def fetch_books(book_title_keyword:str, limit:int = 5) -> list[GoogleBooks]: #5개까지만 나오게
    async with httpx.AsyncClient(timeout=EXTERNAL_TIMEOUT) as client:
        response = await client.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={
                "q": book_title_keyword,
                "maxResult" : limit,
                "key": GOOGLE_BOOKS_API_KEY,
            },
        )
        data = response.json()

    #GoobleBooks 생성
    result_book_list = []
    for item in data.get('items', [])[:limit]:
        book_info = item.get('volumeInfo',{}) #책 1권 정보가 딕셔너리였음

        result_book_list.append(GoogleBooks( #구글북스 형태로 바꿈
                title= book_info.get('title','-'),
                authors= book_info.get('authors',[]),
                published_data= book_info.get('publishedDate','-')
            )
        )

    return result_book_list

def load_fallback_books() -> list[ExternalBook]:
    path = Path(__file__).parent / "sample_books.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [ExternalBook(**item) for item in raw]

async def _fetch_titles(client: httpx.AsyncClient, keyword: str) -> dict:
    response = await client.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": keyword, "maxResults": 3, "key": GOOGLE_BOOKS_API_KEY},
    )
    data = response.json()
    titles = [
        item.get("volumeInfo", {}).get("title", "제목 없음")
        for item in data.get("items", [])
    ]
    return {"keyword": keyword, "titles": titles}

async def fetch_books_multi(keywords: list[str]) -> list[dict]:
    async with httpx.AsyncClient(timeout=EXTERNAL_TIMEOUT * 2) as client:
        return await asyncio.gather(*[_fetch_titles(client, k) for k in keywords])