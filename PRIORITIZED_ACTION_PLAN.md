# 🎯 PRIORITIZED ACTION PLAN
## Smart Student Onboarding Agent — Implementation Roadmap

**Created:** May 13, 2026  
**Status:** Ready for Development  
**Total Estimated Time:** 30 hours  
**Priority:** 🔴 IMMEDIATE

---

## QUICK START PRIORITY

### DO THESE FIRST (These block everything else)

```
PRIORITY 1: Fix Application Startup Failures
PRIORITY 2: Fix Runtime Type Errors  
PRIORITY 3: Fix Database Connection
PRIORITY 4: Fix Core Agent Functionality
PRIORITY 5: Fix Data Persistence
```

---

## PHASE 1: CRITICAL FIXES (4-6 hours)

### ACTION 1.1: Create Missing Document Verification Agent

**Status:** 🔴 BLOCKING STARTUP  
**Severity:** CRITICAL  
**Files to Create:**
- `backend/app/agents/document_verification_agent.py`

**Specification:**

```python
# File: backend/app/agents/document_verification_agent.py
# Purpose: Process and verify student documents

Module should contain:
1. document_verification_node(state: AgentState) -> dict
   - Takes user_message and uploaded document reference
   - Uses OCR service to extract text
   - Validates document requirements
   - Returns verification result or request for reupload
   
2. _validate_document_requirements(doc_type: str, doc_text: str) -> dict
   - Check document meets requirements
   - Extract key information
   - Return validation status
   
3. _check_missing_info(required_fields: list, found_fields: dict) -> list
   - Compare required vs extracted fields
   - Return list of missing fields
```

**Tasks:**
- [ ] Create file with document verification logic
- [ ] Implement OCR integration
- [ ] Add validation rules
- [ ] Handle errors properly
- [ ] Return proper state updates
- [ ] Test with sample documents

**Effort:** 2 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ File exists at correct path
- ✅ Can be imported without errors
- ✅ Agent node signature matches other agents
- ✅ Returns proper state updates

---

### ACTION 1.2: Fix AgentState Initialization

**Status:** 🔴 BLOCKING RUNTIME  
**Severity:** CRITICAL  
**File to Modify:**
- `backend/app/agents/graph.py` (lines 124-147)

**Current Code (BROKEN):**
```python
initial_state: AgentState = {
    "user_id": user_id,
    "user_message": user_message,
    "messages": [...],
    "intent": "",
    "confidence": 0.0,
    "response": "",
    "sources": [],
    "context": {},
    "should_escalate": False,
    "escalation_reason": "",
    "error": "",
    "turn_count": turn_count,
}
```

**Required Changes:**

Add ALL required TypedDict fields from `state.py`:

```python
initial_state: AgentState = {
    # User Information
    "user_id": user_id,
    "student_id": uuid.UUID(user_id),  # Convert to UUID
    "session_id": str(uuid.uuid4()),
    "student_name": current_user.name if current_user else "Student",
    "student_email": current_user.email if current_user else "",
    "student_phone": current_user.phone if current_user else "",
    
    # Admission Information
    "admitted_program": current_user.program if current_user else "",
    "admission_status": "admitted",
    
    # Conversation State
    "user_message": user_message,
    "messages": [{
        "role": "user",
        "content": user_message,
        "agent": None,
        "metadata": None,
    }],
    
    # Intent and Classification
    "intent": "",
    "confidence": 0.0,
    "supervisor_routing_decision": "",
    "query_category": None,
    
    # Agent Tracking
    "current_agent": None,
    "agent_sequence": [],
    "turn_count": turn_count,
    
    # Response Data
    "response": "",
    "sources": [],
    "context": {},
    "conversation_id": uuid.uuid4(),
    
    # Escalation
    "should_escalate": False,
    "escalation_reason": "",
    "escalation_ticket_id": None,
    
    # RAG Data
    "rag_search_query": "",
    "rag_search_results": [],
    "relevant_faq_ids": [],
    
    # Error Handling
    "error": "",
    "error_count": 0,
    
    # Timing
    "conversation_start_time": datetime.now(),
    "last_updated": datetime.now(),
}
```

**Tasks:**
- [ ] Add all required imports (uuid, datetime)
- [ ] Get current_user from context or database
- [ ] Initialize all TypedDict fields
- [ ] Remove hardcoded values
- [ ] Test state creation

**Effort:** 1.5 hours  
**Complexity:** Low

**Success Criteria:**
- ✅ State initializes without TypedDict errors
- ✅ All required fields present
- ✅ Types match schema
- ✅ run_agent() can invoke graph successfully

---

### ACTION 1.3: Fix Database Connection for Docker

**Status:** 🔴 BLOCKING DOCKER  
**Severity:** CRITICAL  
**Files to Modify:**
- `backend/app/config.py` (lines 21-22)
- `backend/deployment/docker/docker-compose.yml` (lines 30-35)

**Current Problem:**

Config (config.py):
```python
DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/saarthi"
```

Docker Compose (docker-compose.yml):
```yaml
postgres:
    environment:
        POSTGRES_DB: saarthi_db
        POSTGRES_USER: saarthi_user
        POSTGRES_PASSWORD: saarthi_password
```

**Mismatch:** Config expects `postgres:postgres` but Docker provides `saarthi_user:saarthi_password`

**Solution:**

**Change 1: Update config.py**
```python
# Use environment variables with defaults
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/saarthi"
)

# Better for Docker
DATABASE_URL_DOCKER: str = "postgresql+asyncpg://saarthi_user:saarthi_password@postgres:5432/saarthi_db"
```

**Change 2: Update docker-compose.yml**
```yaml
backend:
  environment:
    - DATABASE_URL=postgresql+asyncpg://saarthi_user:saarthi_password@postgres:5432/saarthi_db
    - OLLAMA_BASE_URL=http://ollama:11434
    - CHROMA_PERSIST_DIR=/app/storage/vector_db
```

**Change 3: Create .env file**
```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/saarthi
OLLAMA_BASE_URL=http://localhost:11434
```

**Tasks:**
- [ ] Update config.py to use environment variables
- [ ] Update docker-compose.yml with correct credentials
- [ ] Create .env file in backend/
- [ ] Test local connection
- [ ] Test Docker connection
- [ ] Verify database initialization

**Effort:** 1 hour  
**Complexity:** Low

**Success Criteria:**
- ✅ Local development connects to postgres
- ✅ Docker environment connects successfully
- ✅ Database tables created on startup
- ✅ No authentication errors in logs

---

### ACTION 1.4: Fix Escalation Ticket Creation

**Status:** 🔴 BREAKING ESCALATIONS  
**Severity:** CRITICAL  
**File to Modify:**
- `backend/app/agents/escalation_agent.py` (lines 32-48)

**Current Code (BROKEN):**
```python
async with async_session() as session:
    ticket = SupportTicket(
        user_id=uid,
        subject=_generate_subject(user_message),
        description=(...),
        priority=priority,
        department=department,
        status=TicketStatus.OPEN,
    )
    # MISSING: session.add(ticket)
    # MISSING: session.commit()
    # MISSING: ticket_id retrieval
```

**Fixed Code:**
```python
async with async_session() as session:
    ticket = SupportTicket(
        user_id=uid,
        subject=_generate_subject(user_message),
        description=(...),
        priority=priority,
        department=department,
        status=TicketStatus.OPEN,
    )
    
    # ADD THIS:
    session.add(ticket)
    await session.flush()  # Get the ID
    ticket_id = ticket.id
    await session.commit()
    
    return {
        "response": f"I've created support ticket #{ticket_id} for you. Our team will review your case and get back to you soon.",
        "escalation_ticket_id": str(ticket_id),
        "messages": [{
            "role": "assistant",
            "content": f"Escalation: Created ticket #{ticket_id}",
            "agent": "escalation",
            "metadata": {"ticket_id": str(ticket_id)},
        }],
    }
```

**Tasks:**
- [ ] Add session.add(ticket) to create
- [ ] Add session.flush() to get ID
- [ ] Add session.commit() to persist
- [ ] Retrieve ticket_id for response
- [ ] Update return state with ticket_id
- [ ] Test ticket creation

**Effort:** 0.5 hours  
**Complexity:** Low

**Success Criteria:**
- ✅ Ticket created in database
- ✅ Ticket ID returned in response
- ✅ Can retrieve ticket from DB afterward
- ✅ Escalations now work end-to-end

---

### ACTION 1.5: Implement query_stream() in RAG Service

**Status:** 🔴 BREAKING STREAMING  
**Severity:** CRITICAL  
**File to Modify:**
- `backend/app/services/rag_service.py` (add new method)

**Current Problem:**
```python
# chat.py line 82 calls this:
async for chunk in rag_service.query_stream(...)
# But query_stream() doesn't exist!
```

**Solution: Add streaming method to RAGService**

```python
# In backend/app/services/rag_service.py

async def query_stream(
    self,
    question: str,
    category: Optional[str] = None,
    n_context: int = 5,
) -> AsyncGenerator[str, None]:
    """
    Streaming variant of query() - yields tokens as they're generated.
    Useful for SSE streaming responses.
    """
    try:
        # Retrieve from vector store
        results = self.vector_store.query(
            query_text=question,
            n_results=n_context,
            category_filter=category,
        )
        
        # Build context
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        context = "\n".join(documents) if documents else ""
        
        # Stream generation
        async for token in self.ollama_service.generate_stream(
            prompt=question,
            system_prompt=RAG_SYSTEM_PROMPT,
            temperature=0.5,
        ):
            yield token
            
    except Exception as e:
        yield f"\n\nError: {str(e)}"
```

**Tasks:**
- [ ] Add AsyncGenerator import from typing
- [ ] Implement query_stream() method
- [ ] Use ollama_service.generate_stream()
- [ ] Handle errors gracefully
- [ ] Test streaming endpoint
- [ ] Test browser compatibility

**Effort:** 1.5 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ Streaming endpoint doesn't crash
- ✅ Returns SSE formatted data
- ✅ Tokens arrive in real-time
- ✅ Browser can read stream

---

## PHASE 2: HIGH PRIORITY FIXES (8-10 hours)

### ACTION 2.1: Create Conversation Model

**Status:** 🟠 BREAKING MULTI-TURN  
**Severity:** HIGH  
**Files to Create:**
- `backend/app/models/conversation.py`

**Specification:**

```python
# File: backend/app/models/conversation.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Conversation(SQLModel, table=True):
    """Stores conversation sessions for multi-turn support."""
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="conversations")
    
    session_id: str = Field(index=True, unique=True)
    topic: Optional[str] = Field(default=None)
    
    # Conversation metadata
    status: str = Field(default="active")  # active, completed, archived
    turn_count: int = Field(default=0)
    
    # Timing
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = Field(default=None)
    last_message_at: datetime = Field(default_factory=datetime.now)
    
    # Reference
    first_intent: Optional[str] = Field(default=None)
    escalation_ticket_id: Optional[uuid.UUID] = Field(default=None)
    
    # Relationships
    messages: List["ConversationMessage"] = Relationship(back_populates="conversation")


class ConversationMessage(SQLModel, table=True):
    """Stores individual messages in a conversation."""
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id",
        index=True
    )
    conversation: Optional[Conversation] = Relationship(
        back_populates="messages"
    )
    
    # Message content
    role: str = Field(index=True)  # user, assistant, system
    agent: Optional[str] = Field(default=None)  # Which agent generated this
    content: str
    
    # Message metadata
    intent: Optional[str] = Field(default=None)
    confidence: float = Field(default=0.0)
    sources: Optional[list] = Field(default=[])
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.now, index=True)
    processed_in_ms: Optional[int] = Field(default=None)
```

**Tasks:**
- [ ] Create models/conversation.py file
- [ ] Define Conversation class with relationships
- [ ] Define ConversationMessage class
- [ ] Add User -> Conversation relationship
- [ ] Create migration or ensure tables created
- [ ] Test model creation
- [ ] Add queries to retrieve conversations

**Effort:** 2 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ Models can be imported
- ✅ Tables created in database
- ✅ Can create and query conversations
- ✅ Relationships work properly

---

### ACTION 2.2: Create Admin Router

**Status:** 🟠 ADMIN FEATURES MISSING  
**Severity:** HIGH  
**Files to Create:**
- `backend/app/routers/admin.py`

**Specification:**

```python
# File: backend/app/routers/admin.py

Router endpoints needed:

# Conversation Monitoring
GET /admin/conversations
GET /admin/conversations/{conversation_id}
GET /admin/conversations/{conversation_id}/messages

# Analytics
GET /admin/analytics/daily-summary
GET /admin/analytics/agent-performance
GET /admin/analytics/common-issues

# Support Tickets
GET /admin/tickets
PATCH /admin/tickets/{ticket_id}
POST /admin/tickets/{ticket_id}/assign

# System Health
GET /admin/health/system
GET /admin/health/ollama
GET /admin/health/database

# Documents
GET /admin/documents/pending-approval
PATCH /admin/documents/{document_id}/approve
PATCH /admin/documents/{document_id}/reject

# Configuration
GET /admin/config
PATCH /admin/config

# Requires admin role check in all endpoints
```

**Tasks:**
- [ ] Create admin.py file
- [ ] Add @require_admin middleware
- [ ] Implement conversation list endpoint
- [ ] Implement analytics endpoints
- [ ] Implement support ticket endpoints
- [ ] Implement document approval endpoints
- [ ] Add to main.py router includes
- [ ] Test all endpoints

**Effort:** 3 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ Admin router file created
- ✅ All endpoints return proper responses
- ✅ Admin-only access enforced
- ✅ Data aggregation working

---

### ACTION 2.3: Fix Vector Store Embedding Consistency

**Status:** 🟠 BREAKING SEMANTIC SEARCH  
**Severity:** HIGH  
**File to Modify:**
- `backend/app/services/vector_store.py` (lines 30-45)

**Current Problem:**
```python
@property
def collection(self) -> chromadb.Collection:
    return self.client.get_or_create_collection(
        name=self.COLLECTION_NAME,
        metadata={"description": "..."},
        # NO embedding_function specified!
    )
```

ChromaDB uses default embeddings, but documents were added with Ollama embeddings.

**Solution:**

```python
@property
def collection(self) -> chromadb.Collection:
    """Get or create collection with proper embedding function."""
    
    # Define embedding function
    def embed_with_ollama(texts: List[str]) -> List[List[float]]:
        """Use Ollama for embeddings to match ingestion."""
        embeddings = []
        for text in texts:
            embedding = asyncio.run(
                self.ollama_service.generate_single_embedding(text)
            )
            embeddings.append(embedding)
        return embeddings
    
    return self.client.get_or_create_collection(
        name=self.COLLECTION_NAME,
        metadata={"description": "Saarthi student onboarding knowledge base"},
        embedding_function=embed_with_ollama,  # Add this
    )
```

**Alternative (Better):** Ingest embeddings separately
```python
# When adding documents:
embeddings = await self.ollama_service.generate_embeddings(texts)
self.vector_store.add_documents(
    documents=texts,
    metadatas=metadatas,
    ids=ids,
    embeddings=embeddings,  # Pre-computed embeddings
)
```

**Tasks:**
- [ ] Specify embedding function in collection creation
- [ ] OR pre-compute embeddings during ingestion
- [ ] Test semantic search quality
- [ ] Re-index existing documents if needed
- [ ] Verify search returns relevant results

**Effort:** 1.5 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ Semantic search returns relevant documents
- ✅ Embedding consistency verified
- ✅ FAQ queries work properly
- ✅ Search quality improved

---

### ACTION 2.4: Fix Async/Await Violations

**Status:** 🟠 PERFORMANCE ISSUES  
**Severity:** HIGH  
**Files to Modify:**
- `backend/app/services/rag_service.py` (line 47+)
- `backend/app/services/knowledge_service.py` (line 36+)
- `backend/app/services/vector_store.py` (all methods)

**Problem:** Blocking operations called from async context

**Solution: Use run_in_executor**

```python
# In rag_service.py
from concurrent.futures import ThreadPoolExecutor

async def query(
    self,
    question: str,
    category: Optional[str] = None,
    n_context: int = 5,
) -> Dict[str, Any]:
    """Async-safe RAG query."""
    loop = asyncio.get_event_loop()
    
    # Run blocking vector store operation in thread pool
    results = await loop.run_in_executor(
        None,  # Use default executor
        lambda: self.vector_store.query(
            query_text=question,
            n_results=n_context,
            category_filter=category,
        )
    )
    
    # Continue with async operations...
```

**Tasks:**
- [ ] Add asyncio imports
- [ ] Wrap blocking vector store calls
- [ ] Wrap blocking knowledge service calls
- [ ] Test that event loop isn't blocked
- [ ] Monitor performance improvement

**Effort:** 2 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ No blocking operations in async context
- ✅ Other requests can process concurrently
- ✅ Performance improves under load

---

### ACTION 2.5: Implement Turn Count Tracking

**Status:** 🟠 MULTI-TURN BROKEN  
**Severity:** HIGH  
**Files to Modify:**
- `backend/app/routers/chat.py` (lines 76-77)
- `backend/app/services/chat_service.py` (NEW)

**Solution:**

```python
# In chat.py - replace TODO with actual tracking

# Get or create conversation session
session_id = request.session_id or str(uuid.uuid4())

# Load existing conversation
existing_conv = await db.query(Conversation).filter(
    Conversation.session_id == session_id
).first()

if existing_conv:
    turn_count = existing_conv.turn_count + 1
    conversation_id = existing_conv.id
else:
    turn_count = 1
    conversation_id = uuid.uuid4()

# Call agent with proper turn count
result = await run_agent(
    user_message=request.message,
    user_id=str(current_user.id),
    conversation_id=str(conversation_id),
    turn_count=turn_count,  # NOT hardcoded to 0!
    session_id=session_id,
)

# Save message to database
msg = ConversationMessage(
    conversation_id=conversation_id,
    role="user",
    content=request.message,
)
db.add(msg)

assistant_msg = ConversationMessage(
    conversation_id=conversation_id,
    role="assistant",
    content=result["response"],
    agent=result.get("intent"),
    confidence=result.get("confidence"),
)
db.add(assistant_msg)
await db.commit()
```

**Tasks:**
- [ ] Modify chat endpoint to get/create conversation
- [ ] Increment turn count
- [ ] Save messages to conversation
- [ ] Return session_id to client
- [ ] Test multi-turn context preservation
- [ ] Test session resumption

**Effort:** 2 hours  
**Complexity:** Medium

**Success Criteria:**
- ✅ Turn count increments properly
- ✅ Conversation history persists
- ✅ Context preserved across turns
- ✅ Sessions can be resumed

---

## PHASE 3: MEDIUM PRIORITY FIXES (4-6 hours)

### ACTION 3.1: Implement Ollama Model Auto-Download

**Priority:** MEDIUM  
**File to Modify:**
- `backend/deployment/docker/docker-compose.yml`
- `backend/deployment/docker/ollama-init.sh` (NEW)

**Solution:**

```dockerfile
# Create new file: backend/deployment/docker/ollama-init.sh
#!/bin/bash

# Start Ollama in background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
sleep 10

# Pull required models
echo "Downloading Ollama models..."
ollama pull llama2
ollama pull llava
ollama pull nomic-embed-text

# Wait for background process
wait $OLLAMA_PID
```

```yaml
# In docker-compose.yml - update ollama service:
ollama:
  image: ollama/ollama:latest
  container_name: saarthi-ollama
  ports:
    - "11434:11434"
  volumes:
    - ollama_data:/root/.ollama
    - ./ollama-init.sh:/init.sh:ro
  entrypoint: /bin/bash
  command: /init.sh  # Run script instead of ollama serve
  environment:
    - OLLAMA_HOST=0.0.0.0:11434
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
    interval: 30s
    timeout: 10s
    retries: 5
    start_period: 60s  # Give model download time
```

**Tasks:**
- [ ] Create ollama-init.sh script
- [ ] Update docker-compose.yml
- [ ] Test model download completes
- [ ] Update healthcheck timing
- [ ] Document model sizes in README

**Effort:** 1 hour  
**Complexity:** Low

**Success Criteria:**
- ✅ Models auto-download on container start
- ✅ Healthcheck waits for models
- ✅ No manual `ollama pull` needed

---

### ACTION 3.2: Improve Error Handling

**Priority:** MEDIUM  
**Files to Modify:**
- `backend/app/agents/supervisor.py` (JSON parsing)
- `backend/app/services/rag_service.py` (error handling)
- `backend/app/agents/escalation_agent.py` (error recovery)

**Tasks:**
- [ ] Add structured logging to all services
- [ ] Add try/catch with proper logging
- [ ] Add retry logic where appropriate
- [ ] Return meaningful error messages
- [ ] Add middleware for unhandled exceptions

**Effort:** 1.5 hours  
**Complexity:** Low

---

### ACTION 3.3: Add Input Validation Middleware

**Priority:** MEDIUM  
**File to Create:**
- `backend/app/middleware/validation.py`

**Tasks:**
- [ ] Create validation middleware
- [ ] Validate request sizes
- [ ] Validate field types
- [ ] Sanitize inputs
- [ ] Add to main.py

**Effort:** 1 hour  
**Complexity:** Low

---

### ACTION 3.4: Fix Config Path Issues

**Priority:** MEDIUM  
**File to Modify:**
- `backend/app/config.py`

**Tasks:**
- [ ] Use absolute paths for Docker
- [ ] Add path validation on startup
- [ ] Create directories if missing
- [ ] Add configuration logging

**Effort:** 0.5 hours  
**Complexity:** Low

---

## PHASE 4: TESTING & VALIDATION (3-4 hours)

### ACTION 4.1: End-to-End Testing

**Create test scenarios:**
- [ ] User sends simple greeting
- [ ] User asks FAQ question
- [ ] User inquires about tasks
- [ ] User needs escalation
- [ ] Multi-turn conversation
- [ ] Document upload and verification

**Effort:** 1.5 hours

---

### ACTION 4.2: Performance Testing

**Test under load:**
- [ ] Multiple concurrent users
- [ ] Streaming response latency
- [ ] Database query performance
- [ ] Ollama response time

**Effort:** 1 hour

---

### ACTION 4.3: Deployment Testing

**Test in all environments:**
- [ ] Local development
- [ ] Docker compose
- [ ] Kubernetes cluster

**Effort:** 1.5 hours

---

## EXECUTION CHECKLIST

### Phase 1: Critical Fixes
- [ ] 1.1 Create document_verification_agent.py
- [ ] 1.2 Fix AgentState initialization
- [ ] 1.3 Fix database credentials
- [ ] 1.4 Fix escalation ticket creation
- [ ] 1.5 Implement query_stream()

### Phase 2: High Priority
- [ ] 2.1 Create conversation model
- [ ] 2.2 Create admin router
- [ ] 2.3 Fix vector store embedding
- [ ] 2.4 Fix async/await issues
- [ ] 2.5 Implement turn tracking

### Phase 3: Medium Priority
- [ ] 3.1 Ollama auto-download
- [ ] 3.2 Improve error handling
- [ ] 3.3 Add validation middleware
- [ ] 3.4 Fix config paths

### Phase 4: Testing
- [ ] 4.1 E2E testing
- [ ] 4.2 Performance testing
- [ ] 4.3 Deployment testing

---

## TIMELINE ESTIMATE

| Phase | Tasks | Hours | Days |
|-------|-------|-------|------|
| 1 | Critical Fixes | 6 | 1 |
| 2 | High Priority | 10 | 1.5 |
| 3 | Medium Priority | 4 | 0.5 |
| 4 | Testing | 3 | 0.5 |
| **TOTAL** | **16 tasks** | **23** | **3.5** |

---

## SUCCESS CRITERIA (PRODUCTION READY)

When completed, the system should:
- ✅ Start without errors
- ✅ Accept chat requests
- ✅ Route to correct agents
- ✅ Retrieve FAQ answers
- ✅ Process tasks
- ✅ Create escalation tickets
- ✅ Support multi-turn conversations
- ✅ Verify documents
- ✅ Provide admin functionality
- ✅ Handle errors gracefully
- ✅ Scale under load

---

## RISK MITIGATION

**Risk: Database migration failures**
- Mitigation: Keep backups, test migrations separately

**Risk: Ollama model download takes too long**
- Mitigation: Pre-pull models, document requirements

**Risk: Breaking existing functionality**
- Mitigation: Write tests before modifying

**Risk: Performance degradation**
- Mitigation: Profile before and after changes

---

**Next Step:** Start with ACTION 1.1 and work through systematically. Each completed action should be tested before moving to the next.

