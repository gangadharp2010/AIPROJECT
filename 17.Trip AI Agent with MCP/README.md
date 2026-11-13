# Trip AI Agent with MCP — Trip Buddy

## Project overview

Trip Buddy is a conversational travel-planning assistant implemented as a Python application. It combines a custom travel agent, Gradio interface, Model Context Protocol (MCP) tools, travel-knowledge retrieval (RAG), and SQLite-backed conversation memory.

The project is organized as an application under `trip_buddy_agent/`.

## Capabilities represented in the codebase

- Conversational travel planning through a Gradio application.
- Travel tools for destination discovery, trip-cost estimation, and budget-based destination search.
- A dedicated Travel MCP server and a Knowledge MCP server.
- An MCP client that communicates with the server processes.
- Retrieval of travel knowledge through a RAG component.
- Conversation memory and preference handling backed by SQLite.
- Response formatting for readable travel suggestions and estimates.
- Test modules for agent and conversation-memory behavior.
- Docker packaging files.

## High-level architecture

```text
User
 |
 v
Gradio Chat Application
 |
 v
Travel Agent + Conversation Memory
 |
 +-------------------+
 |                   |
 v                   v
Travel MCP Client    Knowledge Retrieval
 |                   |
 v                   v
Travel MCP Server    Knowledge MCP Server
 |                   |
 v                   v
Travel Tools         Travel Knowledge
 |
 v
Formatted Assistant Response
```

## Repository structure

The detailed application code, dependencies, configuration, and setup instructions are located in:

`trip_buddy_agent/`

Read the [application README](trip_buddy_agent/README.md) for Python setup, environment configuration, MCP server details, tests, and run instructions.

## Technology stack

- Python
- Gradio
- Model Context Protocol (MCP)
- Retrieval-Augmented Generation (RAG)
- SQLite
- Docker

The application README describes the package versions and configuration assumptions. Use those project-specific instructions when setting up the environment.

## Responsible use and limitations

Trip planning outputs and estimated costs should be checked against current provider information before booking. Retrieved knowledge may be incomplete or outdated. Treat generated recommendations as planning assistance, not as confirmation of live availability, current prices, visa rules, or safety conditions.

## Author

Gangadhar Panda
