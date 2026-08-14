import httpx
from schemas import WeatherResponse, GoogleBooks
import requests
import os
from dotenv import load_dotenv

async def fetch_weather(latitude: float, longitude: float) -> WeatherResponse:
    async with httpx.AsyncClient(timeout=5.0) as client:
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


load_dotenv()
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

#os.getenv 는 값이 없어도 오류를 내지 않고 조용히 None 을 돌려줍니다. 서버 시작 시 확인하는 코드를 넣어 두면 원인 파악이 쉽다
if not GOOGLE_BOOKS_API_KEY:
    print("경고: GOOGLE_BOOKS_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

async def fetch_books(book_title_keyword:str, limit:int = 5) -> list[GoogleBooks]: #5개까지만 나오게
    async with httpx.AsyncClient(timeout=5.0) as client:
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