# MLOps Continuous Delivery Demo

A small Flask inference API delivered as one immutable Docker artifact through
staging and production.

- GitHub Actions
- Docker
- GitHub Container Registry
- Automatic staging deployment
- Staging smoke tests
- Manual production approval
- Versioned rollback

## Delivery pipeline

Pull Request -> CI -> Version Tag -> Docker Image -> GHCR -> Staging -> Health Test -> Approval -> Production

Normal pushes and pull requests run Continuous Integration. A semantic version
tag such as `v1.0.0` starts Continuous Delivery. The workflow builds the image
once, tests it in staging, and promotes the same versioned image to production.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

The service listens on port 5000:

```bash
curl http://localhost:5000/health
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"value": 5}'
```

## Run with Docker

```bash
docker build -t mlops-cd-demo:local .
docker run --rm -p 5052:5000 mlops-cd-demo:local
```

Alternatively:

```bash
docker compose up -d --build
curl --fail http://localhost:5052/health
docker compose down
```

## GitHub environments

Create `staging` and `production` under **Settings -> Environments**. Configure
the production environment with a required reviewer.

Add these secrets to `staging`:

- `STAGING_HOST`
- `STAGING_USER`
- `STAGING_SSH_KEY`

Add these secrets to `production`:

- `PRODUCTION_HOST`
- `PRODUCTION_USER`
- `PRODUCTION_SSH_KEY`

Both hosts must run Docker, accept SSH connections from GitHub-hosted runners,
and expose port 5000 for the health check.

## Release

The value in `VERSION` must match the tag without its leading `v`:

```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

The workflow publishes:

- `ghcr.io/umern236/mlops_activity1:1.0.0`
- `ghcr.io/umern236/mlops_activity1:latest`

Use explicit versions for deployment and rollback. `latest` is only a
convenience tag.

## Rollback

On the target server, authenticate to GHCR if the package is private and run:

```bash
./scripts/rollback.sh ghcr.io/umern236/mlops_activity1 1.0.0
```

This replaces `mlops-api` with the selected known-good immutable image and
verifies the health endpoint.
