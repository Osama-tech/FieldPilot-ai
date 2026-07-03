# FieldPilot AI — Architecture Document

**Status:** Phase 0 Complete — Requirements & Architecture Locked
**Target role reference:** AI Systems Engineer @ Precision AI (agentic AI, tool calling, production deployment, agriculture domain)

---

## 1. Vision

FieldPilot AI is a production-shaped AI Operations Assistant for agriculture. It is not a chatbot — it is an agent that orchestrates tools, data sources, and rules to produce an explainable operational recommendation.

**MVP use case:** *"Is it safe to spray Field X today?"*

The agent gathers weather, field, and chemical inputs, applies safety rules, and returns a structured, justified recommendation.

---

## 2. Functional Requirements

| Requirement | Detail |
|---|---|
| Primary decision | Spray recommendation: `Safe` / `Not Safe` / `Conditional` |
| Inputs | Weather (wind, precipitation, temperature), field size, spray rate/chemical type, crop/field context |
| Rules source | Safety rules (e.g. wind thresholds) — MVP uses a config file, designed to be swapped for RAG later without touching business logic |
| Output | Structured object: `decision`, `reasoning`, `contributing_factors` — not free-form text, because a real product needs to render this in a UI |

---

## 3. Non-Functional Requirements

| NFR | Decision | Rationale |
|---|---|---|
| Response mode | Synchronous | Simplest for MVP; service layer returns a complete result so streaming can be added later at the API layer only, without touching core logic |
| Users / Auth | Single user, no auth | YAGNI — building multi-tenancy/auth for a solo demo project is effort spent on a problem that doesn't exist yet |
| Cost/token tracking | Capture raw data (tokens, latency, tool calls) opportunistically in the logging layer only if it fits naturally — no dedicated cost-tracking feature in MVP | Raw data is cheap to capture now and can't be reconstructed retroactively; analysis on top of it is deferred because it's expensive and not needed yet |
| Rule extensibility | Rules live behind a `RuleProvider` abstraction, not hardcoded in tool logic | Allows swapping config-file rules for RAG-based retrieval later without modifying the Risk Assessment tool |

---

## 4. Architecture Style

**Chosen: Practical layered architecture (5 layers, informal boundaries) — not full Clean/Hexagonal Architecture, not a flat 2-layer app.**

- A flat structure (API + everything mixed) leads to a "God Object" pattern: the endpoint ends up calling the LLM, computing risk, and reading config directly. This breaks testability and makes every change touch everything.
- Full Clean Architecture (explicit entities/use-cases/interface-adapters with formal ports) is over-engineering for a single-user MVP with one real implementation per abstraction.
- The middle ground — clear layer responsibilities and a strict dependency direction, without ceremony — matches the actual size of the problem.

### Dependency Direction (core rule)

Higher layers may depend on lower layers. Lower layers must never depend on higher layers.

```
API → Agent → Tools → Domain
Infrastructure is depended upon (via abstractions) by Agent/Tools/Domain, never the reverse.
```

**Consequence:** the Domain layer contains zero imports of FastAPI, OpenAI/Anthropic SDKs, or any framework. It is pure business/data logic.

---

## 5. Layer Responsibilities

### API Layer (`app/api/`)
- **Owns:** HTTP request/response handling, input validation, status codes.
- **Must not own:** business logic, direct LLM calls, tool internals.
- **Test:** if FastAPI were swapped for a CLI, business logic should be unaffected.
- Example: `api/routes.py` — `POST /spray-decision` calls the Agent layer and returns its result as-is.

### Agent / Orchestration Layer (`app/agent/`)
- **Owns:** deciding which tools to call, in what order, and assembling the final recommendation.
- **Must not own:** tool internals, direct calls to a specific LLM SDK (uses the `LLMClient` abstraction instead).
- **Test:** adding a new tool should only require registering it — not rewriting decision logic.
- Example: `agent/orchestrator.py` — `decide_spray_recommendation()`.

### Tools Layer (`app/tools/`)
- **Owns:** actual execution — calculations, external API calls, rule application.
- **Must not own:** the decision of *when* to use a tool (that's the Agent's job).
- All tools share one interface (`execute(input) -> ToolResult`) so the Agent can treat them generically.
- Example: `tools/risk_assessment_tool.py` uses `RuleProvider` to fetch current safety thresholds.

### Domain Layer (`app/domain/`)
- **Owns:** data models (`Field`, `WeatherData`, `SprayRecommendation`) and abstractions like `RuleProvider`.
- **Must not own:** anything technical/external — no FastAPI, no HTTP, no SDKs.
- Example: `domain/models.py`, `domain/rule_provider.py` (abstract interface only).

### Infrastructure Layer (`app/infrastructure/`)
- **Owns:** all external-world communication — LLM client, weather API client, config loading, logging.
- **Must not own:** business decisions, knowledge of Agent/API layers.
- Example: `infrastructure/llm_client.py` (`LLMClient` abstract + `OpenAILLMClient` implementation), `infrastructure/config_rule_provider.py` (concrete `RuleProvider` reading YAML — the piece that gets swapped for RAG later).

---

## 6. Key Architectural Decisions (ADR-style)

**Decision: `RuleProvider` abstraction for safety rules**
Rules are read through an interface, not hardcoded inside the Risk Assessment tool. MVP implementation reads from `config/safety_rules.yaml`. This is the designed seam for the future RAG upgrade — swapping the implementation should require zero changes to the Tools or Agent layers.

**Decision: `LLMClient` abstraction in Infrastructure**
The Agent layer depends on an `LLMClient` interface, never directly on the OpenAI or Anthropic SDK. If the provider changes, most changes stay in `infrastructure/llm_client.py`. Note: if a new provider has materially different tool-calling behavior, minimal *parsing/normalization* changes may leak into the Agent layer — the abstraction reduces blast radius, it does not guarantee zero change.

**Decision: No dedicated `services/` layer**
The Agent layer already serves as the orchestration/service layer. Adding a separate `services/` layer on top would be indirection without a distinct responsibility.

**Decision: No `exceptions.py` yet**
Not enough distinct error-handling cases exist yet to justify a custom exception hierarchy. Rule of three: introduce it once the same error-handling logic is duplicated three times.

**Decision: No auth, no multi-user support**
Single-user demo/interview project — building this now would be effort spent on a non-existent requirement (YAGNI).

---

## 7. Folder Structure

```
fieldpilot-ai/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── agent/
│   │   ├── orchestrator.py
│   │   └── tool_registry.py
│   ├── tools/
│   │   ├── base.py
│   │   ├── weather_tool.py
│   │   ├── calculator_tool.py
│   │   └── risk_assessment_tool.py
│   ├── domain/
│   │   ├── models.py
│   │   └── rule_provider.py
│   └── infrastructure/
│       ├── llm_client.py
│       ├── weather_api_client.py
│       ├── config_rule_provider.py
│       ├── config.py
│       └── logging_setup.py
├── config/
│   └── safety_rules.yaml
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 8. MVP Success Criteria (Definition of Done)

| # | Criterion | Verification (not just "runs") |
|---|---|---|
| 1 | FastAPI app runs locally | `uvicorn` starts without errors |
| 2 | `/health` works | Returns 200 + status payload |
| 3 | `/spray-decision` accepts structured input | Rejects invalid input with 422 |
| 4 | Orchestrator calls the needed tools | Trace/log confirms all 3 tools were actually invoked |
| 5 | Weather, Calculator, Risk tools work | Each has a unit test proving correct output for a known input |
| 6 | Rules come from `safety_rules.yaml` | Changing a value in the YAML changes the outcome — proves `RuleProvider` isn't hardcoded |
| 7 | Returns Safe / Not Safe / Conditional | At least one test scenario produces each of the three outcomes |
| 8 | Unit tests pass | Plus one end-to-end integration test (full request → response) |
| 9 | README explains architecture + how to run | Includes the layer diagram and rationale for each architectural decision |

---

## 9. Technology Stack (Finalized)

| Component | Choice | Rationale |
|---|---|---|
| LLM Provider | Gemini 2.5 Flash (`google-genai` SDK) | Free tier supports function calling + structured outputs (verified July 2026); cost-optimized for learning. **Trade-off accepted:** free-tier prompts/responses may be used by Google to improve their products — acceptable for this non-sensitive demo project, not appropriate for production data. Isolated behind `LLMClient` so the provider can change with minimal blast radius. |
| Package manager | `uv` | Fast, unifies venv + dependency management, current industry direction (2025–2026) |
| Web framework | FastAPI | Async-native, Pydantic-integrated, industry standard for Python AI services |
| HTTP client | `httpx` | Async-compatible (unlike `requests`), required so external calls don't block the event loop |
| Config management | `pydantic-settings` | Validates env vars as a typed Pydantic model, consistent with the rest of the stack |
| Testing | `pytest` + `pytest-asyncio` | De facto Python standard, async test support |
| Logging | Python standard `logging`, wrapped in a single `log_event()` helper | Simplest option for MVP; the wrapper is the seam that allows upgrading to `structlog` later by changing one file |
| Rules storage | `PyYAML`, read through `RuleProvider` | No real alternative needed for a simple config format |
| Weather data | Open-Meteo (`https://api.open-meteo.com`) | No API key required, 10,000 free requests/day, exposes agriculture-relevant data (soil temperature/moisture) beyond basic conditions. CC BY 4.0 — requires attribution in README |
| Agent loop (MVP) | Native function-calling loop, no framework | LangGraph is deferred to Phase 3 by design; understanding the raw tool-calling loop first means Phase 3 teaches *what LangGraph adds*, rather than being used as a black box |

---

## 10. Explicitly Out of Scope for MVP

- RAG / vector store / agriculture manuals (Phase 2)
- LangGraph / multi-step planning / memory (Phase 3)
- Evaluation framework, monitoring, Docker, CI/CD (Phase 4)
- Streaming responses, auth, cost-tracking dashboards

These are deferred, not forgotten — each has a designed seam (`RuleProvider`, `LLMClient`, layer boundaries) so they can be added without rewriting the MVP.