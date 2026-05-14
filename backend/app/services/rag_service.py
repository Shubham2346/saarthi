"""
RAG (Retrieval-Augmented Generation) service — NO Ollama dependency.

Orchestrates the full RAG pipeline entirely through the knowledge base:
1. Takes a student's question.
2. Retrieves relevant FAQ entries from ChromaDB vector store.
3. Constructs a context-enriched response from the knowledge base.
4. Returns the best matching answer with sources.

No LLM/Ollama involved — all responses are grounded in stored knowledge.
"""

from typing import List, Optional, Dict, Any, AsyncGenerator

from app.services.vector_store import vector_store

# Fallback responses organized by topic for when ChromaDB has no results
FALLBACK_RESPONSES = {
    "admission": (
        "I can help you with engineering admission information.\n\n"
        "The admission process typically involves:\n"
        "1) CET or JEE Main entrance exam\n"
        "2) CAP (Centralized Admission Process) rounds\n"
        "3) Branch and college preference filling\n"
        "4) Seat allotment based on merit\n"
        "5) Document verification and fee payment\n\n"
        "For specific information about CET cutoffs, eligibility criteria, "
        "required documents, or counseling dates, please browse the Knowledge Base "
        "section or contact the admission helpdesk."
    ),
    "fee": (
        "Regarding fee structure:\n\n"
        "• Government/merit quota: approx ₹80,000 - ₹1,20,000 per year\n"
        "• Management quota: approx ₹1,50,000 - ₹2,50,000 per year\n"
        "• NRI quota: as per university norms\n\n"
        "Scholarships are available for eligible students (SC/ST/OBC/EWS). "
        "Fees can be paid online via UPI, Net Banking, or Card. "
        "Installment options are available.\n\n"
        "For exact fee amounts and payment deadlines, check the 'Tasks' section "
        "or contact the accounts office."
    ),
    "hostel": (
        "For hostel accommodation:\n\n"
        "• Hostel is not mandatory for day scholars (within 30 km radius)\n"
        "• Apply through the 'Hostel Application' section after admission\n"
        "• Room types: Triple (₹40k/yr), Double (₹55k/yr), Single (₹75k/yr)\n"
        "• Facilities: Wi-Fi, mess, 24/7 security, study rooms\n"
        "• Hostel allotment is first-come, first-served\n\n"
        "Required documents: Hostel application form, admission letter, Aadhaar, "
        "parent consent, medical certificate, anti-ragging affidavit."
    ),
    "academic": (
        "Academic information:\n\n"
        "• Semester system with internal assessment (40%) + end-semester exams (60%)\n"
        "• Minimum 75% attendance required per subject\n"
        "• CGPA-based grading on a 10-point scale\n"
        "• Minimum CGPA 4.0 required to graduate\n"
        "• Can carry up to 4 backlogs; more than 4 = year-back\n\n"
        "For the detailed academic calendar and course registration, visit the LMS portal."
    ),
    "lms": (
        "The LMS (Learning Management System):\n\n"
        "• Access course materials, assignments, grades, and attendance\n"
        "• Login with admission number and date of birth\n"
        "• Features: Discussion forums, notifications, timetable, exam schedule\n"
        "• Login issues: Contact IT helpdesk (computer center, Room B-201)\n\n"
        "You can access the LMS through the link provided during orientation."
    ),
    "exam": (
        "Exam information:\n\n"
        "• Internal assessments: 40% weightage (class tests, assignments, lab work)\n"
        "• End-semester exams: 60% weightage (3-hour written exam)\n"
        "• Need minimum 40% in both internal and external separately to pass\n"
        "• Failed a subject? Appear for supplementary exam in the next cycle\n"
        "• Check exam schedule on the LMS portal."
    ),
    "placement": (
        "Placement information:\n\n"
        "• Placement season runs from August to March of the final year\n"
        "• Minimum 60% CGPA (6.0) usually required, no active backlogs\n"
        "• Average package: ₹4-8 LPA depending on branch\n"
        "• Training starts from 3rd year: aptitude, coding, soft skills\n"
        "• Register on the placement portal with updated resume by July\n\n"
        "For current placement statistics, contact the placement office."
    ),
    "documents": (
        "Required documents for engineering admission:\n\n"
        "1) 10th and 12th Marksheets (originals + photocopies)\n"
        "2) Entrance exam scorecard (CET/JEE)\n"
        "3) Aadhaar Card and PAN Card\n"
        "4) Domicile Certificate\n"
        "5) Category Certificate (SC/ST/OBC/EWS) if applicable\n"
        "6) Non-Creamy Layer Certificate (for OBC)\n"
        "7) Transfer and Migration Certificates\n"
        "8) Passport-size photographs (6 copies)\n"
        "9) Gap Certificate (if applicable)\n"
        "10) Physical fitness certificate\n\n"
        "Upload scanned copies (PDF/JPG, max 500 KB) on the portal. "
        "Keep originals ready for physical verification during reporting."
    ),
    "general": (
        "Welcome to Saarthi! I'm your AI admission assistant. I can help you with:\n\n"
        "• Admission process and eligibility (CET/JEE, CAP rounds, merit lists)\n"
        "• Fee structure, payment methods, and scholarships\n"
        "• Hostel accommodation and facilities\n"
        "• Academic policies, grading, and attendance\n"
        "• Document requirements and verification\n"
        "• LMS portal access and troubleshooting\n"
        "• Exam schedule and rules\n"
        "• Placement preparation and process\n\n"
        "Just type your question and I'll do my best to help! "
        "For platform-specific issues, you can also raise a support ticket."
    ),
}


class RAGService:
    """Retrieval-Augmented Generation pipeline — no LLM dependency."""

    def __init__(self):
        self.vector_store = vector_store

    def _build_response_from_sources(
        self, question: str, sources: List[Dict], context_parts: List[str]
    ) -> str:
        """Build a response from retrieved knowledge base sources."""
        if not sources or not context_parts:
            return self._build_fallback_answer(question)

        q_lower = question.lower()

        if any(w in q_lower for w in ["hello", "hi ", "hey", "greetings"]):
            return (
                "Hello! I'm Saarthi, your AI admission assistant. "
                "How can I help you today? You can ask me about admissions, "
                "fees, documents, hostel, and more!"
            )

        if any(w in q_lower for w in ["thank", "thanks"]):
            return (
                "You're welcome! If you have any more questions, "
                "feel free to ask. I'm here to help!"
            )

        if any(w in q_lower for w in ["who are you", "what can you do", "help"]):
            return FALLBACK_RESPONSES["general"]

        best = sources[0]
        best_answer = context_parts[0].split("A: ")[-1] if context_parts else ""

        if len(sources) > 1 and sources[1].get("relevance_score", 0) > 0.5:
            combined = best_answer
            for i in range(1, min(3, len(sources))):
                additional = (
                    context_parts[i].split("A: ")[-1]
                    if i < len(context_parts)
                    else ""
                )
                if additional and additional != best_answer:
                    combined += "\n\n" + additional
            return combined

        return best_answer

    def _build_fallback_answer(
        self, question: str, category: Optional[str] = None
    ) -> str:
        """Build a context-based fallback answer without retrieval."""
        q_lower = question.lower()

        if any(w in q_lower for w in ["hello", "hi ", "hey", "greetings"]):
            return (
                "Hello! I'm Saarthi, your AI admission assistant. "
                "How can I help you today? You can ask me about admissions, "
                "fees, documents, hostel, and more!"
            )

        if any(w in q_lower for w in ["thank", "thanks"]):
            return (
                "You're welcome! If you have any more questions, "
                "feel free to ask. I'm here to help!"
            )

        if any(w in q_lower for w in ["who are you", "what can you do", "help"]):
            return FALLBACK_RESPONSES["general"]

        if any(
            w in q_lower
            for w in ["admission", "cet", "jee", "cap", "cutoff", "merit", "apply", "seat"]
        ):
            return FALLBACK_RESPONSES["admission"]

        if any(
            w in q_lower
            for w in ["fee", "payment", "scholarship", "installment", "reimbursement", "pay"]
        ):
            return FALLBACK_RESPONSES["fee"]

        if any(
            w in q_lower
            for w in ["hostel", "accommodation", "room", "mess", "dorm"]
        ):
            return FALLBACK_RESPONSES["hostel"]

        if any(
            w in q_lower
            for w in ["document", "certificate", "upload", "scanned", "marksheet"]
        ):
            return FALLBACK_RESPONSES["documents"]

        if any(
            w in q_lower
            for w in ["academic", "syllabus", "attendance", "grade", "cgpa", "semester"]
        ):
            return FALLBACK_RESPONSES["academic"]

        if any(w in q_lower for w in ["lms", "login", "password", "portal"]):
            return FALLBACK_RESPONSES["lms"]

        if any(
            w in q_lower for w in ["exam", "test", "fail", "backlog", "supplementary"]
        ):
            return FALLBACK_RESPONSES["exam"]

        if any(
            w in q_lower for w in ["placement", "job", "company", "interview", "package"]
        ):
            return FALLBACK_RESPONSES["placement"]

        if category and category.lower() in FALLBACK_RESPONSES:
            return FALLBACK_RESPONSES[category.lower()]

        return FALLBACK_RESPONSES["general"]

    async def query(
        self,
        question: str,
        category: Optional[str] = None,
        n_context: int = 5,
    ) -> Dict[str, Any]:
        """
        Full RAG pipeline: retrieve from vector store -> build response.
        Works entirely without Ollama. Uses ChromaDB to find the best
        matching knowledge entries.
        """
        sources = []
        context_parts = []

        try:
            results = await self.vector_store.query(
                query_text=question,
                n_results=n_context,
                category_filter=category,
            )

            if results and results.get("documents"):
                for i, (doc, metadata, distance) in enumerate(
                    zip(
                        results["documents"][0],
                        results["metadatas"][0],
                        results["distances"][0],
                    )
                ):
                    context_parts.append(
                        f"[Source {i + 1}] (Category: {metadata.get('category', 'N/A')})\n"
                        f"Q: {metadata.get('question', 'N/A')}\n"
                        f"A: {doc}"
                    )
                    sources.append({
                        "question": metadata.get("question", ""),
                        "category": metadata.get("category", ""),
                        "relevance_score": round(1 - distance, 3) if distance else 0,
                    })
        except Exception:
            pass

        if sources:
            answer = self._build_response_from_sources(question, sources, context_parts)
            return {
                "answer": answer,
                "sources": sources,
                "context_used": len(sources),
            }

        answer = self._build_fallback_answer(question, category)
        return {
            "answer": answer,
            "sources": [],
            "context_used": 0,
            "fallback": True,
        }

    async def query_stream(
        self,
        question: str,
        category: Optional[str] = None,
        n_context: int = 5,
    ) -> AsyncGenerator[str, None]:
        """Streaming variant — yields the full answer in a single chunk."""
        result = await self.query(
            question=question,
            category=category,
            n_context=n_context,
        )
        yield result.get("answer", "I couldn't process your request.")

    async def search_knowledge_base(
        self,
        query: str,
        category: Optional[str] = None,
        n_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """Search the knowledge base without generating a response."""
        results = await self.vector_store.query(
            query_text=query,
            n_results=n_results,
            category_filter=category,
        )

        entries = []
        if results and results.get("documents"):
            for doc, metadata, distance, doc_id in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
                results["ids"][0],
            ):
                entries.append({
                    "id": doc_id,
                    "question": metadata.get("question", ""),
                    "answer": doc,
                    "category": metadata.get("category", ""),
                    "relevance_score": round(1 - distance, 3) if distance else 0,
                })

        return entries


# Singleton instance
rag_service = RAGService()
