# 1 Introduction: AI Agents and MCP Protocol

## 1.1 What is an AI Agent?
An AI agent is autonomous software. The agent receives information from the environment. It processes the information. After that, it performs actions.

An AI agent is different from a regular program. A regular program performs instructions set in advance. An AI agent decides by itself what to do. The decision is based on the current situation.

### 1.1.1 Characteristics of an AI Agent
Every AI agent has a number of characteristics:
- **Autonomy** – The agent operates independently.
- **Perception** – The agent receives information from the environment.
- **Action** – The agent influences the environment.
- **Goal-oriented** – The agent has a defined goal.

In the book by Dr. Yoram Segal "AI Agents with MCP" [1], it is explained how agents communicate. The book presents the MCP protocol in detail. We will use these principles in the exercise.

## 1.2 MCP Protocol – Model Context Protocol
MCP is a communication protocol. The protocol was developed by Anthropic. It allows AI agents to communicate with each other.

### 1.2.1 Protocol Principles
The protocol is based on a number of principles:
1. **Structured Messages** – Every message is a JSON object.
2. **JSON-RPC 2.0 Standard** – The protocol uses this standard.
3. **Tools** – Agents expose functions as "tools".
4. **Flexible Transport** – Possible to use HTTP or stdio.

### 1.2.2 Architecture Host/Server
In the MCP system there are two types of components:

**MCP Server** – A component that provides services. The server exposes "tools" that enable calling them. Every tool is a function with defined parameters.

**Host** – A component that coordinates between servers. The host sends requests to servers. It receives answers and processes them.

*(Diagram reference: Host (Orchestrator) connected via JSON-RPC to MCP Server 1, MCP Server 2, MCP Server 3)*

## 1.3 Communication HTTP on localhost
In this exercise we will use HTTP communication. Every agent will operate on a different port on localhost.

### 1.3.1 Port Definition
We will define fixed ports for every agent:
- League Manager – Port 8000
- Referee – Port 8001
- Players – Ports 8101 to 8104

Every agent implements a simple HTTP server. The server accepts POST requests at the path `/mcp`. The content of the request is JSON-RPC 2.0.

### 1.3.2 Example of Agent Address
Address of League Manager server:
`http://localhost:8000/mcp`

Address of first player server:
`http://localhost:8101/mcp`

## 1.4 Message Structure JSON-RPC
Every message in the protocol is a JSON object. The message has a fixed structure.

**Basic Structure of a Message**
```json
{
  "jsonrpc": "2.0",
  "method": "tool_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  },
  "id": 1
}
```

Fields in the message:
- `jsonrpc` – Protocol version, always "2.0".
- `method` – Name of the tool we want to operate.
- `params` – Parameters for the tool.
- `id` – Unique identifier for the request.

## 1.5 Goal of the Exercise
In this exercise we will build a league system for AI agents. The system will include three types of agents:
1. **League Manager** – Manages the league, including registration of players and referees.
2. **Referee** – Signs up to the league manager and manages single games.
3. **Player Agents** – Participate in the games.

**Registration Process:** Before the start of the league, referees and also players must register with the League Manager. The League Manager keeps a list of available referees and assigns them to games.

The specific game in the exercise is "Even/Odd". The general protocol allows replacing the game in the future. It will be possible to use Rock-Paper-Scissors, 12 Questions, or other games.

### 1.5.1 Learning Objective
At the end of the exercise you will be able to:
- Understand the MCP protocol.
- Build a simple MCP server.
- Communicate between different agents.
- Run a full league in your environment.
- Verify compatibility of the protocol with other students.

**Important:** All students will use the same protocol. This will allow your agents to play against this in the future.
