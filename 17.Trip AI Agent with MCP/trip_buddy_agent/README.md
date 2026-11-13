# Trip Buddy AI – Intelligent Travel Planning Assistant

An AI-powered travel planning application built with Python, Gradio, Model Context Protocol (MCP), Retrieval-Augmented Generation (RAG), and SQLite.

Trip Buddy helps users explore destinations, estimate trip costs, compare destinations against budgets, and retrieve travel-related knowledge through an AI-powered conversational interface.

---

## 1. Project Features

- **AI Travel Assistant:** Conversational travel planning.
- **MCP Integration:** Travel and knowledge tools exposed through MCP servers.
- **RAG:** Retrieve relevant information from travel knowledge documents.
- **Conversation Memory:** Store conversation history and extracted trip preferences using SQLite.
- **Budget Estimation:** Estimate trip expenses based on destination, group size, and number of nights.
- **Destination Comparison:** Find destinations matching a specified budget.
- **Response Formatting:** Present travel recommendations, budgets, and itineraries in readable Markdown.
- **Gradio UI:** Interactive web-based chat interface.

---

## 2. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.12 |
| Frontend | Gradio |
| AI / LLM | OpenAI (optional, depending on configuration) |
| Agent Framework | Custom Python travel agent |
| Agent Communication | Model Context Protocol (MCP) |
| MCP SDK | Python MCP SDK 1.x |
| Knowledge Retrieval | RAG |
| Database | SQLite |
| Deployment (planned) | Docker and AWS ECS Fargate |

---

## 3. Project Structure

```text
trip_buddy_agent/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── agents/
│   ├── travel_agent.py
│   ├── conversation_memory.py
│   └── response_formatter.py
│
├── database/
│   └── db_connection.py
│
├── tools/
│   └── travel_tools.py
│
├── rag/
│   └── retriever.py
│
├── mcp_client/
│   └── client.py
│
├── mcp_servers/
│   ├── travel_mcp_server.py
│   └── knowledge_mcp_server.py
│
└── knowledge/
    └── travel knowledge documents
```

*The exact knowledge directory and its files depend on your RAG implementation.*

---

## 4. Prerequisites

Install the following software before starting:

1. Python 3.12
2. Visual Studio Code
3. Git
4. Internet connection
5. OpenAI API key, if using the OpenAI-powered agent
6. Docker Desktop (only needed for the later Docker deployment steps)

Verify Python:

```powershell
python --version
```

Expected:

```text
Python 3.12.x
```

Verify Git:

```powershell
git --version
```

---

## 5. Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project:

```powershell
cd trip_buddy_agent
```

If you already have the project locally, navigate to its existing directory instead.

---

## 6. Create a Python Virtual Environment

Create a project-specific virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Verify the Python interpreter:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

The interpreter should point to:

```text
trip_buddy_agent\.venv\Scripts\python.exe
```

**Important:** Always activate this project's `.venv` before installing packages or running the application.

---

## 7. Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Make sure the MCP SDK is pinned to version 1.x in `requirements.txt`:

```text
mcp[cli]>=1.28,<2
```

If the MCP package is missing, install it:

```powershell
python -m pip install "mcp[cli]>=1.28,<2"
```

Verify installation:

```powershell
python -c "import mcp; print('MCP SDK installed successfully')"
```

Check the installed MCP version:

```powershell
python -m pip show mcp
```

The project currently uses the MCP SDK 1.x API:

```python
from mcp.server.fastmcp import FastMCP
```

---

## 8. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
```

Add other environment variables required by your implementation to this file.

If the application supports running without OpenAI, configure the key only when using that integration.

Create `.env.example` for repository users:

```env
OPENAI_API_KEY=
```

**Security:** Never commit `.env` or API keys to GitHub.

---

## 9. Initialize the Database

The application uses SQLite for destination data and conversation memory.

Check the database initialization code in:

```text
database/db_connection.py
```

The application should initialize its database tables before serving requests.

If your application has a separate initialization function, run it using the project's actual function and module names.

The database files should be generated locally and should not be committed to Git.

---

## 10. Run MCP Servers

Trip Buddy uses two MCP servers.

### 10.1 Travel MCP Server

File:

```text
mcp_servers/travel_mcp_server.py
```

Available tools:

| Tool | Description |
|---|---|
| `get_destinations` | Retrieve available destinations |
| `calculate_trip_cost` | Calculate estimated trip expenses |
| `find_destinations_by_budget` | Find destinations within a budget |

### 10.2 Knowledge MCP Server

File:

```text
mcp_servers/knowledge_mcp_server.py
```

Available tool:

| Tool | Description |
|---|---|
| `search_travel_knowledge` | Search travel knowledge documents using RAG |

### 10.3 MCP Communication

The MCP servers use STDIO transport.

The MCP client starts the server processes automatically using Python subprocesses.

**Important:** You normally do not need to start these servers manually. The application starts them when required.

For debugging, you can inspect the server scripts, but do not leave separately started server processes running while testing the normal application.

---

## 11. Test MCP Integration

Activate the project virtual environment first.

### Test 1: Discover Travel MCP tools

```powershell
python -c "from mcp_client.client import list_mcp_tools; print(list_mcp_tools('travel'))"
```

Expected tools:

```text
get_destinations
calculate_trip_cost
find_destinations_by_budget
```

### Test 2: Execute Travel MCP tool

```powershell
python -c "from mcp_client.client import call_mcp_tool; print(call_mcp_tool('travel','get_destinations',{}))"
```

Expected: A list of available travel destinations.

### Test 3: Discover Knowledge MCP tools

```powershell
python -c "from mcp_client.client import list_mcp_tools; print(list_mcp_tools('knowledge'))"
```

Expected:

```text
search_travel_knowledge
```

### Test 4: Execute Knowledge MCP tool

```powershell
python -c "from mcp_client.client import call_mcp_tool; print(call_mcp_tool('knowledge','search_travel_knowledge',{'query':'Is Manali safe to visit in July?','top_k':3}))"
```

Expected: Relevant travel knowledge retrieved from the RAG system.

---

## 12. Run the Application

Once the dependencies, database, and MCP integration are ready:

```powershell
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:7860
```

The exact port depends on your Gradio launch configuration.

---

## 13. Test the Application

Try the following example questions in the chat interface.

### Test 1: Destination discovery

```text
Show me all available travel destinations.
```

### Test 2: Budget estimation

```text
Calculate the trip cost for Goa for 4 friends for 3 nights.
```

### Test 3: Budget-based destination search

```text
Suggest destinations for 4 friends with a budget of ₹10,000 per person for 3 nights.
```

### Test 4: Travel knowledge / RAG

```text
Is Manali safe to visit in July?
```

### Test 5: Conversation memory

```text
I am planning a trip to Goa with 4 friends.
```

Then ask:

```text
How many friends am I travelling with?
```

The assistant should use the previously stored conversation context when the same session is maintained.

---

## 14. Troubleshooting

### Error: No module named `gradio`

```powershell
python -m pip install gradio
```

### Error: No module named `mcp`

```powershell
python -m pip install "mcp[cli]>=1.28,<2"
```

### Error: No module named `sentence_transformers`

```powershell
python -m pip install sentence-transformers
```

### Error: Python is using the wrong virtual environment

```powershell
python -c "import sys; print(sys.executable)"
```

Activate the correct environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Error: MCP JSON-RPC or invalid JSON response

Check the following:

1. MCP server scripts use STDIO transport.
2. Diagnostic logging goes to `stderr`, not `stdout`.
3. Imported modules do not print debugging messages to `stdout`.
4. The MCP client starts the correct Python executable.
5. The server script paths are correct.

### Error: OpenAI authentication

Check:

1. `.env` exists in the project root.
2. `OPENAI_API_KEY` is configured.
3. `config.py` loads the environment variables.
4. The key is valid and has the required API access.

---

## 15. Git Configuration

Recommended `.gitignore`:

```gitignore
# Virtual environments
.venv/
venv/

# Python cache
__pycache__/
*.py[cod]
*.pyo

# Environment variables
.env
.env.*

# SQLite databases
database/*.db
database/*.sqlite
database/*.sqlite3

# IDE
.vscode/
.idea/

# Logs
*.log

# Jupyter
.ipynb_checkpoints/

# Cache and temporary files
.cache/
.pytest_cache/
```

Check repository status:

```powershell
git status
```

Add and commit:

```powershell
git add .
git commit -m "Add Trip Buddy AI application and documentation"
git push
```

---

## 16. Docker and AWS Deployment

Deployment will be documented and verified separately after the local application is working.

Planned deployment architecture:

```text
              User Browser
                   |
                   v
              AWS ALB
                   |
                   v
             ECS Fargate
                   |
             Trip Buddy App
                   |
          -------------------
          |                 |
          v                 v
      Travel MCP       Knowledge MCP
          |                 |
          v                 v
      SQLite /         RAG Knowledge
      Travel Data       Retrieval
```

Planned deployment components:

- Docker image
- Amazon Elastic Container Registry (ECR)
- Amazon ECS Fargate
- Application Load Balancer (ALB)
- AWS Secrets Manager
- Amazon CloudWatch
- Amazon RDS PostgreSQL for persistent production data

**Note:** The current SQLite conversation memory is local to the application. It will not provide durable storage across ECS task replacements. Persistent production storage needs to be addressed before deployment.

---

## 17. Development Roadmap

- [x] Gradio-based travel assistant
- [x] Travel MCP server
- [x] Knowledge MCP server
- [x] SQLite conversation memory
- [x] Response formatter
- [ ] Verify all MCP tool executions
- [ ] Verify complete end-to-end application flow
- [ ] Add automated tests
- [ ] Add Docker support
- [ ] Test the Docker container locally
- [ ] Configure AWS ECR
- [ ] Deploy to AWS ECS Fargate
- [ ] Configure persistent production storage
- [ ] Configure HTTPS and monitoring

---

## 18. Quick Start

For an existing local checkout on Windows PowerShell:

```powershell
# 1. Navigate to project
cd D:\AIML\aibootcamp\trip_buddy_agent

# 2. Activate environment
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Run application
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

**Trip Buddy AI – Your intelligent travel planning companion.**
