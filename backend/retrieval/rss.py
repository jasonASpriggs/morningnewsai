import hashlib
import re
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import feedparser
import httpx

from backend.models import Article, NewsSource, RetrievalMethod


def create_article_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def remove_html(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value).strip()


def parse_published_at(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        published_at = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None

    if published_at.tzinfo is None:
        published_at = published_at.replace(tzinfo=UTC)

    return published_at.astimezone(UTC)


class RSSRetriever:
    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(
            timeout=15.0,
            follow_redirects=True,
            headers={"User-Agent": "MorningNewsAI/0.1"},
        )

    def retrieve(self, source: NewsSource) -> list[NewsSource]:
        if source.retrieval_method != RetrievalMethod.RSS:
            raise ValueError(f"Source {source.id} is not configured for RSS.")

        articles: list[Article] = []

        for feed_url in source.feed_urls:
            response = self.client.get(str(feed_url))
            response.raise_for_status()

            parsed_feed = feedparser.parse(response.content)

            if parsed_feed.bozo and not parsed_feed.entries:
                raise ValueError(f"Unable to parse RSS feed: {feed_url}")

            for entry in parsed_feed.entries:
                url = entry.get("link")
                title = entry.get("title")

                if not url or not title:
                    continue

                description = remove_html(
                    entry.get("summary") or entry.get("description") or ""
                )

                articles.append(
                    Article(
                        id=create_article_id(url),
                        title=remove_html(title),
                        source_id=source.id,
                        source_name=source.name,
                        url=url,
                        canonical_url=url,
                        published_at=parse_published_at(
                            entry.get("published") or entry.get("updated")
                        ),
                        author=entry.get("author"),
                        description=description or None,
                    )
                )

        return articles