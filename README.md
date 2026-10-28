# Under Pressure

An authored two-player project-management simulation. Alex manages delivery while a live mentor receives role-specific project reports and provides guidance through a persistent conversation panel.

## Online play

Open the deployed website, create a project and share its room code and game address. The mentor chooses Join as mentor. Reports, conversations and interventions synchronize live. Keep your private role link to return to the same room.

## Deployment

Run the Dockerfile as one web-service instance with persistent storage mounted at `/data`. The server reads `PORT`, `STATE_DIRECTORY`, and `PUBLIC_ORIGIN` or Render’s automatic `RENDER_EXTERNAL_URL`. Health endpoint: `/health`. See DEPLOYMENT.md for configuration and storage requirements.

## Local development

Python 3.9+; no application dependencies are required. Run `python3 server.py --host 127.0.0.1`. Use `--db /path/to/save.sqlite3` for a chosen local database. Never commit saves, credentials or participant conversations.

## Verification

`python3 -m unittest test_reports test_multiplayer` exercises reporting and live room permissions. `node test_ui.js` checks UI wiring with a DOM shim. Browser layout and assessment calibration still require playtesting. The rules are provisional, not validated hiring measures.
