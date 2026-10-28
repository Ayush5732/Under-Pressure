# Free Render deployment

Live game: https://under-pressure-game.onrender.com

One free Python web service in My Workspace, Virginia. Build: `pip install -r requirements.txt`. Start: `python server.py --no-browser --host 0.0.0.0`. Render supplies PORT and RENDER_EXTERNAL_URL. Health endpoint: `/health`.

Set STATE_DIRECTORY to `/tmp/under-pressure`. Do not configure DATABASE_URL or attach a persistent disk. Rooms use temporary SQLite files only to synchronize a round between Alex and the mentor. No permanent user records, external database, or paid resource is provisioned.

A service restart, redeploy, or idle spin-down erases rooms. Free services spin down after 15 minutes without incoming traffic and take about a minute to wake. Active clients send live update requests during play. No uninterrupted-round guarantee is possible on the free service.

Automatic deployment is disabled to avoid interrupting rounds when the repository changes. Deploy deliberately when no rounds need preserving. PostgreSQL support in server.py is optional and unused by this deployment. No paid upgrade is authorized.
