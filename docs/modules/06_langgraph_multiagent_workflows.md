# Module 06: Subproject II — Autonomous Multi-Agent Workflows with LangGraph

## Objectives
Design and implement a production-grade, stateful multi-agent system using LangGraph. Implement cyclic execution graphs, PostgreSQL checkpoint persistence, multi-agent collaboration, and a Human-in-the-Loop (HITL) approval gate for enterprise automation.

---

## Subproject Scope & Architecture

```text
                     ┌───────────────────────┐
                     │ Incident Alert Ingest │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  Log & Telemetry Node │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Diagnostic Agent Node │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │ Planner & Patch Node  │
                     └───────────┬───────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
             ──────> │   [HUMAN-IN-THE-LOOP] │ <──────
            │        │  Approval Breakpoint  │        │
            │        └───────────┬───────────┘        │
    (Amend / Feedback)           │                    │ (Reject)
            │                    ▼ (Approved)         │
            │        ┌───────────────────────┐        │
            └─────── │ Execution Node (Patch)│        │
                     └───────────┬───────────┘        │
                                 │                    │
                                 ▼                    │
                     ┌───────────────────────┐        │
                     │ Health Check / Verify │ ───────┘
                     └───────────┬───────────┘
                                 │ (Passed)
                                 ▼
                            [RESOLVED]
```

---

## Core Topics
1. **LangGraph State Graph Mechanics:**
   - Defining workflow state using Pydantic models or `TypedDict` with custom channel reducers (`operator.add`, custom merge logic).
   - Graph components: Nodes (execution logic), Edges (deterministic routing), and Conditional Edges (dynamic LLM decision branching).
   - Building cyclic loops for critique, self-correction, and error recovery.
2. **State Persistence & Thread Checkpointing:**
   - Durable checkpointing using `PostgresSaver` to persist graph state across execution pauses and service restarts.
   - Managing multi-tenant conversations and operations via unique `thread_id` configurations.
   - Time-travel debugging: Inspecting historical checkpoints and re-executing graphs from previous states.
3. **Human-in-the-Loop (HITL) Engineering:**
   - Configuring static and dynamic breakpoints (`interrupt_before`, `interrupt_after`).
   - Exposing state review and human approval endpoints over a REST API.
   - State updating: Enabling human engineers to edit proposed plans before the agent continues execution.
4. **Multi-Agent Collaboration Patterns:**
   - Supervisor Pattern: Central orchestrator routing subtasks to specialized sub-agents.
   - Tool-calling agents with strict schema validation and error feedback loops.
5. **Deterministic Testing of Agentic Workflows:**
   - Unit testing individual graph nodes with mock LLM outputs.
   - Integration testing graph state transitions using recorded checkpoint states.

---

## Planned Directory Structure
```text
Module_06_LangGraph_MultiAgent_Workflows_Subproject/
├── README.md
├── pyproject.toml
├── src/
│   └── incident_agent/
│       ├── __init__.py
│       ├── main.py              # API server for triggering workflows & human approval
│       ├── state.py             # LangGraph State definition & channel reducers
│       ├── nodes/               # Specialized agent nodes (diagnose, plan, execute, verify)
│       ├── edges/               # Routing and conditional branching logic
│       ├── tools/               # Agent tools (log fetcher, metric query, script runner)
│       └── checkpoint.py        # PostgreSQL checkpoint persistence setup
└── tests/
    ├── test_state_transitions.py
    ├── test_agent_nodes.py
    └── test_hitl_approval.py
```

---

## Verification Criteria
- [ ] Graph execution safely halts at the Human-in-the-Loop approval gate.
- [ ] State is persistently saved in PostgreSQL and can survive application restarts.
- [ ] Human approval or modification via API resumes execution cleanly.
- [ ] Automated regression tests verify all conditional edge routing paths.
