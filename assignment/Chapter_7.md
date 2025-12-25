# 7 Learning through the League Exercise
The Even/Odd league exercise is not only a programming exercise. It constitutes a pedagogical model for understanding the MCP protocol and AI agent principles. In this chapter we will explain how the exercise teaches the foundations of AI agents and the MCP protocol.

## 7.1 The Player as an AI Agent

### 7.1.1 Is the player an AI agent?
The first question to ask is: Is the player agent (Player Agent) in the league really an AI agent? The answer is unequivocally: Yes.

An AI agent is defined as an entity that maintains interaction with the environment in order to achieve defined goals [1]. Unlike a regular computer program executing predetermined instructions, an AI agent is autonomous software that receives information from the environment, processes it, and decides by itself what to perform based on the current situation.

### 7.1.2 The Four Characteristics of an AI Agent
We will examine the player in the league in light of the four main characteristics of an AI agent:
1. **Autonomy** – The agent operates independently. In the context of the game, the player decides absolutely autonomously which strategy to choose: "even" or "odd". No one dictates to it what to choose.
2. **Perception** – The agent receives information from the environment. The player receives game invitations (`GAME_INVITATION`), requests for choice (`CHOOSE_PARITY_CALL`), and game results (`GAME_OVER`) from the referee and the League Manager.
3. **Action** – The agent influences the environment. The player performs actions by sending choices (`CHOOSE_PARITY_RESPONSE`) and arrival confirmations (`GAME_JOIN_ACK`) to the games.
4. **Goal-oriented** – It has a defined goal. Its goal is to play, to win games and to update its internal state, such as history of victories and defeats.

The player can also use a large language model (LLM) to choose the best strategy. In this way it demonstrates "thinking" or "drawing conclusions" before executing the action.

## 7.2 The Player in MCP Architecture

### 7.2.1 Service or Client?
In the Even/Odd league architecture, the player is primarily an **MCP Server**.

An MCP server is a component that exposes capabilities and services, called "Tools", "Resources" or "Prompts". The server is defined as a separate process on a defined port and provides a "gateway" to the outside world [2].

Therefore the player is required to implement an HTTP server that accepts POST requests at the path `/mcp`. The rules that expose capabilities via the JSON-RPC 2.0 protocol. The tools that the player is obliged to implement include:
- `handle_game_invitation` – Handling a game invitation.
- `choose_parity` – Choosing "even" or "odd".
- `notify_match_result` – Receiving a notification on the game result.

### 7.2.2 Relationships against the Referee and the League Manager
Given that the player is a server, who calls its services is the Client. In the league system, the Referee and the League Manager are the Actuators or Orchestrators.

The referee is the one creating the JSON-RPC request calling the tool `choose_parity` of the player. When the referee wants to collect choices from the players, it sends a request `CHOOSE_PARITY_CALL` to each player.

**Summary:** Although usually the player is an AI agent autonomously, in terms of MCP implementation, it fulfills the role of the server providing capabilities to the orchestrators.

## 7.3 The Referee and League Manager as AI Agents

### 7.3.1 Agents of High Degree
Also the referee and the League Manager are defined as AI agents. They stand at the same level as four characteristics:
These agents are not passive. They manage the entire system in accordance with general rules and defined goals. This is the essence of autonomy and purposefulness of an AI agent.

### 7.3.2 MCP Servers acting also as Clients
These two agents are defined as MCP Servers:
- The League Manager operates as an MCP server on port 8000. It implements tools like `register_player`, `register_referee`, and `report_match_result`.
- The Referee operates as an MCP server on port 8001. It implements tools like `start_match` and `collect_choices`.

**Important Note:** The referee and the League Manager, although they are defined as servers, are required to act also as MCP Clients to fulfill their central roles. For example:

**Table 14: Characteristics of an AI Agent for Referee and League Manager**

| Characteristic | League Manager | Referee |
| :--- | :--- | :--- |
| **Purposefulness** | Management of the entire league, registration of referees and players, schedule, calculation of ranking | Registration to the League Manager, management of a single match, verification of legality of moves, declaration of winner |
| **Autonomy** | Operates independently for registration of referees and fixing the schedule | Operates independently for management of stages of the game |
| **Perception** | Receives registration requests, reports of results from referees | Receives arrival confirmations, choices (Even/Odd) from the players |
| **Action** | Approves registration requests, sends invitations, sends round broadcast, updates standings table | Sends request for match invitation, sends request for choice, sends declaration of results |

- The referee must act as a client to register to the League Manager (`REFEREE_REGISTER_REQUEST`).
- The referee must act as a client to call the tool `choose_parity` of the player agent.
- The League Manager must act as a client to send the round announcement to the player agents.

In this system, the central servers are practically Orchestrator-Clients when they need to move the action at the players' servers.

## 7.4 Reversal of Roles: Central Insight

### 7.4.1 The Traditional Paradigm
In a traditional client-server architecture, the client is the active component that sends a request, and the server is the passive component waiting for a request. In the AI league, the roles are reversed creatively.

### 7.4.2 Function Reversal in the League
**The Player (The Autonomous Agent) is the Server:** Although the player is the autonomous entity needing to perform an action, it is required to expose its capabilities as an MCP Server.

**The Referee and the League Manager (The Orchestrators) are the Clients:** The referee is the Orchestrator acting as an MCP Client calling the tool `choose_parity` of the player in order to get it to move in the game.

*(Diagram reference: Player 1 (MCP Server :8101) <- (choose_parity) - Referee (Orchestrator, Acts as MCP Client :8001) - (choose_parity) -> Player 2 (MCP Server :8102). Referee <- (ROUND_ANNOUNCEMENT) - League Manager (Acts as MCP Client :8000))*

## 7.5 Principle of Separation of Layers

### 7.5.1 Three Separate Layers
The MCP protocol enables clear separation between the roles:
1. **League Layer** (Managed by the League Manager) – Recruitment of players, game schedule (Round-Robin), and standings table.
2. **Refereeing Layer** (Managed by the Referee) – Management of a single match and verification of moves.
3. **Game Rules Layer** (Managed by a separate module) – Specific logic for Even/Odd.

### 7.5.2 Benefit of Separation
The player, in that it exposes a standard MCP interface (JSON-RPC 2.0 over HTTP), enables the league to remain agnostic to the development language or the internal strategy.
This is a solution to the fragmentation problem where every agent and every model demanded in the past a unique integration. The MCP protocol solves this by creating a universal interface [2].
When the player receives a request like `CHOOSE_PARITY_CALL`, the data arrives in a fixed JSON structure. The player responds with `CHOOSE_PARITY_RESPONSE`, also in a fixed structure. This ensures that every agent, regardless of the way it calculates the data, can communicate efficiently with every orchestrator respecting the protocol.

## 7.6 The Role of the LLM in the Agent

### 7.6.1 The Dilemma
An interesting question arises: On one hand, the player is defined as an MCP server that exposes capabilities. On the other hand, it is described as an autonomous AI agent that can use an LLM as a "brain" to choose a strategy. By traditional definition, a server is not an "operator" of a "brain" but fills a request.

### 7.6.2 The Solution: Separation of Roles
The solution lies in understanding that the MCP function (Client/Server) and the AI components (Brain/Tools) are separate but complementary concepts.

**The Agent is also a Server and also a Client (Effectively):** Every one of the agents acts in practice also as a server and also as a client. The role of the server is required for every agent so that the host can enable communication to others to call it. The role of the client is required for every agent needing to initiate interaction.

**The LLM as an Internal Component:** A large language model is the "Brain" of the AI agent. If the player implements an MCP server, the LLM is simply an internal component within the general agent.
When the server receives a request `choose_parity`:
1. The MCP layer (The Server) receives the request.
2. The internal logic of the agent (The LLM or another strategy) operates to determine the choice.
3. The MCP layer (The Server) sends the response back.

The LLM is the "Intelligence" of the server, and it is not a server-client model. The central idea in MCP is to ensure that even when the "Brain" is found within the server, external communication will remain standard via JSON-RPC.

### 7.6.3 Analogy: Customer Service Station
It is possible to imagine the architecture as a customer service station:
- **MCP (Protocol)** – is the telephone and the language in which people speak (JSON-RPC over HTTP).
- **The Player (Server)** – is the service office with a telephone line of its own.
- **The Strategy/LLM (The Brain)** – is the smart consultant sitting inside the office, who receives the call, calculates the answer, and dictates to the clerk what to write back in the MCP layer response to send.

The internal tools (The LLM and the logic) are not exposed directly to the MCP protocol, but serve the public tools that the agent exposes, such as `choose_parity`.

## 7.7 Role of the Orchestrator

### 7.7.1 League Manager – The Architect
The League Manager is an agent at the highest level in terms of strategy, the manager of the league layer. It is not involved in the rules of the game itself, but in the general management: The schedule and the standings table.

**Benefit of Separation:** If the league wants to replace the game from Even/Odd to Tic-Tac-Toe, the League Manager almost does not change. This is a perfect example of the principle of Separation of Concerns promoted by MCP.

### 7.7.2 The Referee – The Internal Implementer
The referee embodies the refereeing layer. It does not know the general rules of the game (handled separately), but acts as responsible for managing the conversation (Conversation Lifecycle) between the players.
The referee verifies that the players meet the deadlines (Deadlines). It is the one activating the loop of the external agent for the players – it calls `choose_parity` so that they perform the autonomous action of the player.
**MCP allows splitting the clear roles:** The referee manages and the League Manager is responsible for the "id" (The communication protocol), while the players are responsible for the "what" (The strategy and the content).

## 7.8 What does the Exercise Teach

### 7.8.1 Basic Principles of AI Agents
The exercise teaches the four characteristics of an AI agent in a practical way:
- **Autonomy** – The player decides by itself.
- **Perception** – The player receives notifications from the system.
- **Action** – The player sends responses.
- **Goal-oriented** – The player strives to win.

### 7.8.2 Basic Principles of MCP
The exercise teaches the core principles of the MCP protocol:
1. **Standard Interface** – Every agent exposes tools via JSON-RPC 2.0.
2. **Separation of Roles** – League layer, refereeing layer, and game rules layer.
3. **Language Agnosticism** – Possible to implement an agent in any programming language.
4. **Communication via Orchestrator** – Agents do not talk directly, but via the referee or the League Manager.
5. **Registration of Agents** – Referees and players register to the League Manager before the start of the games.

### 7.8.3 The Learning Experience
At the end of the exercise, the student will understand:
- How an AI agent communicates with other agents.
- How to build a simple MCP server.
- What is the meaning of "Tools" in the MCP protocol.
- How an orchestrator manages interaction between agents.
- Why separation of layers is important for designing AI systems.

## 7.9 Summary
The Even/Odd league exercise constitutes a pedagogical model integrated for understanding the MCP protocol and AI agents. The simple game allows focusing on the architectural principles without getting complicated with complex logic.

The student learns that an AI agent can be also an MCP server – reversal of roles creates the possibility for the orchestrator to call the agents and activate their actions. The separation of layers ensures that it will be possible to replace the game in the future without changing the general protocol.

For additional details on the MCP protocol, see the book "AI Agents with MCP" [1] and the official documentation of Anthropic [2].
