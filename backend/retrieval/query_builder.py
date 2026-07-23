from backend.models import NewsSource, NewsTopic


def build_search_query(topic: NewsTopic, source: NewsSource) -> str:
    if not topic.enabled:
        raise ValueError(f"Topic {topic.id} is disabled")

    if not source.enabled:
        raise ValueError(f"Source {source.id} not enabled")

    domain_query = " OR ".join(
        f"site:{domain}" for domain in source.domains
    )

    exclusions = " ".join(
        f'-"{term}"' for term in topic.exclude_terms
    )

    parts = [
        f"({domain_query})",
        f"({topic.query})",
        exclusions
    ]

    #very chupid line of code lmao
    return " ".join(part for part in parts if part).strip()