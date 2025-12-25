# CLAUDE.md - Comprehensive Assignment Completion Guide

## Purpose
This guide ensures assignments are completed with the highest quality to achieve a 100/100 grade in the LLMs and Agents course.

---

## Quick Start for New Claude Code Session

**If you're starting a new session**, here's what you need to know immediately:

### 1. Read These Files First
- **This file (CLAUDE.md)**: Complete guide to 100/100 assignment completion
- **agents_and_skills.md**: List of Claude Code agents to create/use
- **Assignment files**: Look for assignment description (PDF, .md, or .txt)
- **PDF Guidelines**:
  - `software_submission_guidelines.pdf`: Dr. Yoram Segal's grading criteria (Version 2.0)
  - `self-assessment-guide.pdf`: Self-assessment guide

### 2. Project Structure Already Created
The project is organized as a proper Python package with:
- `/src/my_project/`: All source code
- `/tests/`: Unit and integration tests (70%+ coverage required)
- `/docs/`: PRD.md, ARCHITECTURE.md, API docs, PROMPTS_BOOK.md
- `/data/`: Raw and processed data
- `/results/`: Experiments and visualizations
- `/config/`: Configuration files
- Root files: `pyproject.toml`, `requirements.txt`, `README.md`, `.env.example`, `.gitignore`

### 3. Critical Requirements (Version 2.0)
**NEW in Version 2.0** - These are NON-OPTIONAL:
1. **Package Organization** (Chapter 13): Proper Python package with `pyproject.toml`, `__init__.py`, relative imports
2. **Multiprocessing/Multithreading** (Chapter 14): Correct parallel processing based on operation type
3. **Building Block Design** (Chapter 15): Modular architecture with Input/Output/Setup documentation

### 4. Grading Breakdown
- **60%**: Academic criteria (Chapters 1-12) - Documentation, code quality, testing, research
- **40%**: Technical criteria (Chapters 13-15) - Package structure, parallel processing, building blocks

### 5. Workflow Overview
1. **Read assignment** thoroughly
2. **Fill in assignment-specific sections** in CLAUDE.md and agents_and_skills.md
3. **Plan architecture** and building blocks
4. **Implement** following all criteria
5. **Test** (70%+ coverage)
6. **Document** (PRD, ARCHITECTURE, README, API docs, PROMPTS_BOOK)
7. **Self-assess** honestly
8. **Review** against all checklists in this file

### 6. Where to Find Information
- **Project structure**: See "Project Structure & File Organization" section below
- **Academic criteria**: See "Part I: Academic Criteria (60%)" section
- **Technical criteria**: See "Part II: Technical Criteria (40%)" section
- **Checklists**: Throughout this document and in "Quality Assurance Checklist" section
- **Building block template**: See "Building Blocks Documentation" section
- **Parallel processing**: See "Parallel Processing Documentation" section

---

## Grading System Overview

### Grade Weighting
- **60%** Academic criteria (Chapters 1-12)
- **40%** Technical criteria (Chapters 13-15)

### Grade Levels
- **90-100**: Outstanding excellence - "needle in haystack" search, meticulous attention to every detail
- **80-89**: Very good - Thorough and methodical inspection of all criteria
- **70-79**: Good - Reasonable and balanced inspection with main criteria
- **60-69**: Basic pass - Flexible and forgiving, if reasoning exists

---

## Project Structure & File Organization

**Reference**: Software Submission Guidelines PDF, Chapter 13 - "Package Organization as a Package"

This project MUST be organized as a proper Python package. Below is the complete structure with detailed explanations of what belongs in each directory and file.

### Complete Directory Structure

```
HW7/
├── src/
│   └── my_project/              # Main package directory
│       ├── __init__.py          # Package initialization
│       ├── agents/              # Agent implementations
│       │   ├── __init__.py
│       │   └── [agent_files].py
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   └── [utility_files].py
│       ├── config/              # Configuration classes
│       │   ├── __init__.py
│       │   └── settings.py
│       └── core/                # Core business logic
│           ├── __init__.py
│           └── [core_files].py
├── tests/
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   └── test_*.py
│   └── integration/             # Integration tests
│       ├── __init__.py
│       └── test_*.py
├── docs/
│   ├── PRD.md                   # Product Requirements Document
│   ├── ARCHITECTURE.md          # Architecture Documentation
│   ├── API_REFERENCE.md         # API Documentation
│   └── PROMPTS_BOOK.md          # All prompts used with AI
├── data/
│   ├── raw/                     # Original, immutable data
│   │   └── .gitkeep
│   └── processed/               # Cleaned, processed data
│       └── .gitkeep
├── results/
│   ├── experiments/             # Experiment results
│   │   └── .gitkeep
│   └── visualizations/          # Generated plots and graphs
│       └── .gitkeep
├── config/
│   ├── config.yaml              # Main configuration file
│   └── [other_configs].json
├── notebooks/
│   └── analysis.ipynb           # Jupyter notebooks for analysis
├── assets/
│   ├── images/                  # Images for documentation
│   └── diagrams/                # Architecture diagrams
├── pyproject.toml               # Python package configuration (REQUIRED)
├── requirements.txt             # Python dependencies
├── README.md                    # Main project documentation
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore file
└── CLAUDE.md                    # This file (assignment guide)
```

#### Assignment-Specific Structure Note
For the Even/Odd League assignment, you may also have a different structure:
- **`SHARED/`** directory with `config/`, `data/`, `logs/`, and `league_sdk/` (shared resources)
- **`agents/`** directory with `league_manager/`, `referee_REF01/`, and `player_P01/` (agent implementations)
- See "Assignment-Specific Requirements" section (line ~941) for full details on the Even/Odd League structure

Both structures are valid - choose based on whether you're following the assignment's Chapter 11 structure or the general course structure. The key is maintaining proper package organization with `__init__.py` files and relative imports.

### Directory Explanations

#### `/src/my_project/` - Main Package Directory
**Purpose**: Contains all source code organized as a proper Python package
**Reference**: Chapter 13, Section on "Organized Directory Structure"

**Required Files**:
- `__init__.py`: **MUST EXIST**
  - Define `__version__ = "0.1.0"`
  - Export public interfaces in `__all__`
  - Example:
    ```python
    __version__ = "0.1.0"
    __author__ = "Your Name"

    from .core.main_module import MainClass
    from .agents.agent1 import Agent1

    __all__ = ["MainClass", "Agent1"]
    ```

**Subdirectories**:
- `agents/`: Agent implementations (if using multi-agent architecture)
- `utils/`: Helper functions, utilities, common tools
- `config/`: Configuration management classes
- `core/`: Core business logic and main functionality

**Critical Requirements**:
- All imports MUST use relative paths (e.g., `from .utils import helper`)
- NO absolute paths in code
- Files should be under 150 lines (Chapter 3, Project Structure)
- Each module should have a clear, single responsibility

#### `/tests/` - Test Directory
**Purpose**: All test files with 70%+ coverage requirement
**Reference**: Chapter 5 - "Testing & QA"

**Structure**:
- `unit/`: Unit tests for individual functions/classes
  - Name pattern: `test_<module_name>.py`
  - Each test file should mirror the structure in `src/`
  - Example: `test_agent1.py` tests `src/my_project/agents/agent1.py`

- `integration/`: Integration tests for component interactions
  - Test how different modules work together
  - Test API endpoints, database connections, etc.

**Required Content**:
- Test coverage report showing 70%+ for new code
- Edge case tests (empty input, None, invalid types, boundary conditions)
- Error handling tests
- Example test structure:
  ```python
  import pytest
  from my_project.core.main_module import MainClass

  class TestMainClass:
      def test_normal_case(self):
          """Test with normal input"""
          pass

      def test_edge_case_empty(self):
          """Test with empty input"""
          pass

      def test_error_handling(self):
          """Test error handling"""
          with pytest.raises(ValueError):
              # test code
              pass
  ```

**Commands to Run**:
```bash
pytest tests/ --cov=src/my_project --cov-report=html
pytest tests/ --cov=src/my_project --cov-report=term-missing
```

#### `/docs/` - Documentation Directory
**Purpose**: All project documentation
**Reference**: Chapter 1 - "Project Documentation" (20% of grade)

**Required Files**:

1. **PRD.md** - Product Requirements Document
   - Executive Summary (project overview, problem statement, target users)
   - Objectives and Goals (primary objectives, KPIs, acceptance criteria)
   - Functional Requirements (core features with user stories)
   - Non-Functional Requirements (performance, scalability, reliability, security, usability)
   - Technical Requirements (tech stack, dependencies, constraints)
   - Assumptions and Dependencies
   - Timeline and Milestones
   - Risks and Mitigation
   - Stakeholders
   - See template in `docs/PRD.md`

2. **ARCHITECTURE.md** - Architecture Documentation
   - High-Level Architecture (C4 Model - Context diagram)
   - Container Architecture (C4 Model - major components)
   - Component Architecture (detailed breakdown)
   - Building Blocks Documentation (Chapter 15 requirement)
     - For each building block: Input Data, Output Data, Setup Data
   - Data Flow diagrams
   - UML Sequence Diagrams
   - Parallel Processing Architecture (Chapter 14 requirement)
     - Multiprocessing design (if CPU-bound operations)
     - Multithreading design (if I/O-bound operations)
   - Deployment Architecture
   - Architecture Decision Records (ADRs)
   - Security Architecture
   - Quality Attributes (performance, scalability, maintainability)
   - See template in `docs/ARCHITECTURE.md`

3. **API_REFERENCE.md** - API Documentation
   - All public classes, methods, functions
   - Parameters, return values, exceptions
   - Usage examples
   - Generated from docstrings (use Sphinx or similar)

4. **PROMPTS_BOOK.md** - AI Prompts Documentation
   - ALL significant prompts used with AI tools
   - Context and reason for each prompt
   - Examples of outputs received
   - Iterative improvements
   - Best practices learned
   - **This is REQUIRED if you use AI tools**

#### `/data/` - Data Directory
**Purpose**: Store all data files separately from code
**Reference**: Chapter 3 - "Project Structure & Code Quality"

**Subdirectories**:
- `raw/`: Original, immutable data
  - NEVER modify files here
  - Keep original data intact
  - .gitkeep file to preserve directory in git

- `processed/`: Cleaned and processed data
  - Generated by processing scripts
  - Can be regenerated from raw data
  - .gitkeep file to preserve directory in git

**Important**:
- Large data files should be in `.gitignore`
- Use relative paths: `data_path = Path(__file__).parent.parent / "data" / "raw" / "file.csv"`

#### `/results/` - Results Directory
**Purpose**: Store experiment results and visualizations
**Reference**: Chapter 6 - "Research & Analysis" (15% of grade)

**Subdirectories**:
- `experiments/`: Experiment results, parameter variations
  - JSON or CSV files with results
  - Timestamp-based naming: `experiment_2024-01-15_14-30.json`

- `visualizations/`: Generated plots and graphs
  - High-resolution images (300+ DPI)
  - Bar charts, line charts, heatmaps, etc.
  - Clear captions and legends
  - Saved as PNG or SVG

**Important**:
- These can be regenerated, so add to `.gitignore` if large
- Document how to regenerate results in README

#### `/config/` - Configuration Directory
**Purpose**: Configuration files separate from code
**Reference**: Chapter 4 - "Configuration & Security" (10% of grade)

**Files**:
- `config.yaml` or `config.json`: Main configuration
  - Model parameters
  - System settings
  - Feature flags
  - All configurable parameters with defaults

**Requirements**:
- NO hardcoded values in source code
- All parameters documented with:
  - Description
  - Type
  - Valid range
  - Default value
- Example:
  ```yaml
  # config.yaml
  model:
    name: "gpt-4"
    temperature: 0.7  # Range: 0.0-2.0, Default: 0.7
    max_tokens: 2000  # Max: 4096, Default: 2000

  processing:
    batch_size: 100   # Default: 100
    num_workers: 4    # Default: CPU count
  ```

#### `/notebooks/` - Jupyter Notebooks Directory
**Purpose**: Analysis and experimentation notebooks
**Reference**: Chapter 6 - "Research & Analysis"

**Required Content**:
- `analysis.ipynb`: Main analysis notebook
  - Full documentation of experiments
  - Parameter exploration
  - Sensitivity analysis
  - Visualizations with explanations
  - Mathematical formulas in LaTeX (if applicable)
  - References to academic literature

**Quality Requirements**:
- Clear markdown explanations between code cells
- Well-commented code
- Reproducible results
- Organized flow (introduction → methods → results → conclusions)

#### `/assets/` - Assets Directory
**Purpose**: Static files for documentation and diagrams

**Subdirectories**:
- `images/`: Screenshots, logos, UI mockups
- `diagrams/`: Architecture diagrams
  - C4 Model diagrams (Context, Container, Component)
  - UML sequence diagrams
  - Data flow diagrams
  - Created with PlantUML, Mermaid, Draw.io, or similar

### Critical Root Files

#### `pyproject.toml` - Python Package Configuration
**Purpose**: Define project as a proper Python package
**Reference**: Chapter 13 - "Package Organization as a Package" (REQUIRED)

**MUST INCLUDE**:
```toml
[project]
name = "my_project"              # REQUIRED
version = "0.1.0"                # REQUIRED
description = "Project description"
authors = [{name = "Your Name", email = "your.email@example.com"}]
requires-python = ">=3.8"
dependencies = [                 # REQUIRED with version numbers
    "numpy>=1.21.0",
    "pandas>=1.3.0",
    "anthropic>=0.3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=22.0.0",
    "flake8>=5.0.0",
]

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_backend"
```

**Installation**:
```bash
pip install -e .          # Install in editable mode
pip install -e ".[dev]"   # Install with dev dependencies
```

#### `requirements.txt` - Dependencies List
**Purpose**: List all Python dependencies
**Reference**: Chapter 13

**Format**:
```txt
# Core Dependencies
numpy>=1.21.0
pandas>=1.3.0
anthropic>=0.3.0
openai>=1.0.0

# For development:
# pip install -e ".[dev]" from pyproject.toml
```

#### `README.md` - Main Documentation
**Purpose**: Comprehensive project documentation
**Reference**: Chapter 2 - "Code Documentation" (15% of grade)

**MUST INCLUDE**:
1. **Project Title and Description**
   - What the project does
   - Why it exists
   - Key features

2. **Installation Instructions**
   - Step-by-step setup
   - Prerequisites (Python version, system requirements)
   - Virtual environment creation
   - Dependency installation
   - Configuration setup

3. **Usage Instructions**
   - How to run the project
   - Command-line arguments
   - Configuration options
   - Examples with expected outputs

4. **Examples**
   - Code examples
   - Screenshots of running system
   - Expected outputs

5. **Configuration Guide**
   - How to set up `.env` file
   - Configuration parameters explained
   - Environment-specific settings

6. **Testing**
   - How to run tests
   - How to generate coverage reports

7. **Project Structure**
   - Brief explanation of directory organization

8. **Troubleshooting**
   - Common issues and solutions
   - FAQ

9. **Contributing** (if applicable)
   - How to contribute
   - Coding standards

10. **License**
    - License information

#### `.env.example` - Environment Variables Template
**Purpose**: Example environment variables without secrets
**Reference**: Chapter 4 - "Configuration & Security"

**MUST INCLUDE**:
```bash
# API Keys (NEVER commit actual keys!)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Configuration
ENVIRONMENT=development  # development, staging, production
DEBUG=True
LOG_LEVEL=INFO

# Project Settings
BATCH_SIZE=100
PROCESSING_MODE=fast  # fast or accurate

# Paths (use relative paths when possible)
DATA_DIR=./data
RESULTS_DIR=./results
CONFIG_DIR=./config
```

**Usage**:
```bash
cp .env.example .env
# Then edit .env with actual values
```

#### `.gitignore` - Git Ignore File
**Purpose**: Prevent committing sensitive data and generated files
**Reference**: Chapter 4 - "Configuration & Security" (10% of grade)

**MUST INCLUDE**:
```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/

# Virtual Environment
venv/
env/
.venv

# Environment variables and secrets
.env
.env.local
*.key
*.pem
secrets/
credentials.json

# Data files (might be too large)
data/raw/*
!data/raw/.gitkeep
data/processed/*
!data/processed/.gitkeep

# Results (can regenerate)
results/experiments/*
!results/experiments/.gitkeep
results/visualizations/*
!results/visualizations/.gitkeep

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDEs
.vscode/
.idea/
*.swp
.DS_Store

# Jupyter
.ipynb_checkpoints

# Logs
*.log
logs/
```

### Building Blocks Documentation (Chapter 15 Requirement)

**Reference**: Chapter 15 - "Building Block Design"

For EACH building block in your system, document in ARCHITECTURE.md:

#### Building Block Template

**Building Block Name**: [Descriptive Name]

**Purpose**: [What this building block does]

**Input Data**:
| Parameter | Type | Description | Valid Range | Required |
|-----------|------|-------------|-------------|----------|
| param1 | str | Description | Any string | Yes |
| param2 | int | Description | 1-100 | No (default: 10) |

**Output Data**:
| Parameter | Type | Description |
|-----------|------|-------------|
| result | dict | Description of output |
| status | str | "success" or "error" |

**Setup/Configuration**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| config1 | str | "default" | Configuration parameter |
| timeout | int | 30 | Timeout in seconds |

**Responsibilities**:
- Specific responsibility 1
- Specific responsibility 2

**Dependencies**:
- Building Block A (for data processing)
- External API X (for data retrieval)

**Error Handling**:
- `ValueError`: If input is invalid
- `TimeoutError`: If operation times out
- All errors logged with context

**Example Usage**:
```python
from my_project.core.building_block import BuildingBlock

block = BuildingBlock(config1="custom", timeout=60)
result = block.process(param1="value", param2=50)
```

### Parallel Processing Documentation (Chapter 14 Requirement)

**Reference**: Chapter 14 - "Multiprocessing & Multithreading"

Document in ARCHITECTURE.md:

#### When to Use Multiprocessing
- **Use for**: CPU-bound operations
- **Examples**:
  - Training ML models
  - Complex calculations
  - Data transformations
  - Encryption/decryption

**Implementation**:
```python
from multiprocessing import Pool, cpu_count

def cpu_intensive_task(data):
    # Complex computation
    return result

# Use all available CPUs
with Pool(processes=cpu_count()) as pool:
    results = pool.map(cpu_intensive_task, data_list)
```

**Checklist**:
- [ ] Number of processes based on `cpu_count()`
- [ ] Proper process termination (`pool.close()`, `pool.join()`)
- [ ] Exception handling for each process
- [ ] Avoiding shared state (use queues for communication)
- [ ] Memory management (avoid memory leaks)

#### When to Use Multithreading
- **Use for**: I/O-bound operations
- **Examples**:
  - Network requests (API calls)
  - File reading/writing
  - Database queries
  - Web scraping

**Implementation**:
```python
from concurrent.futures import ThreadPoolExecutor
import threading

def io_bound_task(url):
    # Network request
    return response

# Use thread pool
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(io_bound_task, urls)
```

**Checklist**:
- [ ] Thread pool size appropriate for I/O operations
- [ ] Proper thread synchronization (locks for shared data)
- [ ] Avoiding race conditions
- [ ] Avoiding deadlocks
- [ ] Graceful shutdown of threads

### Import Path Examples

**Reference**: Chapter 13 - "All imports use relative paths or package names"

**CORRECT** ✅:
```python
# Within package
from .utils.helpers import helper_function
from ..core.main import MainClass
from my_project.agents.agent1 import Agent1

# External packages
import numpy as np
from anthropic import Anthropic
```

**INCORRECT** ❌:
```python
# Absolute filesystem paths
import sys
sys.path.append('/Users/username/project/src')
from my_project.utils import helper

# Hardcoded paths
data = open('/Users/username/project/data/file.csv')
```

**File Path Handling** ✅:
```python
from pathlib import Path

# Get package root
PACKAGE_ROOT = Path(__file__).parent.parent
DATA_DIR = PACKAGE_ROOT / "data" / "raw"

# Read file
data_file = DATA_DIR / "input.csv"
with open(data_file, 'r') as f:
    data = f.read()
```

---

## Part I: Academic Criteria (60%)

### 1. Project Documentation (20%)

#### Product Requirements Document (PRD)
- Clear description of project purpose and user problem
- Measurable success metrics (KPIs)
- Detailed functional and non-functional requirements
- Constraints, assumptions, dependencies
- Milestones and timeline

#### Architecture Documentation
- Visual diagrams (C4 Model, UML)
- Operational architecture
- Architecture Decision Records (ADRs)
- API documentation and interfaces

### 2. Code Documentation (15%)

#### Comprehensive README
- Step-by-step installation instructions
- Detailed usage instructions
- Examples with screenshots
- Configuration guide
- Troubleshooting section

#### Code Quality
- Docstrings for every function/class/module
- Comments explaining complex design decisions
- Descriptive function and variable names

### 3. Project Structure & Code Quality (15%)

#### Project Organization
- Clear modular directory structure: src/, tests/, docs/, data/, results/, config/, assets/
- Separation between code, data, and results
- Files under ~150 lines
- Consistent naming conventions

#### Code Quality
- Focused, short functions (Single Responsibility)
- Avoid duplicate code (DRY)
- Consistent coding style throughout

### 4. Configuration & Security (10%)

#### Configuration Management
- Separate config files (.env, .yaml, .json)
- No hardcoded values in code
- Example config file (example.env)
- Parameter documentation

#### Information Security
- No API keys in source code
- Use environment variables
- Updated .gitignore

### 5. Testing & QA (15%)

#### Test Coverage
- Unit tests with 70%+ coverage for new code
- Edge cases testing
- Coverage reports

#### Error Handling
- Documented edge cases with responses
- Comprehensive error handling
- Clear error messages
- Debugging logs

#### Test Results
- Expected test results documentation
- Automated testing reports

### 6. Research & Analysis (15%)

#### Parameter Exploration
- Systematic experiments with parameter variations
- Sensitivity analysis
- Results table with outcomes
- Identification of critical parameters

#### Analysis Notebook
- Jupyter Notebook (or similar) with full documentation
- In-depth methodical analysis
- Mathematical formulas in LaTeX (if relevant)
- References to academic literature

#### Visual Presentation
- Quality graphs (bar charts, line charts, heatmaps, etc.)
- Clear captions and legends
- High resolution

### 7. User Interface & Extensibility (10%)

#### User Interface
- Clear and intuitive interface
- Workflow documentation with screenshots
- Accessibility considerations

#### Extensibility
- Extension points/hooks
- Plugin development documentation
- Clear interfaces

---

## Part II: Technical Criteria (40%)

### 8. Package Organization as a Package (NEW - Critical)

**This is a NEW requirement in version 2.0**

#### Package Definition File
- **MUST HAVE**: pyproject.toml or setup.py
- Required information: name, version, dependencies
- Detailed dependencies with version numbers

#### __init__.py Files
- Present in main package directory
- Exports public interfaces
- Defines __version__

#### Organized Directory Structure
- Source code in dedicated directory (e.g., /src or package name directory)
- Tests in separate /tests/ directory
- Documentation in separate /docs/ directory

#### Relative Paths
- ALL imports use relative paths or package names
- NO absolute paths in code
- File reading/writing relative to package location

#### Checklist
- [ ] Package definition file exists (pyproject.toml or setup.py)?
- [ ] Contains all required information (name, version, dependencies)?
- [ ] Dependencies specified with version numbers?
- [ ] __init__.py file in main directory?
- [ ] Exports public interfaces?
- [ ] __version__ defined?
- [ ] Source code in dedicated directory?
- [ ] Tests in separate directory?
- [ ] Documentation in separate directory?
- [ ] All imports use relative paths?
- [ ] No absolute paths in code?
- [ ] File reading/writing relative to package?

### 9. Multiprocessing & Multithreading (NEW - Critical)

**This is a NEW requirement in version 2.0**

#### Understanding the Difference
- **Multiprocessing**: For CPU-bound operations (computation, training ML models)
- **Multithreading**: For I/O-bound operations (network requests, file reading, database access)

#### Multiprocessing Checklist
- [ ] Identified CPU-bound operations?
- [ ] Operations suitable for parallelization?
- [ ] Evaluated potential benefit from parallel execution?
- [ ] Using multiprocessing module from Python?
- [ ] Number of processes dynamically set based on CPU count?
- [ ] Correct handling of data sharing between processes?
- [ ] Processes properly closed at end of work?
- [ ] Exception handling exists?
- [ ] Avoiding memory leaks?

#### Multithreading Checklist
- [ ] Identified I/O-bound operations?
- [ ] Operations include waiting (e.g., network, disk)?
- [ ] Evaluated potential benefit from concurrency?
- [ ] Using threading module from Python?
- [ ] Threads properly managed?
- [ ] Proper synchronization between threads (locks, semaphores)?
- [ ] Avoiding race conditions?
- [ ] Shared variables protected with locks?
- [ ] Avoiding deadlocks?

### 10. Building Block Design (NEW - Critical)

**This is a NEW requirement in version 2.0**

Building blocks are a modular approach to software architecture. Each block is an independent unit with:

#### Input Data
- Information required for operation execution
- Clear definition of all input data
- Data types specified
- Valid range for each parameter
- Comprehensive input validation

#### Output Data
- Products that the block creates
- Clear definition of all output data
- Data types specified
- Consistent output in all states

#### Setup Data
- Parameters and configuration for building block
- Default reasonable values
- Parameters loaded from config files or environment variables

#### Design Principles
1. **Single Responsibility**: Each block responsible for ONE defined task
2. **Separation of Concerns**: Each block deals with ONE aspect of system
3. **Reusability**: Blocks can be reused in different contexts
4. **Testability**: Each block can be tested independently

#### Checklist
- [ ] Created flow diagrams for system?
- [ ] Identified all main building blocks?
- [ ] Mapped dependencies and connections between blocks?
- [ ] Each block defined as class or separate function?
- [ ] Each block has clear and descriptive name?
- [ ] Each block has detailed docstring?
- [ ] All input data clearly defined?
- [ ] Input validation exists for all data?
- [ ] Appropriate error messages returned to user?
- [ ] All output data clearly defined?
- [ ] Output consistent in all states?
- [ ] Edge cases handled?
- [ ] All configuration parameters identified?
- [ ] Each parameter has reasonable default?
- [ ] Configuration separated from code?

---

## Assignment-Specific Requirements

### Assignment: Even/Odd League AI Agent (Homework 7)

#### Overview
Build an AI Player Agent for the Even/Odd League using the Model Context Protocol (MCP).

#### Your Task
Implement a **Player Agent** - an MCP server that:
1. Listens on a localhost port (e.g., 8101-8104)
2. Accepts POST requests at `/mcp` using JSON-RPC 2.0
3. Registers with the League Manager
4. Participates in Even/Odd games against other players
5. Follows the `league.v2` protocol exactly

#### The Even/Odd Game
- **Players**: 2 players per match
- **Gameplay**: Each player simultaneously chooses "even" or "odd" (without seeing opponent's choice)
- **Draw**: Referee draws a random number between 1-10
- **Winner**: If number is even and player chose "even" → player wins; if odd and chose "odd" → player wins
- **Scoring**: Win = 3 points, Draw = 1 point, Loss = 0 points
- **Tournament**: Round-Robin format (each player plays all others)

#### Three Agent System
1. **League Manager** (port 8000) - Manages registration, scheduling, standings *(provided)*
2. **Referee** (port 8001+) - Manages matches, draws numbers, declares winners *(provided)*
3. **Player Agent** (port 8101-8104) - **THIS IS WHAT YOU MUST IMPLEMENT**

#### Required Tools (3 mandatory)
Your Player Agent MCP server MUST implement these tools:

1. **`handle_game_invitation`** (Response time: ≤5 seconds)
   - Receives: GAME_INVITATION message with match_id, opponent_id, game_type
   - Returns: GAME_JOIN_ACK with acceptance and arrival timestamp

2. **`choose_parity`** (Response time: ≤30 seconds)
   - Receives: CHOOSE_PARITY_CALL with context (opponent, standings, deadline)
   - Returns: CHOOSE_PARITY_RESPONSE with parity_choice: "even" or "odd" (lowercase!)

3. **`notify_match_result`** (Response time: ≤10 seconds)
   - Receives: GAME_OVER message with winner, drawn_number, all choices
   - Returns: Acknowledgment, updates internal state

#### Critical Protocol Requirements

**MUST FOLLOW EXACTLY:**
- ✅ All timestamps in UTC/GMT (ISO-8601 format ending with 'Z')
- ✅ parity_choice must be lowercase: "even" or "odd"
- ✅ Include auth_token in all messages after registration
- ✅ Respond within timeout limits (5s/30s/10s)
- ✅ Match JSON structures from protocol specification exactly
- ✅ Use JSON-RPC 2.0 format for all messages

**WILL CAUSE FAILURE:**
- ❌ Local timezone timestamps (must be UTC!)
- ❌ "Even" or "Odd" with capital letters
- ❌ Missing auth_token
- ❌ Timeout violations
- ❌ Incorrect JSON structure

#### Message Flow Example
1. Player registers → League Manager (LEAGUE_REGISTER_REQUEST/RESPONSE)
2. League Manager announces round → All Players (ROUND_ANNOUNCEMENT)
3. Referee invites → Player (GAME_INVITATION)
4. Player confirms → Referee (GAME_JOIN_ACK) *[5s timeout]*
5. Referee requests choice → Player (CHOOSE_PARITY_CALL)
6. Player chooses → Referee (CHOOSE_PARITY_RESPONSE) *[30s timeout]*
7. Referee declares result → Players (GAME_OVER)
8. Referee reports → League Manager (MATCH_RESULT_REPORT)
9. League Manager updates → All Players (LEAGUE_STANDINGS_UPDATE)

#### Project Structure (Per Chapter 11)
```
HW7/
├── SHARED/                      # Shared resources (may be provided)
│   ├── config/                  # system.json, agents_config.json, etc.
│   ├── data/                    # standings.json, match history, etc.
│   ├── logs/                    # Structured logs (JSONL format)
│   └── league_sdk/              # Python SDK (ConfigLoader, JsonLogger, etc.)
├── agents/
│   ├── league_manager/          # (may be provided)
│   ├── referee_REF01/           # (may be provided)
│   └── player_P01/              # ← YOU IMPLEMENT THIS
│       ├── main.py              # Entry point, HTTP server setup
│       ├── handlers.py          # 3 tool implementations
│       ├── strategy.py          # Strategy logic (random/history/LLM)
│       └── requirements.txt     # Dependencies
└── doc/
    ├── protocol-spec.md         # Reference documentation
    └── message-examples/        # JSON message examples
```

**Note**: Align with existing project structure. Your player agent goes in `/src/my_project/agents/player/` or similar.

#### Strategy Options
1. **Random Strategy** (baseline): `random.choice(["even", "odd"])`
2. **History-Based**: Track opponent patterns (won't improve win rate statistically)
3. **LLM-Based**: Use Claude/GPT to decide (interesting but won't help in pure chance game)

**Important**: Even/Odd is pure luck - strategy won't affect long-term win rate. Focus on **correct protocol implementation** first!

#### Testing Requirements (Chapter 6.3)
Before submission:
1. Run local league with 4 copies of your agent
2. Verify all message types handled correctly
3. Verify JSON structures match protocol exactly
4. Test stability (no crashes, proper error handling)
5. (Optional) Test with other students' agents for compatibility

#### Submission Requirements (Chapter 6.5)
1. **Source code** of the Player Agent
2. **README** with:
   - Installation instructions (dependencies via pip/poetry)
   - Running instructions (how to start on specific port)
   - Configuration (how to set display name, etc.)
3. **Detailed report** including:
   - Architecture and implementation description
   - Strategy description and rationale
   - Difficulties encountered and solutions
   - Development and testing process documentation
   - Conclusions and recommendations for improvement
4. **Link to public repository**
5. **Manual report submission** to exercises checker

#### Evaluation Criteria (Chapter 6.6)
| Criterion | Description |
|-----------|-------------|
| Basic functioning | Agent works, answers messages, plays games |
| Protocol compatibility | JSON structures match protocol exactly |
| Stability | No crashes, handles errors gracefully |
| Code quality | Clean, documented, organized |
| Documentation | Clear instructions, detailed description |
| Strategy | Interesting implementation (not just random) |

#### Reference Chapters
- **Chapter 1**: Introduction to AI Agents and MCP
- **Chapter 2**: General League Protocol (message envelope, timeouts, error handling)
- **Chapter 3**: Even/Odd Game Rules and Flow
- **Chapter 4**: JSON Message Structures (18 message types defined)
- **Chapter 5**: Implementation Guide (FastAPI examples, state management)
- **Chapter 6**: Homework Requirements (what to implement and submit)
- **Chapter 7**: Learning through the Exercise (pedagogical context)
- **Chapter 8**: Running the League System (ports, terminals, full flow)
- **Chapter 9**: League Data Protocol (config/, data/, logs/ architecture)
- **Chapter 10**: Python Toolkit (league_sdk library)
- **Chapter 11**: Project Structure (directory tree, file organization)
- **Chapter 12**: References

---

## Detailed Implementation Workflow

**This section provides a step-by-step workflow for completing the assignment to achieve 100/100.**

### Phase 0: MCP Server Setup (For Even/Odd League Assignment Only)
**Time**: Day 0 (4-6 hours)
**Goal**: Set up the basic HTTP server infrastructure for the Player Agent

**Note**: This phase is specific to the Even/Odd League assignment. Skip if working on a different assignment.

#### Step 0.1: Choose HTTP Framework
Select one of the following frameworks for your MCP server:

- **FastAPI** (recommended):
  - Async support built-in
  - Automatic API documentation
  - Type hints with Pydantic
  - `pip install fastapi uvicorn pydantic`

- **Flask** (simpler):
  - Synchronous, easier to understand
  - Large community and resources
  - `pip install flask`

- **aiohttp** (async, lightweight):
  - Good for async operations
  - Lower-level than FastAPI
  - `pip install aiohttp`

#### Step 0.2: Implement Basic MCP Server
Create `src/my_project/agents/player/main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from datetime import datetime

app = FastAPI()

class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: dict = {}
    id: int = 1

class MCPResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: dict = {}
    id: int = 1

@app.post("/mcp")
async def mcp_endpoint(request: MCPRequest):
    """Main MCP endpoint - routes to appropriate tool handler"""
    if request.method == "handle_game_invitation":
        result = handle_invitation(request.params)
    elif request.method == "choose_parity":
        result = handle_choose_parity(request.params)
    elif request.method == "notify_match_result":
        result = handle_result(request.params)
    else:
        result = {"error": f"Unknown method: {request.method}"}

    return MCPResponse(result=result, id=request.id)

def handle_invitation(params):
    """Handle GAME_INVITATION -> return GAME_JOIN_ACK"""
    # TODO: Implement invitation handling
    return {
        "protocol": "league.v2",
        "message_type": "GAME_JOIN_ACK",
        "sender": "player:P01",  # TODO: Use actual player_id
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "conversation_id": params.get("conversation_id"),
        "match_id": params.get("match_id"),
        "player_id": "P01",  # TODO: Use actual player_id
        "arrival_timestamp": datetime.utcnow().isoformat() + "Z",
        "accept": True
    }

def handle_choose_parity(params):
    """Handle CHOOSE_PARITY_CALL -> return CHOOSE_PARITY_RESPONSE"""
    # TODO: Implement strategy
    import random
    choice = random.choice(["even", "odd"])

    return {
        "protocol": "league.v2",
        "message_type": "CHOOSE_PARITY_RESPONSE",
        "sender": "player:P01",  # TODO: Use actual player_id
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "conversation_id": params.get("conversation_id"),
        "match_id": params.get("match_id"),
        "player_id": "P01",  # TODO: Use actual player_id
        "parity_choice": choice  # MUST be lowercase "even" or "odd"
    }

def handle_result(params):
    """Handle GAME_OVER -> update internal state"""
    # TODO: Implement state management
    print(f"Match result received: {params}")
    return {"status": "acknowledged"}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8101, help="Port to listen on")
    args = parser.parse_args()

    print(f"Starting Player Agent MCP server on port {args.port}")
    uvicorn.run(app, host="localhost", port=args.port)
```

#### Step 0.3: Test Server Responds
**Terminal 1** - Start the server:
```bash
cd src/my_project/agents/player
python main.py --port 8101
```

**Terminal 2** - Test with curl:
```bash
# Test basic connectivity
curl -X POST http://localhost:8101/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"ping","id":1}'

# Test handle_game_invitation
curl -X POST http://localhost:8101/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"handle_game_invitation",
    "params":{
      "conversation_id":"test-001",
      "match_id":"R1M1"
    },
    "id":1
  }'

# Test choose_parity
curl -X POST http://localhost:8101/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "method":"choose_parity",
    "params":{
      "conversation_id":"test-001",
      "match_id":"R1M1"
    },
    "id":2
  }'
```

**Expected**: Server responds with JSON-RPC 2.0 formatted responses.

#### Step 0.4: Implement JSON-RPC 2.0 Response Format
Add helper function to `main.py`:

```python
def create_response(result, request_id=1):
    """Create JSON-RPC 2.0 compliant response"""
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }

def create_error_response(error_code, error_message, request_id=1):
    """Create JSON-RPC 2.0 error response"""
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": error_code,
            "message": error_message
        },
        "id": request_id
    }
```

#### Step 0.5: Deliverables Checklist
- [ ] HTTP server running on specified port (default 8101)
- [ ] `/mcp` endpoint accepting POST requests
- [ ] Basic routing to 3 tool handlers (stubs are okay for now)
- [ ] JSON-RPC 2.0 response format implemented
- [ ] Server can be tested with curl commands
- [ ] No crashes or errors on startup

**Once Phase 0 is complete**, you have the basic MCP server infrastructure. The actual game logic, strategy, and protocol compliance will be implemented in later phases.

---

### Phase 1: Understanding & Planning (Day 1)

#### Step 1.1: Read Assignment
- [ ] Read assignment description thoroughly (2-3 times)
- [ ] Highlight key requirements
- [ ] Identify deliverables
- [ ] Note any constraints or special requirements
- [ ] Fill in "Assignment-Specific Requirements" section in this file

#### Step 1.2: Fill Documentation Templates
- [ ] Update `docs/PRD.md`:
  - Project name, date, author
  - Executive summary (project overview, problem statement, target users)
  - Objectives and success metrics
  - Functional requirements with user stories
  - Non-functional requirements
  - Technical stack and dependencies
  - Timeline and milestones
  - Risks and mitigation

- [ ] Update `docs/ARCHITECTURE.md`:
  - Project name
  - System overview
  - Start planning building blocks
  - Identify where multiprocessing/multithreading might be needed

#### Step 1.3: Identify Building Blocks
- [ ] Draw system flow diagram
- [ ] Identify all major building blocks
- [ ] For each block, define:
  - Purpose and responsibility
  - Input data (parameters, types, valid ranges)
  - Output data (return values, types)
  - Setup/Configuration (parameters with defaults)
  - Dependencies on other blocks
- [ ] Document in `docs/ARCHITECTURE.md`

#### Step 1.4: Plan Parallel Processing
- [ ] Identify CPU-bound operations (computation-heavy)
  - Plan to use **multiprocessing** for these
  - Document in ARCHITECTURE.md
- [ ] Identify I/O-bound operations (network, disk, database)
  - Plan to use **multithreading** for these
  - Document in ARCHITECTURE.md

#### Step 1.5: Update Configuration
- [ ] Update `pyproject.toml`:
  - Project name
  - Version
  - Dependencies (with version numbers)
- [ ] Update `requirements.txt` with same dependencies
- [ ] Create `.env` from `.env.example`
- [ ] Update `config/config.yaml` with project-specific parameters

### Phase 2: Implementation (Days 2-4)

#### Step 2.1: Set Up Development Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import my_project; print(my_project.__version__)"
```

#### Step 2.2: Implement Core Building Blocks
For each building block:

1. **Create module file** in appropriate directory:
   ```python
   # src/my_project/core/building_block_name.py

   from typing import Any, Dict
   from pathlib import Path

   class BuildingBlockName:
       """
       Purpose: [What this building block does]

       Input Data:
           param1 (str): Description
           param2 (int): Description (1-100)

       Output Data:
           dict: {
               'result': ...,
               'status': 'success' or 'error'
           }

       Setup/Configuration:
           config1 (str): Configuration parameter (default: 'default')
           timeout (int): Timeout in seconds (default: 30)
       """

       def __init__(self, config1: str = "default", timeout: int = 30):
           """Initialize the building block."""
           self.config1 = config1
           self.timeout = timeout

       def process(self, param1: str, param2: int = 10) -> Dict[str, Any]:
           """
           Process the input data.

           Args:
               param1: Description
               param2: Description (default: 10, range: 1-100)

           Returns:
               Dictionary with result and status

           Raises:
               ValueError: If param2 is out of range
               TimeoutError: If operation times out
           """
           # Input validation
           if not 1 <= param2 <= 100:
               raise ValueError(f"param2 must be 1-100, got {param2}")

           # Implementation
           try:
               result = self._do_work(param1, param2)
               return {"result": result, "status": "success"}
           except Exception as e:
               return {"result": None, "status": "error", "error": str(e)}

       def _do_work(self, param1: str, param2: int):
           """Internal implementation."""
           # Your logic here
           pass
   ```

2. **Write unit tests** immediately:
   ```python
   # tests/unit/test_building_block_name.py

   import pytest
   from my_project.core.building_block_name import BuildingBlockName

   class TestBuildingBlockName:
       def test_normal_case(self):
           """Test with normal input."""
           block = BuildingBlockName()
           result = block.process("test", 50)
           assert result["status"] == "success"

       def test_edge_case_minimum(self):
           """Test with minimum param2."""
           block = BuildingBlockName()
           result = block.process("test", 1)
           assert result["status"] == "success"

       def test_edge_case_maximum(self):
           """Test with maximum param2."""
           block = BuildingBlockName()
           result = block.process("test", 100)
           assert result["status"] == "success"

       def test_invalid_param2_below_range(self):
           """Test with param2 below valid range."""
           block = BuildingBlockName()
           with pytest.raises(ValueError):
               block.process("test", 0)

       def test_invalid_param2_above_range(self):
           """Test with param2 above valid range."""
           block = BuildingBlockName()
           with pytest.raises(ValueError):
               block.process("test", 101)

       def test_empty_param1(self):
           """Test with empty string param1."""
           block = BuildingBlockName()
           result = block.process("", 50)
           # Assert expected behavior

       def test_custom_config(self):
           """Test with custom configuration."""
           block = BuildingBlockName(config1="custom", timeout=60)
           assert block.config1 == "custom"
           assert block.timeout == 60
   ```

3. **Run tests after each building block**:
   ```bash
   pytest tests/unit/test_building_block_name.py -v
   ```

#### Step 2.3: Implement Parallel Processing
If applicable:

**For CPU-bound operations (multiprocessing)**:
```python
# src/my_project/utils/parallel.py

from multiprocessing import Pool, cpu_count
from typing import List, Any

def process_in_parallel(data_list: List[Any], worker_func) -> List[Any]:
    """
    Process data in parallel using multiprocessing.

    Args:
        data_list: List of data items to process
        worker_func: Function to apply to each item

    Returns:
        List of results
    """
    num_processes = cpu_count()
    with Pool(processes=num_processes) as pool:
        results = pool.map(worker_func, data_list)
    return results
```

**For I/O-bound operations (multithreading)**:
```python
# src/my_project/utils/concurrent.py

from concurrent.futures import ThreadPoolExecutor
from typing import List, Any

def fetch_in_parallel(urls: List[str], fetch_func) -> List[Any]:
    """
    Fetch data concurrently using multithreading.

    Args:
        urls: List of URLs to fetch
        fetch_func: Function to fetch each URL

    Returns:
        List of results
    """
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_func, urls))
    return results
```

#### Step 2.4: Implement Integration Between Building Blocks
- [ ] Create main orchestrator that connects building blocks
- [ ] Handle data flow between blocks
- [ ] Implement error handling for entire pipeline
- [ ] Document in `docs/ARCHITECTURE.md` with sequence diagrams

#### Step 2.5: Configuration Management
- [ ] Load configuration from `config/config.yaml`
- [ ] Load environment variables from `.env`
- [ ] Example:
   ```python
   # src/my_project/config/settings.py

   from pathlib import Path
   import yaml
   import os
   from dotenv import load_dotenv

   # Load environment variables
   load_dotenv()

   # Get package root
   PACKAGE_ROOT = Path(__file__).parent.parent.parent
   CONFIG_FILE = PACKAGE_ROOT / "config" / "config.yaml"

   # Load config
   with open(CONFIG_FILE, 'r') as f:
       config = yaml.safe_load(f)

   # API keys from environment
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
   ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

   # Configuration values
   MODEL_NAME = config['model']['name']
   TEMPERATURE = config['model']['temperature']
   BATCH_SIZE = config['processing']['batch_size']
   ```

### Phase 3: Testing (Day 5)

#### Step 3.1: Write Comprehensive Tests
- [ ] Unit tests for all building blocks
- [ ] Integration tests for building block interactions
- [ ] Edge case tests (empty, None, invalid, boundary values)
- [ ] Error handling tests

#### Step 3.2: Achieve 70%+ Coverage
```bash
# Run tests with coverage
pytest tests/ --cov=src/my_project --cov-report=html --cov-report=term-missing

# Open coverage report
open htmlcov/index.html  # On macOS
# Or navigate to htmlcov/index.html in browser
```

- [ ] Review coverage report
- [ ] Write additional tests for uncovered lines
- [ ] Target: 70%+ coverage for new code

#### Step 3.3: Test Edge Cases
For each function/method, test:
- [ ] Empty input (`""`, `[]`, `{}`, `None`)
- [ ] Invalid types
- [ ] Boundary values (min, max, just below, just above)
- [ ] Large inputs
- [ ] Concurrent access (if applicable)

### Phase 4: Research & Analysis (Days 6-7)

#### Step 4.1: Parameter Exploration
- [ ] Identify key parameters to vary
- [ ] Design systematic experiments:
  - Parameter 1: Values [v1, v2, v3, ...]
  - Parameter 2: Values [v1, v2, v3, ...]
  - Combinations to test
- [ ] Run experiments and save results to `results/experiments/`
- [ ] Document results in table format

#### Step 4.2: Analysis Notebook
- [ ] Create `notebooks/analysis.ipynb`
- [ ] Document experiments with:
  - Introduction (research questions)
  - Methodology (how experiments were conducted)
  - Results (tables and visualizations)
  - Analysis (interpretation of results)
  - Conclusions (insights and recommendations)
- [ ] Add mathematical formulas in LaTeX if relevant
- [ ] Reference academic literature if applicable

#### Step 4.3: Visualizations
- [ ] Create high-quality visualizations:
  - Bar charts for comparisons
  - Line charts for trends
  - Heatmaps for parameter interactions
  - Confusion matrices (if applicable)
- [ ] Save to `results/visualizations/`
- [ ] High resolution (300+ DPI)
- [ ] Clear labels, legends, captions

### Phase 5: Documentation (Days 8-9)

#### Step 5.1: Complete Architecture Documentation
- [ ] Update `docs/ARCHITECTURE.md`:
  - C4 Model diagrams (Context, Container, Component)
  - UML sequence diagrams
  - Data flow diagrams
  - All building blocks documented
  - Parallel processing architecture
  - ADRs (Architecture Decision Records)
- [ ] Create diagrams in `assets/diagrams/`

#### Step 5.2: Complete API Documentation
- [ ] Generate API documentation from docstrings
- [ ] Create `docs/API_REFERENCE.md`
- [ ] Include all public classes, methods, functions
- [ ] Usage examples for each

#### Step 5.3: Write Comprehensive README
- [ ] Complete all sections:
  1. Project title and description
  2. Installation instructions (step-by-step)
  3. Usage instructions with examples
  4. Configuration guide
  5. Testing instructions
  6. Project structure
  7. Troubleshooting
  8. License
- [ ] Add screenshots/examples
- [ ] Test README by following it on a fresh machine/environment

#### Step 5.4: Document AI Prompts
- [ ] Create `docs/PROMPTS_BOOK.md`
- [ ] For each significant prompt:
  - Context (why this prompt was needed)
  - Full prompt text
  - Output received
  - Iterations made
  - Lessons learned
- [ ] Include best practices discovered

#### Step 5.5: Code Documentation
- [ ] Ensure all functions/classes have docstrings
- [ ] Add comments for complex logic
- [ ] Document design decisions in code
- [ ] Update `__init__.py` files with proper exports

### Phase 6: Quality Assurance & Polish (Day 10)

#### Step 6.1: Code Quality
- [ ] Run linter: `flake8 src/`
- [ ] Run formatter: `black src/ tests/`
- [ ] Check for unused imports
- [ ] Ensure consistent naming conventions
- [ ] Files under 150 lines

#### Step 6.2: Security Review
- [ ] No API keys in code
- [ ] All secrets in `.env`
- [ ] `.env` in `.gitignore`
- [ ] `.env.example` provided
- [ ] No hardcoded paths

#### Step 6.3: Package Verification
```bash
# Verify package can be installed
pip uninstall my_project -y
pip install -e .

# Verify imports work
python -c "from my_project import *; print('Success!')"

# Verify tests work
pytest tests/

# Verify entry points (if applicable)
my_project --help
```

#### Step 6.4: Review Against All Checklists
- [ ] Go through every checklist in this CLAUDE.md file
- [ ] Verify each item is complete
- [ ] Fix any gaps

### Phase 7: Self-Assessment (Final Day)

#### Step 7.1: Honest Self-Assessment
- [ ] Review `self-assessment-guide.pdf`
- [ ] For each criterion, assess honestly:
  - What grade do I deserve for this criterion?
  - Why? (provide justification)
  - Evidence (point to specific files/sections)
- [ ] Remember: Higher self-assessed grade = more thorough review
- [ ] Be conservative if uncertain

#### Step 7.2: Final Checklist
- [ ] All documentation complete and thorough
- [ ] All tests passing with 70%+ coverage
- [ ] Package installs and runs correctly
- [ ] No secrets committed
- [ ] All requirements met
- [ ] Self-assessment complete and honest

#### Step 7.3: Submission Preparation
- [ ] Final git commit
- [ ] Create submission archive (if required)
- [ ] Double-check submission includes all required files
- [ ] Submit before deadline

---

## Quality Assurance Checklist

### Before Submission
- [ ] All sections of PRD completed
- [ ] Architecture diagrams created and documented
- [ ] README is comprehensive with all sections
- [ ] Code has proper docstrings and comments
- [ ] Project organized as a proper Python package
- [ ] All tests passing with 70%+ coverage
- [ ] Edge cases documented and tested
- [ ] Analysis notebook complete with visualizations
- [ ] Multiprocessing/multithreading implemented correctly (if applicable)
- [ ] Building block design documented
- [ ] Configuration separated from code
- [ ] No API keys or secrets in code
- [ ] .gitignore updated
- [ ] All dependencies listed with versions
- [ ] Self-assessment completed honestly

### Self-Assessment Grade Expectation

Based on thoroughness of review:
- **90-100**: Meticulous search for every detail, "needle in haystack" approach
- **80-89**: Thorough review of ALL criteria, no exceptions
- **70-79**: Reasonable review of main criteria
- **60-69**: Flexible review, if reasoning exists

---

## Important Notes

### Contract-Based Grading
The higher the self-assessed grade, the more thorough the review will be. A grade of 90-100 means every tiny detail will be scrutinized.

### Integrated Evaluation
This is a holistic evaluation combining both academic excellence and technical engineering skills. The goal is to develop students into practical software engineers alongside theoretical research capabilities.

### New Technical Requirements (Version 2.0)
The three new chapters (13-15) focus on deep technical inspection:
1. **Package organization**: Professional Python package structure
2. **Parallel processing**: Correct use of multiprocessing/multithreading
3. **Building blocks**: Modular architecture with clear separation of concerns

These are NOT optional - they are critical for achieving high grades.

---

## Prompts Book Requirement

Document ALL significant prompts used with AI throughout project:
- Prompt for each component
- Context and reason for the prompt
- Examples of outputs received
- Iterative improvements over time
- Best practices learned from experience

---

## Cost Analysis (if using AI APIs)

Document token usage by:
- Detailed token count (input/output) per model
- Cost breakdown by service
- Total cost calculation
- Optimization strategies

---

## Remember

> **This self-assessment is accurate and methodical - it is a sign of academic and professional maturity.**

Your work will be evaluated with the same level of scrutiny you claim in your self-assessment. Be honest, thorough, and set realistic expectations.

---

## Common Pitfalls to Avoid

**Reference**: Based on common mistakes in submissions

### Package Organization (Chapter 13)
- **DON'T**: Use absolute paths like `/Users/username/project/`
- **DO**: Use relative paths with `pathlib.Path(__file__).parent`

- **DON'T**: Forget `__init__.py` files
- **DO**: Add `__init__.py` to every package directory with proper exports

- **DON'T**: Import with `sys.path.append()`
- **DO**: Use relative imports `from .module import function`

- **DON'T**: Forget version numbers in dependencies
- **DO**: Specify `package>=1.0.0` in pyproject.toml

### Multiprocessing/Multithreading (Chapter 14)
- **DON'T**: Use multiprocessing for I/O operations (API calls, file reading)
- **DO**: Use multithreading for I/O, multiprocessing for CPU-heavy tasks

- **DON'T**: Forget to close processes/threads
- **DO**: Use context managers (`with Pool() as pool:`)

- **DON'T**: Share mutable state between processes without synchronization
- **DO**: Use queues or manager objects for inter-process communication

### Building Blocks (Chapter 15)
- **DON'T**: Create building blocks without clear Input/Output/Setup documentation
- **DO**: Document each building block completely in ARCHITECTURE.md

- **DON'T**: Mix responsibilities in one building block
- **DO**: Follow Single Responsibility Principle

- **DON'T**: Hardcode configuration in building blocks
- **DO**: Use Setup data with defaults

### Testing (Chapter 5)
- **DON'T**: Only test happy paths
- **DO**: Test edge cases (empty, None, invalid, boundaries)

- **DON'T**: Forget to check coverage
- **DO**: Run `pytest --cov` and aim for 70%+

- **DON'T**: Write tests that depend on each other
- **DO**: Make each test independent

### Documentation (Chapters 1-2)
- **DON'T**: Write README after implementation is done
- **DO**: Update documentation as you go

- **DON'T**: Skip docstrings "to save time"
- **DO**: Write docstrings while writing the code

- **DON'T**: Use vague commit messages like "fixed stuff"
- **DO**: Write clear, descriptive messages

### Security (Chapter 4)
- **DON'T**: Commit `.env` file to git
- **DO**: Only commit `.env.example` and add `.env` to `.gitignore`

- **DON'T**: Put API keys in code "just for testing"
- **DO**: Always use environment variables

### Research & Analysis (Chapter 6)
- **DON'T**: Run experiments without systematic approach
- **DO**: Design experiments with clear parameter variations

- **DON'T**: Create visualizations without labels/legends
- **DO**: Make graphs publication-quality with clear captions

### MCP Protocol Implementation (Even/Odd League Assignment)

#### Timestamp Errors
**❌ WRONG:**
```python
from datetime import datetime
timestamp = datetime.now().isoformat()  # Local timezone!
timestamp = "2025-01-15T10:30:00+02:00"  # Not UTC!
timestamp = "2025-01-15T10:30:00"  # No timezone indicator!
```

**✅ CORRECT:**
```python
from datetime import datetime
timestamp = datetime.utcnow().isoformat() + "Z"  # "2025-01-15T10:30:00.123456Z"
```

#### Parity Choice Errors
**❌ WRONG:**
```python
return {"parity_choice": "Even"}  # Capital E!
return {"parity_choice": "ODD"}   # All caps!
return {"parity_choice": 0}       # Number instead of string!
```

**✅ CORRECT:**
```python
return {"parity_choice": "even"}  # lowercase only
return {"parity_choice": "odd"}   # lowercase only
```

#### Auth Token Errors
**❌ WRONG:**
```python
# Forgetting to save token after registration
response = register_to_league()
# ... token is lost!

# Not including token in subsequent messages
params = {
    "message_type": "CHOOSE_PARITY_RESPONSE",
    "parity_choice": "even"
    # Missing auth_token!
}
```

**✅ CORRECT:**
```python
# Save token from registration
response = register_to_league()
self.auth_token = response["result"]["auth_token"]

# Include in all messages after registration
params = {
    "protocol": "league.v2",
    "message_type": "CHOOSE_PARITY_RESPONSE",
    "sender": f"player:{self.player_id}",
    "auth_token": self.auth_token,  # ← Critical!
    "parity_choice": "even"
}
```

#### Timeout Violations
**❌ WRONG:**
```python
def choose_parity(params):
    # Expensive LLM call that takes 45 seconds
    result = llm_api.generate(prompt)  # TIMEOUT!
    return {"parity_choice": result}
```

**✅ CORRECT:**
```python
import asyncio

async def choose_parity(params):
    # Set timeout for LLM call
    try:
        result = await asyncio.wait_for(
            llm_api.generate_async(prompt),
            timeout=25  # Leave 5s buffer from 30s limit
        )
        return {"parity_choice": result}
    except asyncio.TimeoutError:
        # Fallback to quick strategy
        import random
        return {"parity_choice": random.choice(["even", "odd"])}
```

#### JSON Structure Errors
**❌ WRONG:**
```python
# Missing required fields
return {
    "message_type": "GAME_JOIN_ACK",
    "accept": True
    # Missing: protocol, sender, timestamp, conversation_id, match_id, player_id, arrival_timestamp!
}

# Wrong field names
return {
    "msg_type": "GAME_JOIN_ACK",  # Should be message_type
    "player": "P01",               # Should be player_id
}
```

**✅ CORRECT:**
```python
from datetime import datetime

return {
    "protocol": "league.v2",
    "message_type": "GAME_JOIN_ACK",
    "sender": f"player:{self.player_id}",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "conversation_id": params["conversation_id"],  # Echo from invitation
    "auth_token": self.auth_token,
    "match_id": params["match_id"],
    "player_id": self.player_id,
    "arrival_timestamp": datetime.utcnow().isoformat() + "Z",
    "accept": True
}
```

---

## Quick Reference Table

**Where to find/implement each requirement:**

| Requirement | Chapter | Grade % | File/Directory | Details |
|------------|---------|---------|----------------|---------|
| **Product Requirements** | 1 | 20% | `docs/PRD.md` | Executive summary, objectives, requirements, timeline |
| **Architecture Docs** | 1 | 20% | `docs/ARCHITECTURE.md` | C4 diagrams, UML, building blocks, data flow |
| **README** | 2 | 15% | `README.md` | Installation, usage, config, troubleshooting |
| **Code Docstrings** | 2 | 15% | All `.py` files | Every function/class with docstring |
| **API Documentation** | 2 | 15% | `docs/API_REFERENCE.md` | All public interfaces |
| **Project Structure** | 3 | 15% | Root directory | src/, tests/, docs/, data/, results/ |
| **Modular Code** | 3 | 15% | `src/my_project/` | Files <150 lines, clear separation |
| **Configuration Files** | 4 | 10% | `config/`, `.env.example` | Separate config from code |
| **Security** | 4 | 10% | `.env`, `.gitignore` | No secrets in code |
| **Unit Tests** | 5 | 15% | `tests/unit/` | 70%+ coverage |
| **Edge Case Tests** | 5 | 15% | `tests/unit/` | Empty, None, invalid, boundary |
| **Error Handling** | 5 | 15% | All `.py` files | Try/except, clear error messages |
| **Parameter Exploration** | 6 | 15% | `results/experiments/` | Systematic experiments |
| **Analysis Notebook** | 6 | 15% | `notebooks/analysis.ipynb` | Full analysis with insights |
| **Visualizations** | 6 | 15% | `results/visualizations/` | High-quality graphs |
| **User Interface** | 7 | 10% | Main entry point | CLI/GUI with clear workflow |
| **Extensibility** | 7 | 10% | Architecture | Plugin system, hooks |
| **Package Definition** | 13 | 40% | `pyproject.toml` | Name, version, dependencies |
| **__init__.py Files** | 13 | 40% | All package dirs | With __version__ and exports |
| **Relative Paths** | 13 | 40% | All `.py` files | No absolute paths |
| **Multiprocessing** | 14 | 40% | `src/my_project/utils/` | For CPU-bound operations |
| **Multithreading** | 14 | 40% | `src/my_project/utils/` | For I/O-bound operations |
| **Building Blocks** | 15 | 40% | `docs/ARCHITECTURE.md` | Input/Output/Setup documented |
| **Building Block Code** | 15 | 40% | `src/my_project/core/` | Classes with clear responsibilities |
| **Prompts Book** | Special | - | `docs/PROMPTS_BOOK.md` | All AI prompts documented |
| **Self-Assessment** | Special | - | Submission form | Honest evaluation |
| **MCP Server** | HW7 | - | `agents/player/main.py` | HTTP server, /mcp endpoint, JSON-RPC 2.0 |
| **Player Tools** | HW7 | - | `agents/player/handlers.py` | 3 tools: handle_game_invitation, choose_parity, notify_match_result |
| **Strategy Module** | HW7 | - | `agents/player/strategy.py` | Random/History/LLM-based strategy |
| **Protocol Compliance** | HW7 | - | All agent files | UTC timestamps, lowercase parity, auth_token, timeouts |

---

## Tips for Achieving 100/100

1. **Start with Documentation**: Write PRD and ARCHITECTURE first, then implement
2. **Write Tests Immediately**: Don't wait until the end - write tests as you code
3. **Use Checklists**: Go through every checklist in this file multiple times
4. **Be Honest in Self-Assessment**: Don't claim 95 if you're unsure - the review will be more thorough
5. **Focus on Building Blocks**: This is NEW in Version 2.0 - give it proper attention
6. **Get Parallel Processing Right**: Understand CPU-bound vs I/O-bound difference
7. **Document Everything**: Code, decisions, experiments, prompts - document it all
8. **Quality Over Quantity**: Better to have fewer features done perfectly than many done poorly
9. **Test Edge Cases**: Empty, None, invalid - test everything that could go wrong
10. **Review Before Submitting**: Take a break, come back fresh, review against all criteria

---

## Final Pre-Submission Checklist

**Print this and check off each item before submitting:**

### Package Organization (Chapter 13 - 40% weight)
- [ ] `pyproject.toml` exists with name, version, dependencies with version numbers
- [ ] `__init__.py` in all package directories
- [ ] `__version__` defined in main `__init__.py`
- [ ] Public interfaces exported in `__all__`
- [ ] All imports use relative paths (no `sys.path.append`)
- [ ] All file operations use relative paths (no hardcoded absolute paths)
- [ ] Package installs with `pip install -e .`

### Multiprocessing/Multithreading (Chapter 14 - 40% weight)
- [ ] Identified CPU-bound operations → using multiprocessing
- [ ] Identified I/O-bound operations → using multithreading
- [ ] Number of processes based on `cpu_count()`
- [ ] Proper process/thread cleanup (context managers)
- [ ] No race conditions or deadlocks
- [ ] Documented in ARCHITECTURE.md

### Building Blocks (Chapter 15 - 40% weight)
- [ ] All building blocks identified and documented in ARCHITECTURE.md
- [ ] Each block has Input Data documented (parameters, types, ranges)
- [ ] Each block has Output Data documented (return values, types)
- [ ] Each block has Setup/Configuration documented (parameters with defaults)
- [ ] Each block follows Single Responsibility Principle
- [ ] Building blocks tested independently
- [ ] Example usage provided for each block

### Documentation (20%)
- [ ] PRD.md complete with all sections
- [ ] ARCHITECTURE.md complete with diagrams
- [ ] README.md comprehensive and tested
- [ ] API_REFERENCE.md generated from docstrings
- [ ] PROMPTS_BOOK.md documents all AI usage

### Code Quality (15%)
- [ ] All functions/classes have docstrings
- [ ] Files under 150 lines
- [ ] Consistent naming conventions
- [ ] No duplicate code
- [ ] Code formatted (`black src/ tests/`)
- [ ] No linter errors (`flake8 src/`)

### Security (10%)
- [ ] No API keys in code
- [ ] `.env` in `.gitignore`
- [ ] `.env.example` provided
- [ ] No secrets committed to git

### Testing (15%)
- [ ] All tests passing (`pytest tests/`)
- [ ] 70%+ coverage (`pytest --cov`)
- [ ] Edge cases tested
- [ ] Error handling tested
- [ ] Coverage report generated

### Research & Analysis (15%)
- [ ] Parameter exploration completed
- [ ] Analysis notebook complete
- [ ] High-quality visualizations created
- [ ] Results documented

### Self-Assessment
- [ ] Reviewed against all criteria
- [ ] Honest evaluation (not inflated)
- [ ] Evidence provided for each claim
- [ ] Conservative if uncertain

### MCP Protocol Compliance (Even/Odd League Assignment)
- [ ] Player agent runs HTTP server on specified port
- [ ] `/mcp` endpoint accepts POST requests
- [ ] All 3 tools implemented correctly:
  - [ ] `handle_game_invitation` → returns GAME_JOIN_ACK
  - [ ] `choose_parity` → returns CHOOSE_PARITY_RESPONSE
  - [ ] `notify_match_result` → updates internal state and acknowledges
- [ ] Response timeouts respected:
  - [ ] GAME_JOIN_ACK within 5 seconds
  - [ ] CHOOSE_PARITY_RESPONSE within 30 seconds
  - [ ] All other responses within 10 seconds
- [ ] All timestamps in UTC/GMT (ISO-8601 format with 'Z' suffix)
- [ ] parity_choice is lowercase: "even" or "odd" (NEVER "Even" or "ODD")
- [ ] auth_token included in all messages after registration
- [ ] JSON structures match Chapter 4 examples exactly
- [ ] Message envelope contains all required fields:
  - [ ] protocol: "league.v2"
  - [ ] message_type (correct value for each message)
  - [ ] sender (format: "player:P01")
  - [ ] timestamp (UTC with 'Z')
  - [ ] conversation_id (echoed from incoming message)
- [ ] Successfully registered to League Manager (received player_id and auth_token)
- [ ] Tested in local league with 4 player copies
- [ ] All matches complete without crashes or timeouts
- [ ] Compatible with other students' agents (if tested)
- [ ] State management working (tracks wins/losses/draws correctly)
- [ ] Error handling for all edge cases:
  - [ ] Network errors (connection refused, timeouts)
  - [ ] Malformed messages (missing fields, wrong types)
  - [ ] Timeout scenarios (fallback strategies implemented)
  - [ ] Invalid game states

### Even/Odd League Submission
- [ ] Source code of Player Agent submitted
- [ ] README with installation and running instructions
- [ ] README includes:
  - [ ] Dependencies installation (`pip install -r requirements.txt` or `pip install -e .`)
  - [ ] How to start agent (`python main.py --port 8101`)
  - [ ] Configuration options (display name, strategy type, etc.)
  - [ ] Example usage with curl or test commands
- [ ] Detailed report written including:
  - [ ] Full architecture and implementation description
  - [ ] Strategy choice and rationale (random/history/LLM)
  - [ ] Difficulties encountered and solutions found
  - [ ] Development and testing process documentation
  - [ ] Conclusions and recommendations for improvement
- [ ] Link to public repository provided
- [ ] Manual report submitted to exercises checker
- [ ] Agent tested and verified working before submission

---

**Document Version**: 2.0
**Based on**: Dr. Yoram Segal's Guidelines for Submitting Excellent Software
**Last Updated**: [Current Date]
