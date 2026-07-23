import pytest

from backend.models import (
    NewsSource,
    NewsTopic,
    RetrievalMethod,
)
from backend.retrieval.query_builder import build_search_query


def test_build_search_query() -> None:
    topic = NewsTopic(
        id="climate-change",
        name="Climate Change",
        query='"climate change" OR "climate policy"',
        exclude_terms=["celebrity"],
    )

    source = NewsSource(
        id="ap-news",
        name="Associated Press",
        domains=["apnews.com"],
        retrieval_method=RetrievalMethod.SEARCH,
    )

    query = build_search_query(topic, source)

    assert "site:apnews.com" in query
    assert '"climate change"' in query
    assert '-"celebrity"' in query


def test_reject_disabled_source() -> None:
    topic = NewsTopic(
        id="climate-change",
        name="Climate Change",
        query='"climate change"',
    )

    source = NewsSource(
        id="ap-news",
        name="Associated Press",
        domains=["apnews.com"],
        retrieval_method=RetrievalMethod.SEARCH,
        enabled=False,
    )

    with pytest.raises(ValueError, match="not enabled"):
        build_search_query(topic, source)