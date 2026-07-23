"""
Tests to ensure that the ./config/ folder .yaml files are loaded 
correctly by ./backend/config_loader.py
"""

from backend.config_loader import load_sources, load_topics
from backend.models import RetrievalMethod


def test_load_three_sources() -> None:
    sources = load_sources()

    assert len(sources) == 3
    assert all(source.enabled for source in sources)
    assert all(source.retrieval_method == RetrievalMethod.SEARCH for source in sources)


def test_source_ids_are_unique() -> None:
    sources = load_sources()
    source_ids = [source.id for source in sources]

    assert len(source_ids) == len(set(source_ids))


def test_load_three_topics() -> None:
    topics = load_topics()

    assert len(topics) == 3
    assert all(topic.enabled for topic in topics)
    assert all(topic.query for topic in topics)


def test_topic_ids_are_unique() -> None:
    topics = load_topics()
    topic_ids = [topic.id for topic in topics]

    assert len(topic_ids) == len(set(topic_ids))
