"""
Class to define the different news topics, ie Politics or Climate Change
"""

from pydantic import BaseModel, ConfigDict, Field


class NewsTopic(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9_-]*$")
    name: str = Field(min_length=1, max_length=100)
    query: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=500)

    include_domains: list[str] = Field(default_factory=list)
    exclude_terms: list[str] = Field(default_factory=list)

    weight: float = Field(default=1.0, ge=0.0, le=10.0)
    minimum_articles: int = Field(default=0, ge=0, le=20)
    maximum_articles: int = Field(default=5, ge=1, le=50)
    enabled: bool = True


"""
Example implementation:: 

from backend.models.topic import NewsTopic


climate_topic = NewsTopic(
    id="climate-change",
    name="Climate Change",
    query='"climate change" OR "global warming" OR "climate policy"',
    description="Climate science, policy, mitigation, and adaptation.",
    include_domains=["apnews.com"],
    exclude_terms=["celebrity"],
    weight=1.0,
    maximum_articles=4,
)
"""
