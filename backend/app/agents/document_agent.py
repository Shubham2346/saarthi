"""
Document Agent — handles queries related to student documents and uploads.
"""

import uuid
from app.agents.state import AgentState
from app.services.ollama_service import ollama_service
from app.database import async_session
from app.models.document import Document
from sqlmodel import select


DOCUMENT_AGENT_SYSTEM_PROMPT = """You are the **Document Agent** of Saarthi, a student onboarding assistant.

Your job is to answer questions about the student's uploaded documents, verification status, and requirements.

You will receive the student's DOCUMENT DATA (from the database) and their QUESTION.

Rules:
- Be helpful and reassuring.
- Clearly state the status of uploaded documents (Verified, Rejected, Processing, Uploaded).
- If a document is rejected, politely explain the rejection reason and ask them to re-upload.
- Keep responses concise — 2-3 paragraphs max.
- Never make up document status. Only reference actual documents provided."""


async def _fetch_document_data(user_id: str) -> dict:
    """Fetch the student's document data from the database."""
    try:
        uid = uuid.UUID(user_id)
    except (ValueError, TypeError):
        return {"error": "Invalid user ID", "documents": []}

    try:
        async with async_session() as session:
            statement = select(Document).where(Document.user_id == uid).order_by(Document.created_at.desc())
            result = await session.execute(statement)
            docs = result.scalars().all()
            
            doc_list = []
            for d in docs:
                doc_list.append({
                    "filename": d.original_filename,
                    "status": d.status.value,
                    "rejection_reason": d.rejection_reason,
                    "uploaded_at": d.created_at.strftime("%B %d, %Y")
                })
            return {"documents": doc_list}
    except Exception as e:
        return {"error": str(e), "documents": []}


async def document_node(state: AgentState) -> dict:
    """
    Document agent node.
    Fetches the student's documents from the DB and generates a contextual response.
    """
    user_message = state["user_message"]
    user_id = state.get("user_id", "")

    doc_data = await _fetch_document_data(user_id)

    if doc_data.get("error"):
        return {
            "response": "I couldn't fetch your document records at the moment. Please try again later.",
            "messages": [{
                "role": "system",
                "content": f"Document agent error: {doc_data.get('error')}",
                "agent": "document",
                "metadata": {"error": doc_data.get("error")},
            }],
        }

    docs = doc_data["documents"]
    
    doc_summary = "STUDENT'S DOCUMENT UPLOADS:\n\n"
    if not docs:
        doc_summary += "No documents uploaded yet."
    else:
        for d in docs:
            reason = f" (Reason: {d['rejection_reason']})" if d['rejection_reason'] else ""
            doc_summary += f"- {d['filename']} | Status: {d['status'].upper()}{reason} | Uploaded: {d['uploaded_at']}\n"

    augmented_prompt = f"""{doc_summary}

---

STUDENT'S QUESTION: {user_message}

Respond helpfully based on the document data above."""

    try:
        answer = await ollama_service.generate(
            prompt=augmented_prompt,
            system_prompt=DOCUMENT_AGENT_SYSTEM_PROMPT,
            temperature=0.5,
            max_tokens=600,
        )

        return {
            "response": answer,
            "context": {"document_count": len(docs)},
            "messages": [{
                "role": "assistant",
                "content": f"Document agent: Found {len(docs)} documents",
                "agent": "document",
                "metadata": {"document_count": len(docs)},
            }],
        }
    except Exception as e:
        return {
            "response": "I see you're asking about documents, but I'm having trouble analyzing your request right now. Please check your dashboard or try again.",
            "error": f"Document agent error: {str(e)}",
        }
