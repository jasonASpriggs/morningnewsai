"""
Class for preferences and sentiment mixes
"""

from datetime import time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SentimentMix(BaseModel):
    model_config = ConfigDict(extra="forbid")

    constructive: float = Field(default=0.4, ge=0.0, le=1.0)
    adverse: float = Field(default=0.4, ge=0.0, le=1.0)
    neutral_or_mixed: float = Field(default=0.2, ge=0.0, le=1.0)

    @field_validator("neutral_or_mixed")
    @classmethod
    def validate_total_mix(cls, value: float, info) -> float:
        constructive = info.data.get("constructive", 0.0)
        adverse = info.data.get("adverse", 0.0)
        total = constructive + adverse + value

        if abs(total - 1.0) > 0.001:
            raise ValueError("Sentiment mix values must total 1.0")

        return value


class UserPreferences(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str = Field(min_length=1)
    timezone: str = "America/Chicago"
    generation_time: time = time(hour=6, minute=15)

    briefing_length: int = Field(default=10, ge=3, le=30)
    lookback_hours: int = Field(default=24, ge=1, le=168)

    topic_ids: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)

    sentiment_mix: SentimentMix = Field(default_factory=SentimentMix)

    maximum_articles_per_source: int = Field(default=3, ge=1, le=20)
    include_opinion: bool = False
    include_analysis: bool = True
    reuse_saved_preferences: bool = True
    automatic_generation_enabled: bool = False

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, value: str) -> str:
        try:
            ZoneInfo(value)
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"Unknown timezone: {value}") from error
        return value
