# Agent Notes

## Technology Choices
- Streamlit powers the interactive UI in `app.py`.
- Pydantic v2 provides typed models within `event_tracker.models` and related modules.
- Standard library modules handle networking (`urllib`), parsing, and persistence (JSON + filesystem).

## Directory Structure
- `app.py`: Streamlit entry point for the prototype UI.
- `event_tracker/`: Python package with fetcher, models, and storage logic.
- `data/`: Local persistence location (JSON files).
- `README.md`: Project overview and usage notes.
- `requirements.txt`: Python dependencies for the application.

## Development Notes
- When adding or updating models under `event_tracker/`, prefer Pydantic v2 `BaseModel` classes.
- Keep the repository ready for a future database-backed storage layer; avoid tight coupling between storage and UI concerns.
