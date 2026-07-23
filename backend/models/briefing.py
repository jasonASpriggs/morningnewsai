"""
model Classes to define the overall daily breifing output sctructures
"""

from datetime import UTC, date, datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.models.article import Article
from backend.models.common import BriefingStatus, SentimentLabel


class BriefingItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position: int = Field(ge=1)
    article: Article
    briefing_summary: str = Field(min_length=1, max_length=1_500)
    why_included: str | None = Field(default=None, max_length=500)


class ThemeSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    summary: str = Field(min_length=1, max_length=2_000)
    article_ids: list[str] = Field(min_length=1)
    topic_ids: list[str] = Field(default_factory=list)
    overall_sentiment: SentimentLabel | None = None


class TopicSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic_id: str = Field(min_length=1)
    topic_name: str = Field(min_length=1, max_length=100)
    summary: str = Field(min_length=1, max_length=2_000)
    article_ids: list[str] = Field(default_factory=list)
    notable_developments: list[str] = Field(default_factory=list)


# Class for the ultimate news breifing output
class Briefing(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    briefing_date: date

    status: BriefingStatus = BriefingStatus.PENDING
    generated_at: datetime | None = None

    headline: str | None = Field(default=None, max_length=200)
    executive_summary: str | None = Field(default=None, max_length=3_000)

    items: list[BriefingItem] = Field(default_factory=list)
    topic_summaries: list[TopicSummary] = Field(default_factory=list)
    theme_summaries: list[ThemeSummary] = Field(default_factory=list)

    requested_topic_ids: list[str] = Field(default_factory=list)
    requested_source_ids: list[str] = Field(default_factory=list)

    candidate_article_count: int = Field(default=0, ge=0)
    selected_article_count: int = Field(default=0, ge=0)
    warnings: list[str] = Field(default_factory=list)
    error_message: str | None = None

    @classmethod
    def create_pending(
        cls,
        *,
        briefing_id: str,
        user_id: str,
        briefing_date: date,
        topic_ids: list[str],
        source_ids: list[str],
    ) -> "Briefing":
        return cls(
            id=briefing_id,
            user_id=user_id,
            briefing_date=briefing_date,
            status=BriefingStatus.PENDING,
            requested_topic_ids=topic_ids,
            requested_source_ids=source_ids,
        )

    def mark_completed(self) -> None:
        self.status = BriefingStatus.COMPLETED
        self.generated_at = datetime.now(UTC)
        self.selected_article_count = len(self.items)
