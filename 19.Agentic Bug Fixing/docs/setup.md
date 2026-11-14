# Local setup

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
4. Start the UI: `python -m app.main`.
5. Open `http://localhost:7860`.

Run unit tests with `pytest -q`. The OpenAI integration test runs only when
`OPENAI_API_KEY` is present.
