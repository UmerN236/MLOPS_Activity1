# MLOps Continuous Delivery Demo

A small Flask inference API delivered using:

- GitHub Actions
- Docker
- GitHub Container Registry
- Automatic staging deployment
- Staging smoke tests
- Manual production approval
- Versioned rollback

## Delivery pipeline

Pull Request -> CI -> Version Tag -> Docker Image -> GHCR -> Staging -> Health Test -> Approval -> Production