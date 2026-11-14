# Docker and AWS deployment

## Docker

From repository root:

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY
docker compose -f deployment/compose.yaml up --build -d
docker compose -f deployment/compose.yaml logs -f
```

Open `http://localhost:7860`.

## AWS

Use GitHub Actions -> ECR -> ECS Fargate. Create the ECR repository, ECS cluster,
task execution role, task role, CloudWatch log group, Secrets Manager secret,
task definition and ECS service. Configure GitHub OIDC and repository secret
`AWS_ROLE_TO_ASSUME`. See `.github/workflows/aws-ecs-deploy.yml`.

Before deployment, update region, account ID, repository/cluster/service names,
IAM role ARNs, subnets, security groups, and secret ARN in the task definition.
Do not expose this demo publicly until code execution is moved to a hardened sandbox.
