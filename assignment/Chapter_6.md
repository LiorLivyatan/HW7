# 6 Homework Requirements

## 6.1 Goal of the Exercise
In this exercise you will implement an AI agent for the Even/Odd league. At this stage, your agent will run only in your local environment. It is recommended to coordinate with other students to verify protocol compatibility.

**Very Important:** Use the protocol defined in this document exactly. Otherwise your agent will not be able to communicate with others.

It is mandatory to build and program the project subject to the guidelines of Chapter 9 (Protocol data of the league), Chapter 10 (Tools kit in Python), and Chapter 11 (Project structure). Also verify that the project runs and functions as defined in Chapter 8 (Running the league system).
This exercise is based on the book:

**AI Agents with Model Context Protocol**
By Dr. Yoram Segal
December 9, 2025

Therefore it is highly recommended to read and learn the subject in depth.

## 6.2 Mandatory Tasks

### 6.2.1 Task 1: Player Agent Implementation
Implement an MCP server listening on a port on localhost. The server must support the following tools:
1. `handle_game_invitation` – Receiving invitation to a match and returning `GAME_JOIN_ACK`.
2. `choose_parity` – Choosing "even" or "odd" and returning `CHOOSE_PARITY_RESPONSE`.
3. `notify_match_result` – Receiving match result and updating internal state.

### 6.2.2 Task 2: Registration to League
The agent must send a registration request to the League Manager. The request will include:
- Unique display name (Your name or nickname).
- Agent version.
- Endpoint address of the server.

### 6.2.3 Task 3: Self Check
Before submission, check your agent:
1. Run a local league with 4 players.
2. Verify that the agent responds to every message type.
3. Verify that the JSON structures match the protocol.

## 6.3 Technical Requirements

### 6.3.1 Programming Language
You can choose any language you want. The main thing is that the agent:
- Implements an HTTP server.
- Responds to POST requests at path `/mcp`.
- Returns JSON in format JSON-RPC 2.0.

### 6.3.2 Response Times
- `GAME_JOIN_ACK` – Within 5 seconds.
- `CHOOSE_PARITY_RESPONSE` – Within 30 seconds.
- Every other response – Within 10 seconds.

### 6.3.3 Stability
The agent must:
- Operate without crashes.
- Handle exceptions (Exception Handling).
- Not stop operating in the middle of a league.

## 6.4 Work Process

### 6.4.1 Step 1: Local Development
1. Implement the agent.
2. Check locally with your code.
3. Fix bugs.

### 6.4.2 Step 2: Private League
1. Run a local league with 4 copies of the agent.
2. Check that all communication works.
3. Improve the strategy (optional).

### 6.4.3 Step 3: Compatibility Check with Other Students
1. Coordinate with another student to exchange agents.
2. Check that the agents communicate properly.
3. Verify that the JSON structures match the protocol.

### 6.4.4 Look to the Future: Class League
In the future, it is possible that there will be:
- Creation of new games (not only Even/Odd).
- Competition in the class as part of the summary project.
This topic has not been closed yet and changes are possible. You have to adapt the agent in a way that will allow expansion in the future.

## 6.5 Submission

### 6.5.1 Submission Files
1. Source code of the agent.
2. `README` file with running instructions.
3. Detailed report including:
   - Full description of the architecture and implementation.
   - Description of the strategy chosen and reasons for choice.
   - Difficulties encountered and solutions found.
   - Documentation of the development and testing process.
   - Conclusions from the exercise and recommendations for improvement.

### 6.5.2 Submission Format
There is to submit a link to a public repository. And there is to submit manually the report as requested above to the exercises checker.

## 6.6 General Highlights regarding Testing the Work
Updated to requirements The following next criteria will be checked:

**Table 13: Criteria for Testing**

| Description | Criteria |
| :--- | :--- |
| Basic functioning | The agent works, answers messages, plays in games |
| Protocol compatibility | JSON structures match exactly the protocol |
| Stability | The agent is stable, does not crash, handles errors |
| Code quality | Clean code, documented, organized |
| Documentation | Clear running instructions, detailed description |
| Strategy | Interesting strategy implementation (not only random) |

## 6.7 Common Questions

### 6.7.1 Is it possible to use external libraries?
Yes. You can use any library you want. Verify that you supply appropriate installation instructions.

### 6.7.2 Is it mandatory to use Python?
No. Use any language that suits you. The main thing is that the agent adheres to the protocol requirements.

### 6.7.3 What happens if the agent of the course?
The agent will suffer a technical loss in the current game. If it does not return to operation – it will leave the league.

### 6.7.4 Is it possible to update the agent after submission?
No. The final submission. Check well before submitting.

### 6.7.5 How do I know what is my rating?
Ranking table will be published after every round. You will be able to see your location relative to others.

## 6.8 Summary
1. Implement a player agent that adheres to the protocol.
2. Check locally before submission.
3. Submit the code and the report.
4. Your agent will play in the class league.

**Good Luck!**

**Additional Information:**
For questions and clarifications turn to Dr. Yoram Segal.
Recommended to read the book "AI Agents with MCP" [1].
For additional details on the MCP protocol see the official documentation [2].
