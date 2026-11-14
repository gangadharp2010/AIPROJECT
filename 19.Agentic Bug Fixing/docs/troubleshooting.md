# Troubleshooting

- `OPENAI_API_KEY is missing`: check `.env` locally or ECS Secrets Manager injection.
- Browser cannot connect: confirm Gradio binds `0.0.0.0`, container port 7860 is mapped,
  and the container is healthy.
- ECS task stops: inspect ECS stopped reason and CloudWatch `/ecs/agentic-bug-fixing`.
- OpenAI request fails: verify API key, model access, outbound network, and account quota.
- JSON argument error: provide a JSON array such as `[10, 0]`.
