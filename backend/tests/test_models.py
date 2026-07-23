from datetime import date

import pytest
from pydantic import ValidationError

from backend.models import Briefing, BriefingStatus, NewsTopic, SentimentMix, UserPreferences


def test_create_topic() -> None:
    topic = NewsTopic(
        id="climate-change",
        name="Climate Change",
        query='"climate change" OR "climate policy"',
        include_domains=["apnews.com"],
    )

    assert topic.enabled is True
    assert topic.weight == 1.0
    assert topic.include_domains == ["apnews.com"]


def test_sentiment_mix_must_total_one() -> None:
    with pytest.raises(ValidationError):
        SentimentMix(constructive=0.5, adverse=0.5, neutral_or_mixed=0.5)


def test_default_preferences() -> None:
    preferences = UserPreferences(user_id="local-user")

    assert preferences.timezone == "America/Chicago"
    assert preferences.briefing_length == 10
    assert preferences.reuse_saved_preferences is True


def test_invalid_timezone_is_rejected() -> None:
    with pytest.raises(ValidationError):
        UserPreferences(user_id="local-user", timezone="Not/A-Timezone")


def test_create_pending_briefing() -> None:
    briefing = Briefing.create_pending(
        briefing_id="local-user-2026-07-22",
        user_id="local-user",
        briefing_date=date(2026, 7, 22),
        topic_ids=["climate-change"],
        source_ids=["ap-news"],
    )

    assert briefing.status == BriefingStatus.PENDING
    assert briefing.items == []
    assert briefing.requested_topic_ids == ["climate-change"]
