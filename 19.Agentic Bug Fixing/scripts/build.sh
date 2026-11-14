#!/usr/bin/env bash
set -euo pipefail
docker build -f deployment/Dockerfile -t agentic-bug-fixing:local .
