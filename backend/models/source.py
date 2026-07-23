"""
Create classe to define the news source
"""

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from backend.models.common import RetrievalMethod


class NewsSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(
        min_length=1,
        pattern=r"^[a-z0-9][a-z0-9_-]*$",
        description="Stable identifier such as ap-news.",
    )
    name: str = Field(min_length=1, max_length=100)
    retrieval_method: RetrievalMethod
    domains: list[str] = Field(min_length=1)
    feed_urls: list[HttpUrl] = Field(default_factory=list)
    enabled: bool = True
    maximum_articles_per_briefing: int = Field(default=3, ge=1, le=20)


"""
Example Implementation::

from backend.models.common import RetrievalMethod
from backend.models.source import NewsSource


ap_source = NewsSource(
    id="ap-news",
    name="Associated Press",
    domains=["apnews.com"],
    retrieval_method=RetrievalMethod.SEARCH,
    maximum_articles_per_briefing=3,
)
"""
