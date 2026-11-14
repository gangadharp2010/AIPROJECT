#!/usr/bin/env bash
set -euo pipefail
# Deployment is performed by GitHub Actions. This script is a reminder entry point.
echo "Push to main to trigger .github/workflows/aws-ecs-deploy.yml"
