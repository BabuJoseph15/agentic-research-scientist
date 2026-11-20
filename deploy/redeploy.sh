#!/bin/bash

set -e

echo "Stopping container..."

docker stop agentic-research-scientist || true

docker rm agentic-research-scientist || true

echo "Logging into ECR..."

aws ecr get-login-password \
--region ap-southeast-2 | docker login \
--username AWS \
--password-stdin \
774055931904.dkr.ecr.ap-southeast-2.amazonaws.com

echo "Pulling latest image..."

docker pull \
774055931904.dkr.ecr.ap-southeast-2.amazonaws.com/agentic-research-scientist:latest

echo "Starting container..."

docker run -d \
  --name agentic-research-scientist \
  --restart unless-stopped \
  -p 8501:8501 \
  --env-file /home/ubuntu/.env \
  -v /opt/ars/reports:/app/reports \
  -v /opt/ars/chroma:/app/memory/chroma_db \
  -v /opt/ars/history:/app/reports/history \
  774055931904.dkr.ecr.ap-southeast-2.amazonaws.com/agentic-research-scientist:latest

echo "Deployment completed successfully."
