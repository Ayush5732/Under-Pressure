# Deployment preparation

The application runs as one Python service with a shared SQLite database. Run one instance only. The live subscription uses this process's room-change notifications.

The Dockerfile reads PORT, supports Render's RENDER_EXTERNAL_URL for canonical HTTPS invitations and origin validation, and stores saves under STATE_DIRECTORY (default /data in Docker). Mount persistent storage at /data before creating real rooms. Container-local storage without a persistent mount does not preserve saves across replacement.

Render configuration: Docker runtime; health check /health; one instance; persistent disk mounted at /data. A persistent disk requires an appropriate paid service. Choose and approve that plan before provisioning; no billing or hosting resource has been created by preparing these files.

No credentials, existing rooms or chat saves belong in the Git repository. Existing saves may be migrated separately by the owner. Protect original saves until the hosted deployment and room tests pass.
