# Deployment notes

- Use `DATABASE_URL` to configure the database; SQLite is the default for coursework/local deployment.
- Mount `/data` as a persistent Docker volume when using the provided Dockerfile.
- Never commit `.env`, credentials, tokens, or production database files.
- The container runs as an unprivileged user and includes a `/health` health check.
- For production deployment, use a managed database, HTTPS termination, restricted network access, and managed secrets.
