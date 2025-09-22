# Tokyo Exhibition Watcher

This is a Streamlit prototype that monitors the latest exhibition listings from [Tokyo Art Beat](https://www.tokyoartbeat.com/) for Tokyo.

## Features
- Fetch the latest event detail pages from the specified listing page.
- Detect newly added event subpages when the user presses a button.
- Persist detected events locally in `data/events.json` for future runs.

## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

The app stores fetched events in `data/events.json`. The file structure has been designed with future database migrations in mind.
