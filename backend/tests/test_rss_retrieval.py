import httpx

from backend.models import NewsSource, RetrievalMethod
from backend.retrieval.rss import RSSRetriever

SAMPLE_RSS = """
<rss version="2.0">
  <channel>
    <title>Test News</title>
    <item>
      <title>Climate research reaches a new milestone</title>
      <link>https://example.com/climate-milestone</link>
      <description><![CDATA[<p>A test article summary.</p>]]></description>
      <pubDate>Wed, 22 Jul 2026 12:00:00 GMT</pubDate>
      <author>Test Reporter</author>
    </item>
  </channel>
</rss>
"""


def test_retrieve_articles_from_rss() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            content=SAMPLE_RSS.encode(),
            headers={"Content-Type": "application/rss+xml"},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))

    source = NewsSource(
        id="test-news",
        name="Test News",
        domains=["example.com"],
        retrieval_method=RetrievalMethod.RSS,
        feed_urls=["https://example.com/rss.xml"],
    )

    articles = RSSRetriever(client=client).retrieve(source)

    assert len(articles) == 1
    assert articles[0].source_id == "test-news"
    assert articles[0].title == "Climate research reaches a new milestone"
    assert articles[0].description == "A test article summary."
    assert articles[0].published_at is not None


def test_reject_non_rss_source() -> None:
    source = NewsSource(
        id="test-news",
        name="Test News",
        domains=["example.com"],
        retrieval_method=RetrievalMethod.SEARCH,
    )

    retriever = RSSRetriever()

    try:
        retriever.retrieve(source)
    except ValueError as error:
        assert "not configured for RSS" in str(error)
    else:
        raise AssertionError("Expected ValueError")