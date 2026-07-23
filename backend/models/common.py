"""
Create commonly used and general classes of StrEnums
"""

from enum import StrEnum


class RetrievalMethod(StrEnum):
    RSS = "rss"
    API = "api"
    SEARCH = "search"


class SentimentLabel(StrEnum):
    CONSTRUCTIVE = "constructive"
    ADVERSE = "adverse"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class ContentType(StrEnum):
    NEWS = "news"
    ANALYSIS = "analysis"
    OPINION = "opinion"
    EXPLAINER = "explainer"
    UNKNOWN = "unknown"


class BriefingStatus(StrEnum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
