from pydantic import BaseModel, Field
from pydantic import field_validator

class Publisher(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        title="출판사명",
        description="도서를 출판한 출판사의 이름",
        examples=["믿음"]
    )

    city: str = Field(
        default="서울",
        min_length=1,
        max_length=50,
        title="출판사 도시",
        description="출판사가 위치한 도시 이름",
        examples=["서울"]
    )


class BookCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        title="도서 제목",
        description="등록할 도서의 제목",
        examples=["처음 시작하는 FastAPI"]
    )

    author: str = Field(
        min_length=1,
        max_length=50,
        title="도서 저자",
        description="도서를 작성한 저자의 이름",
        examples=["홍길동"]
    )

    year: int = Field(
        ge=1900,
        le=2026,
        title="출판 연도",
        description="도서가 출판된 연도",
        examples=[2024]
    )

    tags: list[str] = Field(
        default_factory=list,
        title="도서 태그",
        description="도서와 관련된 태그 목록",
        examples=[["python", "web"]]
    )

    publisher: Publisher | None = Field(
        default=None,
        title="출판사 정보",
        description="도서의 출판사 정보",
        examples=[
            {
                "name": "믿음",
                "city": "서울"
            }
        ]
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "처음 시작하는 FastAPI",
                "author": "홍길동",
                "year": 2024,
                "tags": ["python", "web"],
                "publisher": {
                    "name": "믿음",
                    "city": "서울"
                }
            }
        }
    }

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("제목은 공백일 수 없습니다")

        return v


class BookResponse(BookCreate):
    id: int = Field(
        ge=1,
        title="도서 ID",
        description="도서를 구분하기 위한 고유 번호",
        examples=[1]
    )


class WeatherResponse(BaseModel):
    latitude: float = Field(
        ge=-90,
        le=90,
        title="위도",
        description="날씨 조회 지역의 위도",
        examples=[37.5665]
    )

    longitude: float = Field(
        ge=-180,
        le=180,
        title="경도",
        description="날씨 조회 지역의 경도",
        examples=[126.9780]
    )

    temperature: float = Field(
        title="기온",
        description="현재 기온(섭씨)",
        examples=[25.5]
    )

    time: str = Field(
        min_length=1,
        max_length=50,
        title="측정 시간",
        description="날씨 정보가 측정된 시간",
        examples=["2026-08-18T14:00"]
    )


class GoogleBooks(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        title="도서 제목",
        description="Google Books API에서 조회한 도서 제목",
        examples=["FastAPI"]
    )

    authors: list[str] = Field(
        default_factory=list,
        title="저자 목록",
        description="Google Books API에서 조회한 도서 저자 목록",
        examples=[["홍길동", "김철수"]]
    )

    published_date: str = Field(
        default="",
        max_length=30,
        title="출판일",
        description="Google Books API에서 제공하는 도서 출판일",
        examples=["2024-01-15"]
    )


class ExternalBook(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        title="외부 도서 제목",
        description="외부 API에서 조회한 도서 제목",
        examples=["처음 시작하는 FastAPI"]
    )

    authors: list[str] = Field(
        default_factory=list,
        title="외부 도서 저자",
        description="외부 API에서 조회한 도서 저자 목록",
        examples=[["홍길동"]]
    )

    published_date: str = Field(
        default="",
        max_length=30,
        title="외부 도서 출판일",
        description="외부 API에서 제공하는 도서 출판일",
        examples=["2024-01-15"]
    )