from typing import Any, cast

import httpx
from pydantic import BaseModel, ConfigDict, Field

from atlas.config import settings
from atlas.tools.base import Tool


class GNewsInput(BaseModel):
    model_config = ConfigDict(strict=True, str_strip_whitespace=True)
    topic: str = Field(min_length=1)
    count: int = Field(default=5, le=10, ge=1)


class Article(BaseModel):
    title: str
    url: str
    source: str
    published: str
    description: str | None


def parse_articles(data: dict[str, Any]) -> list[Article]:
    """Convert a GNews search response into Article objects.

    :param data: the decoded JSON body of a GNews search response.
    :return: one Article object per item in the response's articles list,
            empty when the key is absent or the list is empty.
    """
    articles = data.get("articles", [])
    result: list[Article] = []

    for article in articles:
        parsed = Article(
            title=article["title"],
            url=article["url"],
            source=article["source"]["name"],
            published=article["publishedAt"],
            description=article.get("description"),
        )
        result.append(parsed)

    return result


def format_articles(articles: list[Article]) -> str:
    """Render parsed articles as numbered display text.

    :param articles: parsed articles, in the order returned by the provider.
    :return: one numbered block per article (title, source and timestamp,
        description when present, URL), or a no-results message when the
        list is empty.
    """
    if not articles:
        return "No news found for that topic."

    blocks: list[str] = []

    for index, article in enumerate(articles, start=1):
        lines = [
            f"{index}. {article.title}",
            f"   {article.source}, {article.published}",
        ]
        if article.description:
            lines.append(f"   {article.description}")
        lines.append(f"   {article.url}")
        blocks.append("\n".join(lines))

    return "\n\n".join(blocks)


class GNewsTool(Tool):
    @property
    def name(self) -> str:
        return "gnews"

    @property
    def description(self) -> str:
        return "Provides News headlines and titles using G-News API"

    @property
    def sensitivity(self) -> str:
        return "none"

    @property
    def input_model(self) -> type[BaseModel]:
        return GNewsInput

    def _execute(self, validated_input: BaseModel) -> str:
        """Fetch news headlines for the validated topic.

        Returns a disabled message when ``NEWS_API_KEY`` is not configured,
        per D30: credentials are enforced at the tool boundary rather than
        at construction or registration.

        :param validated_input: a :class:`GNewsInput` already validated by
        :meth:`Tool.run`; cast is safe because ``run`` builds it from
        ``input_model``.
        :return: formatted headline text, or the disabled message.
        """
        key = settings.news_api_key
        if not key:
            return "News disabled: set NEWS_API_KEY in .env"

        url = "https://gnews.io/api/v4/search"

        gnews_input = cast(GNewsInput, validated_input)

        params: dict[str, str | int] = {
            "q": gnews_input.topic,
            "max": gnews_input.count,
            "apikey": key,
            "lang": "en",
        }

        response = httpx.get(url, params=params)
        result = response.json()
        return format_articles(parse_articles(result))
