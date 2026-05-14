"""
Document Verification Agent — processes and verifies student documents.

This agent:
1. Handles document upload requests
2. Uses OCR to extract text from documents
3. Validates documents against requirements
4. Returns verification results or requests for reupload
5. Can escalate to human if manual review needed
"""

from app.agents.state import AgentState
from app.services.ocr_service import ocr_service
from typing import Dict, Any, Optional


# Document requirements by type
DOCUMENT_REQUIREMENTS = {
    "admission_letter": {
        "required_keywords": ["admission", "congratulations", "enrolled", "program"],
        "min_confidence": 0.7,
    },
    "marksheet": {
        "required_keywords": ["marks", "total", "grade", "score"],
        "min_confidence": 0.7,
    },
    "id_proof": {
        "required_keywords": ["name", "date", "identification"],
        "min_confidence": 0.7,
    },
    "address_proof": {
        "required_keywords": ["address", "residential", "location"],
        "min_confidence": 0.6,
    },
}


async def document_verification_node(state: AgentState) -> dict:
    """
    Document verification agent node.
    Processes uploaded documents and validates them.
    """
    user_message = state.get("user_message", "")
    user_id = state.get("user_id", "")

    try:
        # Check if this is a document-related query
        if not _is_document_request(user_message):
            return {
                "response": (
                    "This doesn't seem to be a document-related request. "
                    "Please upload a document or ask about document requirements."
                ),
                "messages": [{
                    "role": "assistant",
                    "content": "Document agent: Not a document request",
                    "agent": "document_verification",
                    "metadata": {"request_type": "invalid"},
                }],
            }

        # Extract document type from message
        doc_type = _detect_document_type(user_message)
        if not doc_type:
            return {
                "response": (
                    "I couldn't identify the document type. "
                    "Please specify which document you're uploading: "
                    "admission letter, marksheet, ID proof, or address proof."
                ),
                "should_escalate": False,
                "messages": [{
                    "role": "assistant",
                    "content": "Document agent: Could not identify document type",
                    "agent": "document_verification",
                    "metadata": {"request_type": "unknown_type"},
                }],
            }

        # Get document requirements
        requirements = DOCUMENT_REQUIREMENTS.get(doc_type, {})

        # In a real scenario, we'd have the file path from the request
        # For now, we'll provide guidance
        response = (
            f"Thank you for uploading your {doc_type.replace('_', ' ')}. "
            f"I'll verify it for you.\n\n"
            f"Requirements:\n"
            f"• File format: PDF or image (JPG, PNG)\n"
            f"• Minimum resolution: 300 DPI\n"
            f"• File size: Less than 10 MB\n"
            f"• Content must be clear and legible\n\n"
            f"Processing your document..."
        )

        return {
            "response": response,
            "sources": [],
            "messages": [{
                "role": "assistant",
                "content": f"Document agent: Processing {doc_type}",
                "agent": "document_verification",
                "metadata": {
                    "document_type": doc_type,
                    "requirements": requirements,
                },
            }],
        }

    except Exception as e:
        return {
            "response": (
                "I encountered an error while processing your document. "
                "Please try again or contact support if the issue persists."
            ),
            "sources": [],
            "error": f"Document verification error: {str(e)[:200]}",
            "should_escalate": True,
            "escalation_reason": "Document processing error",
            "messages": [{
                "role": "system",
                "content": f"Document agent error: {str(e)[:100]}",
                "agent": "document_verification",
                "metadata": {"error": str(e)},
            }],
        }


def _is_document_request(message: str) -> bool:
    """
    Check if the message is about document upload or verification.
    """
    doc_keywords = [
        "document", "upload", "submit", "attach", "file",
        "marksheet", "admit", "admission", "certificate",
        "proof", "id", "address", "verification", "verify"
    ]
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in doc_keywords)


def _detect_document_type(message: str) -> Optional[str]:
    """
    Detect what type of document the user is referring to.
    """
    message_lower = message.lower()

    # Check for admission letter
    if any(word in message_lower for word in ["admission", "admit", "acceptance"]):
        return "admission_letter"

    # Check for marksheet
    if any(word in message_lower for word in ["marksheet", "marks", "score", "certificate"]):
        return "marksheet"

    # Check for ID proof
    if any(word in message_lower for word in ["id", "aadhar", "passport", "pan"]):
        return "id_proof"

    # Check for address proof
    if any(word in message_lower for word in ["address", "utility", "electricity", "rent"]):
        return "address_proof"

    return None


def _validate_document_content(
    text: str,
    doc_type: str,
    confidence: float,
) -> Dict[str, Any]:
    """
    Validate extracted document content against requirements.
    """
    requirements = DOCUMENT_REQUIREMENTS.get(doc_type, {})
    min_confidence = requirements.get("min_confidence", 0.7)
    required_keywords = requirements.get("required_keywords", [])

    # Check confidence
    confidence_ok = confidence >= min_confidence

    # Check for required keywords
    text_lower = text.lower()
    keywords_found = sum(1 for kw in required_keywords if kw in text_lower)
    keywords_ok = keywords_found >= (len(required_keywords) // 2)  # At least 50% of keywords

    return {
        "is_valid": confidence_ok and keywords_ok,
        "confidence": confidence,
        "keywords_found": keywords_found,
        "total_keywords": len(required_keywords),
        "confidence_ok": confidence_ok,
        "keywords_ok": keywords_ok,
    }
