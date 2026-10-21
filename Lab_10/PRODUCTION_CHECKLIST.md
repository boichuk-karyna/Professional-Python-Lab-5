# Production checklist — Variant 2

- [x] src-layout and package metadata
- [x] wheel/sdist build configuration
- [x] environment-based configuration
- [x] `.env.example`; `.env` excluded from Git
- [x] no real credentials in source files
- [x] Dockerfile and `.dockerignore`
- [x] non-root Docker user and health check
- [x] persistent SQLite volume documented
- [x] `/health` endpoint
- [x] REST API for books and authors
- [x] tests for core features and invalid input
- [x] GitHub Actions lint, format, mypy, tests, build and Docker build
- [x] README and report template

Before submission on your machine:
- [ ] Run tests and quality checks locally and fix any environment-specific failures
- [ ] Run `python -m build` and show wheel/sdist files
- [ ] Install wheel into a fresh virtual environment
- [ ] Build and run Docker image; verify `/health` and `/docs`
- [ ] Push to GitHub and show a green Actions run
- [ ] Add screenshots and actual command outputs to the report
- [ ] Check Git history for accidental secrets
