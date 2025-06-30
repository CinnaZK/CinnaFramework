# Cinna Agent Framework

A flexible, multi-interface AI agent framework built to operate across diverse platforms such as Telegram, Discord, Twitter, Farcaster, REST APIs, and MCP environments.

Get a free Cinna API Key instantly using the code `agent` at https://cinnazk.app/dev-access

---

## Overview

The Cinna Agent Framework is designed with a modular architecture that enables agents to:

- Process text and voice input
- Generate and manipulate images and video
- Operate uniformly across multiple platforms
- Query and store knowledge via PostgreSQL or SQLite
- Compose workflows by calling external APIs and Mesh Agents

---

## Table of Contents

- Features
- Cinna Mesh
- MCP Support
- Recommended Mesh Agents
- Full Mesh Agent List
- Agent Architecture
- Usage and Dev Guide
- Agent Interfaces
- Cinna Core
- Components & Workflows
- External Clients
- Dev Setup & GitHub Issues
- License & Contributions

---

## Features

- Modular agent structure with LLM integration
- Plug-and-play architecture for tools and workflows
- Advanced logic chains like RAG and Chain of Thought
- Media generation tools (image/audio)
- Voice transcription and text-to-speech
- Knowledge base integration (PostgreSQL/SQLite)
- MCP-ready tool execution layer
- Native platform support for:
  - Telegram
  - Discord
  - Twitter
  - Farcaster
  - REST API
  - MCP interfaces

---

## Cinna Mesh

Cinna Mesh is a decentralized network of task-specific AI agents. Each Mesh Agent specializes in a unique Web3 domain and can perform targeted data processing, reporting, or interaction. These agents function like modular smart contracts for intelligence workflows.

All agents are accessible through a unified API or via MCP for integration into custom assistant frameworks.

Want to contribute your own agent? Visit the Mesh README for best practices and implementation guides.

---

## MCP Integration

All Cinna Mesh agents are fully MCP-compatible and accessible from Claude Desktop, Cursor, Windsurf, and other MCP clients.

To run your own MCP server, follow the instructions in the Cinna Mesh MCP Server repo.

---

## Recommended Mesh Agents

- `BitquerySolanaTokenInfoAgent`: Solana token analytics, holders, trends
- `CoinGeckoTokenInfoAgent`: Market data and token categories
- `DexScreenerTokenInfoAgent`: Real-time trading data across chains
- `ElfaTwitterIntelligenceAgent`: Token and influencer analysis on Twitter
- `ExaSearchAgent`: Web search with direct question answering
- `GoplusAnalysisAgent`: Security analysis for token contracts
- `MetaSleuthSolTokenWalletClusterAgent`: Cluster behavior on Solana
- `PumpFunTokenAgent`: Solana-based Pump.fun token analysis
- `SolWalletAgent`: Query Solana wallet holdings and swaps

---

## Architecture

### Agent Structure

- `BaseAgent`: Abstract class that defines shared behaviors and lifecycle handling
- `CoreAgent`: Implements `BaseAgent`, orchestrates components and selects workflows

### Agent Interfaces

Each interface inherits from `BaseAgent` and adapts it to a specific platform:
- Telegram: `telegram_agent.py`
- Discord: `discord_agent.py`
- Twitter: `twitter_agent.py`
- Farcaster: `farcaster_agent.py`
- API: `flask_agent.py`

---

## Cinna Core

Cinna Core includes reusable tools and components designed to build intelligent agents or applications, usable independently or with the full framework.

### Key Components

- `PersonalityProvider`: Sets tone, role, and prompt logic
- `KnowledgeProvider`: Vector search from DB
- `ConversationManager`: Tracks conversation context
- `ValidationManager`: Ensures input-output quality
- `MediaHandler`: Processes images and audio
- `LLMProvider`: Interfaces with language models
- `MessageStore`: Indexes and retrieves conversations

### Workflows

- `AugmentedLLMCall`: Combines RAG with tool use
- `ChainOfThoughtReasoning`: Step-by-step execution
- `ResearchWorkflow`: Structured deep search and summarization

---

## Tool Management

- `ToolBox`: Registers tools
- `Tools`: Executes commands
- `ToolsMCP`: Integrates with MCP protocol

---

## External Clients

- `SearchClient`: Unified search engine wrapper
- `MCPClient`: For local/remote MCP operations

---

## Development Setup

```bash
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

To run a file:
```bash
python filename.py
# or
uv run filename.py
```

---

## Using GitHub Issues

Use GitHub issues for:

- **Integration Requests**: New data sources or use cases
- **Bug Reports**: Describe errors in detail
- **Questions**: General inquiries and support
- **Bounties**: Marked with reward offers

Always mention “I’m working on this” in issue threads if you start contributing.

---

## License

MIT License. See LICENSE file.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit and push your changes
4. Open a Pull Request

To contribute new Mesh Agents, refer to the Cinna Mesh README.
