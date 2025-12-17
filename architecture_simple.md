# Simplified Architecture Diagram for Miro/Draw.io

This is a simplified version of the architecture diagram optimized for importing into Miro or Draw.io.

## Component List

### Layer 1: External Integrations
- WhatsApp Cloud API
- Telegram Bot API
- Other Integrations (extensible)

### Layer 2: API Gateway
- FastAPI Server
- Webhook Endpoints
- Route Handlers
- Integration Services

### Layer 3: Orchestration
- LangGraph State Graph
- Router Agent
- Checkpoint Manager

### Layer 4: Agents (Pydantic AI)
- Router Agent
- Lead Qualification Agent
- Property Search Agent
- Property Details Agent
- Scheduling Agent
- Market Analysis Agent
- FAQ Agent
- General Agent

### Layer 5: Tools
- Property Tools (search, details, estimation, similar)
- Scheduling Tools (schedule, slots, cancel, appointments)
- Market Tools (mortgage, trends, compare)
- Custom Tools

### Layer 6: Memory & Storage
- Supabase PostgreSQL (Long-term Memory)
- Milvus / Supabase PGVector (Vector DB)
- In-Memory Cache (Session State)

### Layer 7: Knowledge Base
- Vector Embeddings
- RAG Retrieval System
- Document Store

### Layer 8: LLM Services
- OpenAI GPT-4o-mini
- Embedding API

### Layer 9: Monitoring
- Logfire
- OpenTelemetry
- Metrics

## Connection Map

### Primary Flow
1. External → API Gateway → Orchestration → Agents
2. Agents → LLM Services
3. Agents → Tools
4. Agents → Knowledge Base (via RAG)
5. Orchestration → Memory & Storage
6. Agents → Memory & Storage
7. All Layers → Monitoring

### Specific Connections

**External to API:**
- WhatsApp → Webhook Endpoints
- Telegram → Webhook Endpoints
- Other → Webhook Endpoints

**API to Orchestration:**
- Webhook → Routes → Services → State Graph

**Orchestration to Agents:**
- State Graph → Router Agent
- Router Agent → All 7 Specialized Agents

**Agents to LLM:**
- All Agents → OpenAI GPT-4o-mini
- FAQ Agent → Embedding API (for RAG)

**Agents to Tools:**
- Lead/Search/Details Agents → Property Tools
- Schedule Agent → Scheduling Tools
- Market Agent → Market Tools
- FAQ Agent → RAG Retrieval

**Orchestration to Memory:**
- State Graph → Checkpoint Manager → PostgreSQL
- Checkpoint Manager → In-Memory Cache

**Knowledge Base:**
- RAG Retrieval → Vector DB
- RAG Retrieval → Embeddings
- Embeddings → Embedding API
- Vector DB → Document Store

**Monitoring:**
- All Agents → Logfire
- State Graph → OpenTelemetry
- API → Metrics
- Tools → Logfire

## Color Coding Suggestions

- **External Integrations**: Light Blue (#E1F5FF)
- **API Gateway**: Light Orange (#FFF3E0)
- **Orchestration**: Light Purple (#F3E5F5)
- **Agents**: Light Green (#E8F5E9)
- **Tools**: Light Yellow (#FFF9C4)
- **Memory**: Light Teal (#E0F2F1)
- **Knowledge Base**: Light Pink (#FCE4EC)
- **LLM**: Light Blue (#E3F2FD)
- **Monitoring**: Light Lime (#F1F8E9)

## Layout Suggestions for Miro/Draw.io

### Horizontal Layers (Top to Bottom):
1. External Integrations (top)
2. API Gateway
3. Orchestration
4. Agents (wide horizontal row)
5. Tools (below agents)
6. Memory & Storage (left side)
7. Knowledge Base (right side)
8. LLM Services (center bottom)
9. Monitoring (bottom, spanning all)

### Alternative: Vertical Zones
- **Left**: External → API → Orchestration
- **Center**: Agents (vertical stack)
- **Right**: Tools, Memory, Knowledge Base
- **Bottom**: LLM Services
- **Peripheral**: Monitoring (around edges)

