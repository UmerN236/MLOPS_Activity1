#!/usr/bin/env sh
set -eu

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <ghcr-image> <version>" >&2
  echo "Example: $0 ghcr.io/username/mlops_activity1 1.0.0" >&2
  exit 2
fi

image="$1"
version="$2"

docker pull "$image:$version"
docker stop mlops-api || true
docker rm mlops-api || true
docker run -d \
  --name mlops-api \
  --restart unless-stopped \
  -p 5000:5000 \
  "$image:$version"

curl --fail --show-error \
  --retry 10 --retry-delay 3 --retry-all-errors \
  http://localhost:5000/health
