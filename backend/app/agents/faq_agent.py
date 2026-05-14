"""
FAQ Agent — answers student questions using RAG (Retrieval-Augmented Generation).

This agent wraps the existing RAG service as a LangGraph node.
It retrieves relevant knowledge from ChromaDB and generates a
context-grounded response via Ollama.
"""

from app.agents.state import AgentState
from app.services.rag_service import rag_service


async def faq_node(state: AgentState) -> dict:
    """
    RAG-powered FAQ agent node.
    Retrieves relevant knowledge and generates a grounded answer.
    """
    user_message = state["user_message"]

    try:
        # Use the existing RAG service
        result = await rag_service.query(
            question=user_message,
            category=None,  # Search across all categories
            n_context=5,
            temperature=0.5,
        )

        answer = result.get("answer", "")
        sources = result.get("sources", [])

        # Check if the answer seems low quality or empty
        if not answer or len(answer.strip()) < 20:
            return {
                "response": (
                    "I wasn't able to find specific information about that in our knowledge base. "
                    "You might want to contact the relevant department directly, or I can create "
                    "a support ticket for you. Would you like me to do that?"
                ),
                "sources": sources,
                "should_escalate": False,
                "messages": [{
                    "role": "assistant",
                    "content": "FAQ agent: No strong match found in knowledge base",
                    "agent": "faq",
                    "metadata": {"sources_found": len(sources)},
                }],
            }

        return {
            "response": answer,
            "sources": sources,
            "messages": [{
                "role": "assistant",
                "content": f"FAQ agent generated response using {len(sources)} sources",
                "agent": "faq",
                "metadata": {
                    "sources_found": len(sources),
                    "context_used": result.get("context_used", 0),
                },
            }],
        }

    except Exception as e:
        return {
            "response": (
                "I'm having trouble accessing the knowledge base right now. "
                "Please try again in a moment, or I can create a support ticket for you."
            ),
            "sources": [],
            "error": f"FAQ agent error: {str(e)[:200]}",
            "messages": [{
                "role": "system",
                "content": f"FAQ agent error: {str(e)[:100]}",
                "agent": "faq",
                "metadata": {"error": str(e)},
            }],
        }
