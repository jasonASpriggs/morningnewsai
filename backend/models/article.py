"""
Class model for the news articles
"""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from backend.models.common import ContentType, SentimentLabel


class Article(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        min_length=1, description="Stable hash or provider-specific article identifier."
    )
    title: str = Field(min_length=1, max_length=500)
    source_id: str = Field(min_length=1)
    source_name: str = Field(min_length=1, max_length=500)

    url: HttpUrl
    canonical_url: HttpUrl | None = None

    published_at: datetime | None = None
    retreived_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    author: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=2_000)

    topic_ids: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)

    content_type: ContentType = ContentType.UNKNOWN
    sentiment: SentimentLabel | None = None
    sentiment_score: float | None = Field(default=None, ge=-1.0, le=1.0)
    sentiment_confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    relevance_score: float | None = Field(default=None, ge=0.0, le=1.0)
    quality_score: float | None = Field(default=None, ge=0.0, le=1.0)
    summary: str | None = Field(default=None, max_length=2_000)
