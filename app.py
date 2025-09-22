"""Streamlit prototype for monitoring new Tokyo Art Beat exhibitions."""
from __future__ import annotations

from datetime import datetime
from typing import List

import streamlit as st

from event_tracker.fetcher import BASE_URL, fetch_event_links
from event_tracker.models import StoredEvent
from event_tracker.storage import EventRepository

st.set_page_config(page_title="Tokyo Exhibition Watcher", layout="wide")


def render_event_list(title: str, events: List[StoredEvent]) -> None:
    st.subheader(title)
    if not events:
        st.info("表示できるイベントがありません。")
        return
    for event in events:
        st.markdown(
            f"- [{event.title}]({event.url})\\n  - 初回検知: {format_timestamp(event.first_seen_at)}"
        )


def format_timestamp(timestamp: str) -> str:
    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError:
        return timestamp
    return parsed.astimezone().strftime("%Y-%m-%d %H:%M (%Z)")


def render_new_events(events: List[StoredEvent]) -> None:
    if not events:
        st.success("新しいイベントはありませんでした。")
        return
    st.success(f"{len(events)} 件の新しいイベントを検出しました。")
    for event in events:
        st.markdown(f"- [{event.title}]({event.url})")


def main() -> None:
    st.title("東京の展覧会更新チェッカー")
    st.caption(
        "指定ページに新規で追加された展覧会のサブページを検知して記録します。"
    )

    repository = EventRepository()
    snapshot = repository.load()

    with st.expander("保存済みのイベント一覧", expanded=False):
        render_event_list("保存済みイベント", snapshot.events[:20])
        if len(snapshot.events) > 20:
            st.caption("※ 最新20件のみ表示しています。")

    if st.button("最新の一覧を取得", type="primary"):
        with st.spinner("ページを解析中です..."):
            try:
                links = fetch_event_links(BASE_URL)
            except Exception as exc:  # noqa: BLE001
                st.error(f"取得中にエラーが発生しました: {exc}")
            else:
                new_events = repository.add_new_events(links)
                render_new_events(new_events)
    else:
        if snapshot.last_updated_at:
            st.caption(f"最終更新: {format_timestamp(snapshot.last_updated_at)}")


if __name__ == "__main__":
    main()
