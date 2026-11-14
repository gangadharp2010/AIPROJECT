# Architecture

```text
Browser -> Gradio UI -> BugFixingAgent -> LangGraph
                                  |          |
                                  |       Execute node
                                  |          |
                                  |       Error router
                                  |          |
                                  |       OpenAI fix node
                                  |          |
                                  +------ re-execute
                                  |
                         Diff service -> Gradio outputs
```

- `ui`: Gradio presentation and event handlers.
- `agents`: LangGraph state, prompts, graph and agent facade.
- `services`: code validation/loading, execution, diff generation and model factory.
- `config`: environment-based settings.
- `examples`: sample functions for the UI.
- `tests`: unit tests and opt-in LLM integration test.

The current executor uses `exec()` for demonstration only. It is not a sandbox.
