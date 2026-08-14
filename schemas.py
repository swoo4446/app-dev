from pydantic import BaseModel, Field
from pydantic import field_validator

class Publisher(BaseModel):
    name: str
    city: str = "서울"

class BookCreate(BaseModel):
    title : str = Field(min_length=1, max_length=20)
    author: str = Field(min_length=1, max_length=20)
    year: int = Field(ge=1800, le=2026)
    tags: list[str] = Field(default_factory=list)
    publisher: Publisher | None = None
    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("제목은 공백일 수 없습니다")
        return v

class BookResponse(BookCreate):
    id: int

class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature: float
    time: str

class GoogleBooks(BaseModel):
    title:str
    authors:list[str] = Field(default_factory=list)
    published_data:str=""
      