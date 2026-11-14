# AWS deployment

See the root `docs/deployment.md` and `.github/workflows/aws-ecs-deploy.yml`.

Target architecture: GitHub Actions (OIDC) -> Amazon ECR -> Amazon ECS Fargate.
The task listens on container port 7860. Store `OPENAI_API_KEY` in AWS Secrets Manager
and inject it through the ECS task definition; never bake secrets into the image.

Security: the current demo runs submitted code in-process with `exec()`. Do not expose
it to untrusted users. A dedicated hardened execution sandbox is required before
public deployment.
