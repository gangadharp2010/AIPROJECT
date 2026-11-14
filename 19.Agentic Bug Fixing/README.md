# Agentic Bug Fixing

An AI-assisted Python debugging application that attempts to repair a submitted Python function through a bounded agent workflow. Users provide Python source code and JSON arguments in a Gradio interface. The application validates the source, executes the function, captures failures, asks an OpenAI-backed LangChain chain for a corrected function, validates the proposed source, and retries execution through LangGraph.

The UI presents the original code, proposed fixed code, a Git-style diff, execution status, and the workflow log.

> **Important security warning:** This is a development and demonstration project. The current implementation loads and executes submitted or model-generated source using Python `exec()` inside the application process. AST parsing and function-name checks do not create a security sandbox. Do not expose this service to untrusted users or execute untrusted code on a machine containing sensitive data.

## Features

- **Agentic repair loop:** LangGraph coordinates execution, conditional routing, AI repair, and retry.
- **LLM-assisted diagnosis and repair:** LangChain Core and LangChain OpenAI connect the repair prompt to an OpenAI chat model.
- **Source validation:** Python AST parsing validates syntax and the expected top-level function.
- **Bounded retries:** Repair attempts are limited by `MAX_FIX_ATTEMPTS`.
- **Execution diagnostics:** Captures successful results and exceptions in an execution log.
- **Code comparison:** Displays a unified diff between the submitted and proposed source.
- **Gradio 6 interface:** Load sample scenarios, enter JSON arguments, run the workflow, and inspect outputs.
- **Example scenarios:** Includes representative cases such as division by zero, discounts, invalid coupons, indexing errors, zero quantities, `None` formatting, and missing SKUs.
- **Automated tests:** pytest test modules cover agent behavior, source analysis, diff generation, execution, and a small import/API smoke test.
- **Container deployment assets:** Dockerfile and Docker Compose configuration are provided under `deployment/`.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| User interface | Gradio 6 |
| Agent orchestration | LangGraph |
| LLM integration | LangChain Core, LangChain OpenAI |
| Model provider | OpenAI API |
| Source inspection | Python `ast` |
| Diff generation | Python `difflib` |
| Configuration | `python-dotenv` and environment variables |
| Validation | Pydantic |
| Testing | pytest |
| Containerization | Docker, Docker Compose |

## Project Structure

```text
19.Agentic Bug Fixing/
├── app/
│   ├── agents/
│   │   ├── bug_fixing_agent.py
│   │   ├── graph.py
│   │   ├── prompts.py
│   │   └── state.py
│   ├── config/
│   │   └── settings.py
│   ├── examples/
│   │   └── bug_examples.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── code_analysis_service.py
│   │   ├── code_diff_service.py
│   │   ├── code_execution_service.py
│   │   └── openai_service.py
│   ├── ui/
│   │   ├── components.py
│   │   ├── gradio_app.py
│   │   └── styles.py
│   └── main.py
├── deployment/
│   ├── Dockerfile
│   └── compose.yaml
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── setup.md
│   └── troubleshooting.md
├── scripts/
│   ├── build.sh
│   └── deploy.sh
├── tests/
│   ├── test_agents.py
│   ├── test_api.py
│   ├── test_code_analysis.py
│   ├── test_code_diff.py
│   └── test_code_execution.py
├── requirements.txt
├── .gitignore
└── README.md
```

Some directories also contain package initializer files and supporting assets that are not expanded above.

## Prerequisites

- Python **3.12**
- An OpenAI API key with access to the configured model
- Git
- Docker Desktop and Docker Compose (optional)

## Local Setup

### 1. Clone the repository and enter the project directory

```bash
git clone https://github.com/gangadharp2010/AIPROJECT.git
cd AIPROJECT
cd "19.Agentic Bug Fixing"
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, call the environment's interpreter directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project directory. Do not commit this file or share the API key.

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
MAX_FIX_ATTEMPTS=3
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860
LOG_LEVEL=INFO
```

The settings module currently defines these defaults:

| Variable | Purpose | Default |
|---|---|---|
| `OPENAI_API_KEY` | Authentication for the OpenAI integration | Empty; provide your key |
| `OPENAI_MODEL` | Chat model used by the repair chain | `gpt-4o-mini` |
| `MAX_FIX_ATTEMPTS` | Maximum AI repair cycles | `3` |
| `GRADIO_SERVER_NAME` | Gradio bind address | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | Gradio port | `7860` |
| `LOG_LEVEL` | Application log-level setting | `INFO` |

For a local-only development run, `GRADIO_SERVER_NAME=127.0.0.1` is a safer bind address. The container configuration overrides it to `0.0.0.0` so the port can be published.

### 5. Run the application

From the `19.Agentic Bug Fixing` directory:

```bash
python -m app.main
```

Open:

```text
http://127.0.0.1:7860
```

The application initializes the agent when a repair is first requested. A valid `OPENAI_API_KEY` is therefore needed for LLM-backed repair.

## How the Workflow Works

```text
User submits Python function + JSON arguments
                    |
                    v
             Gradio interface
                    |
                    v
         Validate source with Python AST
                    |
                    v
          Execute submitted function
                    |
             +------+------+
             |             |
          Success        Failure
             |             |
             v             v
       Show result     Check retry limit
                           |
                    +------+------+
                    |             |
                 Reached       Attempts left
                    |             |
                    v             v
                Stop run     LLM repair prompt
                                  |
                                  v
                         Validate proposed source
                                  |
                                  v
                           Execute again
                                  |
                                  v
                        Return code, diff,
                       status, and logs
```

### Workflow stages

1. **Input:** The UI accepts one Python function and arguments encoded as JSON.
2. **Validation:** The source validation service parses the code and checks the expected function.
3. **Execution:** The execution service loads the function and runs it with the supplied arguments.
4. **Diagnosis:** Exceptions and diagnostic messages are captured in the workflow state.
5. **Repair:** The LangGraph workflow routes failures to the repair node, which invokes the configured LLM chain.
6. **Candidate validation:** The proposed code is checked before the next execution cycle.
7. **Retry:** The graph executes the candidate again until it succeeds or reaches the configured attempt limit.
8. **Presentation:** The UI displays the original and proposed code, diff, execution status, and logs.

The LLM output is a proposed code change, not a guarantee of correctness. Review all changes and test relevant edge cases before using repaired code elsewhere.

## Running Tests

Run from the project directory with the virtual environment activated:

```bash
python -m pytest -v
```

Run individual test modules:

```bash
python -m pytest -v tests/test_code_analysis.py
python -m pytest -v tests/test_code_execution.py
python -m pytest -v tests/test_code_diff.py
python -m pytest -v tests/test_agents.py
python -m pytest -v tests/test_api.py
```

The tests should be run locally after dependency installation. LLM-backed paths may require a valid API key, depending on the test being executed. This README does not claim a test result for every environment.

## Docker Deployment

The Dockerfile and Compose file are in the `deployment/` folder. Run the Compose commands from the project directory:

```bash
docker compose -f deployment/compose.yaml up --build -d
```

Check the container:

```bash
docker compose -f deployment/compose.yaml ps
```

View logs:

```bash
docker compose -f deployment/compose.yaml logs -f
```

Stop the service:

```bash
docker compose -f deployment/compose.yaml down
```

The Compose configuration expects a `.env` file at the project root and publishes port `7860`. Ensure the `.env` file contains a valid `OPENAI_API_KEY`.

## Troubleshooting

### `ModuleNotFoundError`

Confirm that the intended Python 3.12 virtual environment is active, then reinstall the project dependencies:

```bash
python --version
python -m pip --version
python -m pip install -r requirements.txt
```

### OpenAI authentication or model errors

Check the `OPENAI_API_KEY` value, confirm the key is active, and verify that the configured model is available to your account. Restart the application after changing `.env`.

### Port 7860 is already in use

Stop the process using port 7860 or configure a different `GRADIO_SERVER_PORT`. When using Docker, update the published host port in the Compose configuration as well.

### Docker container name already exists

Inspect the container:

```bash
docker ps -a --filter "name=agentic-bug-fixing"
```

Stop or remove the existing container only when you are certain it is no longer needed, then rerun Compose. Avoid deleting volumes unless you intentionally want to remove persisted data.

### Python source contains literal newline escapes

When code arrives as serialized text, it may contain literal `\\n` sequences instead of line breaks. Check the normalized source passed to AST parsing and rerun the source-analysis tests after changing normalization logic.

## Security and Responsible Use

This application is a learning/demo tool, not a secure public code-execution service.

- Python `exec()` executes code with the permissions of the application process.
- AST parsing, syntax checks, and function-name validation are not a sandbox.
- A normal Docker container alone should not be treated as a sufficient boundary for arbitrary hostile code.
- Before any public or production deployment, move execution into a dedicated isolation service with strict CPU, memory, time, process, filesystem, and network controls.
- Run workloads with least privilege and no access to application secrets.
- Apply authentication, authorization, request-size limits, rate limiting, audit logging, and resource quotas.
- Never put API keys in source control, container images, logs, or client-side code.
- Review generated changes and run unit, integration, and regression tests before accepting a repair.

## Development Guidelines

- Keep agent orchestration in `app/agents/`.
- Keep source analysis, execution, model integration, and diff logic in `app/services/`.
- Keep UI code in `app/ui/`.
- Add regression tests whenever a bug scenario or repair behavior changes.
- Run `python -m pytest -v` before committing.
- Update documentation when configuration, project structure, or deployment commands change.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make a focused change and add regression tests.
4. Run the relevant tests and the full test suite.
5. Open a pull request with a concise description and test output.

## License

Refer to the `LICENSE` file included in this project directory.
