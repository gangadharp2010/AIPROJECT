# Agentic Bug Fixing

An AI-powered Python bug-fixing application that uses an agent workflow
to inspect, execute, diagnose, and attempt to repair Python functions.
The Gradio interface lets users submit code and arguments, review the
proposed fix, inspect a unified diff, and view execution results and
agent logs.

> **Security warning:** This is a development/demo application. If the
> application executes submitted or model-generated code with Python
> `exec()` in its own process, that code is not isolated. Do not expose
> it to untrusted users or use it in production without a separately
> hardened execution sandbox.

## Features

-   Agent workflow coordinated with LangGraph.
-   LLM-assisted Python code repair using LangChain and the OpenAI
    integration.
-   Python source inspection and validation using `ast`.
-   Function-name validation before loading submitted code.
-   Execution, error capture, and bounded repair attempts.
-   Unified diff between original and repaired source.
-   Gradio interface for code input, arguments, original/fixed code,
    status, and execution logs.
-   Example scenarios covering division by zero, discount calculations,
    invalid coupons, out-of-range indexes, zero quantities, `None` price
    formatting, and missing SKUs.

## Technology Stack

-   Python 3.12
-   Gradio 6
-   LangChain
-   LangChain OpenAI integration
-   LangGraph
-   OpenAI API
-   Python standard library: `ast`, `difflib`, and `html`
-   pytest
-   Docker and Docker Compose

## Project Structure

The following is a representative layout for the modular application.
Adjust it to match the files actually committed to your repository.

``` text
agentic-bug-fixing/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── bug_fixing_agent.py
│   └── services/
│       ├── code_analysis_service.py
│       ├── code_execution_service.py
│       └── code_diff_service.py
├── tests/
│   ├── test_agents.py
│   ├── test_code_analysis.py
│   ├── test_code_diff.py
│   └── test_code_execution.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

-   Python 3.12
-   OpenAI API key
-   Git
-   Docker Desktop and Docker Compose (optional, for container
    deployment)

## Installation

### 1. Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agentic-bug-fixing
```

Replace the placeholder with your GitHub repository URL.

### 2. Create a virtual environment

**Windows PowerShell**

``` powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual environment's Python
executable directly:

``` powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**macOS / Linux**

``` bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The core packages used by the application include:

``` bash
pip install gradio langchain-core langchain-openai langgraph python-dotenv pytest
```

Use the repository's `requirements.txt` as the source of truth for
dependency versions.

### 4. Configure environment variables

Create a `.env` file in the repository root. Keep this file private and
do not commit it.

``` env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
MAX_FIX_ATTEMPTS=3
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860
```

These are example settings. Confirm the variable names and defaults
against your current application configuration.

### 5. Start the application

Run from the repository root:

``` bash
python -m app.main
```

Open the local Gradio URL printed in the terminal. With the example host
and port above:

``` text
http://127.0.0.1:7860
```

## How It Works

1.  Submit a Python function and its arguments through the Gradio
    interface.
2.  Validate and inspect the source using Python AST parsing.
3.  Load the target function and execute it with the supplied arguments.
4.  Capture execution errors and diagnostic details.
5.  When appropriate, ask the configured LLM to propose a correction.
6.  Validate the proposed source before another execution attempt.
7.  Repeat within the configured repair-attempt limit.
8.  Display the result, original and repaired code, unified diff, and
    execution log.

AI-generated changes are suggestions and should be reviewed before use.
The outcome depends on the supplied code and arguments, the model
response, and API availability.

## Running Tests

Run the complete test suite from the repository root:

``` bash
python -m pytest -v
```

Run individual test modules:

``` bash
python -m pytest -v tests/test_code_analysis.py
python -m pytest -v tests/test_code_execution.py
python -m pytest -v tests/test_code_diff.py
python -m pytest -v tests/test_agents.py
```

Optional coverage report:

``` bash
pip install pytest-cov
python -m pytest --cov=app --cov-report=term-missing
```

## Docker Deployment

Build and start the application:

``` bash
docker compose up --build -d
```

Check container status:

``` bash
docker compose ps
```

View logs:

``` bash
docker compose logs -f
```

Stop the Compose application:

``` bash
docker compose down
```

### Resolve a container-name conflict

If Docker reports that `/agentic-bug-fixing` is already in use, inspect
the existing container:

``` powershell
docker ps -a --filter "name=agentic-bug-fixing"
```

If it is safe to replace that container:

``` powershell
docker rm -f agentic-bug-fixing
docker compose up --build -d
```

Avoid `docker compose down -v` or volume deletion unless you
intentionally want to remove persisted data.

## Configuration Reference

  -----------------------------------------------------------------------
  Variable                Purpose                 Example
  ----------------------- ----------------------- -----------------------
  `OPENAI_API_KEY`        Credentials for the     Set privately in `.env`
                          OpenAI integration      

  `OPENAI_MODEL`          Chat model used for     `gpt-4o-mini`
                          repair requests         

  `MAX_FIX_ATTEMPTS`      Maximum repair attempts `3`

  `GRADIO_SERVER_NAME`    Gradio bind address     `127.0.0.1`

  `GRADIO_SERVER_PORT`    Gradio listening port   `7860`
  -----------------------------------------------------------------------

The application code determines which variables are actually supported.

## Security Considerations

This project is intended for controlled development and demonstration.

-   Python `exec()` runs code with the permissions of the application
    process.
-   AST parsing and function-name validation are correctness checks, not
    a security boundary.
-   Never execute arbitrary public-user code on the host or in a normal
    application container.
-   For production, isolate each execution in a dedicated sandbox with
    strict CPU, memory, time, filesystem, and network restrictions.
-   Store API keys in environment variables or a secret manager. Never
    commit `.env` or credentials.
-   Review AI-generated code before accepting or deploying it.
-   Add authentication, authorization, rate limiting, request-size
    limits, and audit logging before exposing the interface externally.

## Troubleshooting

### `ModuleNotFoundError`

Activate the intended virtual environment and install dependencies:

``` bash
python -m pip install -r requirements.txt
```

Check the active interpreter:

``` bash
python --version
python -m pip --version
```

### Missing OpenAI API key

Check that `.env` is in the repository root and contains
`OPENAI_API_KEY`. Restart the application after changing environment
variables.

### Port 7860 is already in use

Stop the process using that port or configure another supported
`GRADIO_SERVER_PORT`.

### Docker container-name conflict

Inspect containers with `docker ps -a`. Remove or rename the conflicting
container only if it is no longer needed. See the Docker Deployment
section.

### Source contains literal `\n` characters

Serialized source may contain literal backslash-n sequences instead of
actual line breaks. Normalize the source before AST parsing and
execution. Run the test suite after changing source normalization.

## Development Guidelines

-   Run tests before committing changes.
-   Keep application logic in `app/` and tests in `tests/`.
-   Keep secrets and local environment files out of Git.
-   Review generated code and diffs rather than automatically trusting
    model output.
-   Update this README when project structure, dependencies,
    configuration, or commands change.

## Contributing

1.  Fork the repository.
2.  Create a feature branch.
3.  Implement the change and add or update tests.
4.  Run `python -m pytest -v`.
5.  Open a pull request describing the change and test results.

## License

No license has been specified here. Add a `LICENSE` file and update this
section before distributing the project publicly.
