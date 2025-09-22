"""Utilities for fetching and parsing event information from Tokyo Art Beat."""
from __future__ import annotations

from html.parser import HTMLParser
from typing import List, Set
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from .models import EventLink

BASE_URL = "https://www.tokyoartbeat.com/events/regionId/3t69ZtVfJeKUQ2UM0DXnJM/orderBy/latest"
USER_AGENT = "Mozilla/5.0 (compatible; ExhibitionTracker/0.1; +https://example.com)"


class EventListParser(HTMLParser):
    """Parses anchor tags that link to individual event pages."""

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self._collecting = False
        self._current_href: str | None = None
        self._current_label: str | None = None
        self._text_fragments: List[str] = []
        self.links: List[EventLink] = []
        self._seen: Set[str] = set()

    def handle_starttag(self, tag: str, attrs):
        if tag != "a":
            return
        attr_map = dict(attrs)
        href = attr_map.get("href")
        if not href or not self._looks_like_event_link(href):
            return
        absolute_href = urljoin(self.base_url, href)
        if absolute_href in self._seen:
            return
        self._collecting = True
        self._current_href = absolute_href
        self._current_label = attr_map.get("aria-label") or attr_map.get("title")
        self._text_fragments = []

    def handle_endtag(self, tag: str):
        if tag != "a" or not self._collecting:
            return
        text = " ".join(fragment.strip() for fragment in self._text_fragments if fragment.strip())
        title = self._current_label or text
        if title and self._current_href:
            title = " ".join(title.split())
            self.links.append(EventLink(title=title, url=self._current_href))
            self._seen.add(self._current_href)
        self._reset_state()

    def handle_data(self, data: str):
        if self._collecting and data:
            self._text_fragments.append(data)

    def _reset_state(self) -> None:
        self._collecting = False
        self._current_href = None
        self._current_label = None
        self._text_fragments = []

    def _looks_like_event_link(self, href: str) -> bool:
        parsed = urlparse(urljoin(self.base_url, href))
        if parsed.scheme not in {"http", "https"}:
            return False
        segments = [segment for segment in parsed.path.split("/") if segment]
        if not segments or segments[0] != "events":
            return False
        if len(segments) < 2:
            return False
        if any(segment.startswith("regionId") or segment.startswith("orderBy") for segment in segments):
            return False
        if parsed.query:
            return False
        return True


def fetch_event_links(base_url: str = BASE_URL, timeout: int = 30) -> List[EventLink]:
    """Fetch the current list of event links from the website."""

    request = Request(base_url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # type: ignore[call-arg]
        encoding = response.headers.get_content_charset("utf-8")
        html = response.read().decode(encoding, errors="ignore")
    parser = EventListParser(base_url)
    parser.feed(html)
    return parser.links
