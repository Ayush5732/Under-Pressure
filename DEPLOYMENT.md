# Free Render deployment

Use a free Python web service, one instance, with build command `pip install -r requirements.txt` and start command `python server.py --no-browser --host 0.0.0.0`. PORT and RENDER_EXTERNAL_URL are supplied by Render. Health endpoint: /health.

Set DATABASE_URL to the internal connection URL of a free Render Postgres database in the same workspace and region. Never put this value in Git. Saved rooms use Postgres when configured, and local SQLite remains available for development.

Free Render Postgres expires after 30 days under the current free-tier terms; it is suitable for temporary testing, not permanent free storage. Free web services can sleep when inactive. No paid service, disk or automatic upgrade is authorized.
