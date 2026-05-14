"""
Supervisor / Router Agent — the entry node of the LangGraph.

Analyzes the student's message and classifies it into an intent using
keyword matching (no Ollama dependency for routing).
"""

import re
from app.agents.state import AgentState


# Keyword → intent mapping for Ollama-free classification
INTENT_KEYWORDS = {
    "greeting": [
        r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgreetings\b",
        r"\bhowdy\b", r"\bgood morning\b", r"\bgood evening\b",
        r"\bthanks\b", r"\bthank you\b", r"\bbye\b", r"\bgoodbye\b",
        r"\bhow are you\b", r"\bwhat'?s up\b",
    ],
    "task": [
        r"\btask\w*\b", r"\bonboarding\b", r"\bpending\b",
        r"\bchecklist\b", r"\bwhat.*(?:next|left|remain|due)\b",
        r"\bprogress\b", r"\bstatus\b", r"\bdeadline\b",
        r"\bto-do\b", r"\btodo\b", r"\bmy task\b",
        r"\bupload.*document\b", r"\bdocument.*upload\b",
        r"\bverify\b", r"\bcompleted\b", r"\boverdue\b",
        r"\bacademic.year\b", r"\bfill.*form\b",
    ],
    "admission": [
        r"\badmission\b", r"\bapplication\b", r"\bapply\b",
        r"\benrollment\b", r"\bform\b", r"\bmy name is\b",
        r"\bi want to (?:study|take|join)\b", r"\bprogram\b",
        r"\bcourse.*(?:select|choose|prefer)\b",
        r"\bstream\b", r"\bbranch\b",
        r"\bcap\b", r"\bcet\b", r"\bjee\b", r"\bmerit\b",
        r"\bcounseling\b", r"\bseat\b",
    ],
    "escalation": [
        r"\b(?:not|can'?t|won'?t)\s*(?:working|able|letting)\b",
        r"\bfrustrated\b", r"\bannoyed\b", r"\bangry\b",
        r"\btalk to (?:human|person|agent|real)\b",
        r"\bspeak to\b", r"\bescalate\b",
        r"\bcomplaint\b", r"\bgrievance\b",
        r"\bunresolved\b", r"\brepeated\b",
        r"\breal person\b", r"\bhuman\b",
    ],
    "faq": [
        r"\bfee\b", r"\bfees\b", r"\bscholarship\b",
        r"\bhostel\b", r"\bacademic\b", r"\blms\b",
        r"\bexam\b", r"\bplacement\b", r"\battendance\b",
        r"\bdocument.*(?:needed|require|list)\b",
        r"\bwhat.*(?:need|require|documents)\b",
        r"\bhelp\b", r"\bhow to\b", r"\bwhat is\b",
        r"\bwhen\b", r"\bwhere\b", r"\bwho\b",
        r"\bwhy\b", r"\bcan i\b", r"\bhow do\b",
        r"\bcontact\b", r"\baddress\b", r"\btiming\b",
        r"\binfo\b", r"\binformation\b", r"\bguide\b",
        r"\bdress code\b", r"\brules\b", r"\bpolicies?\b",
        r"\btransport\b", r"\blibrary\b", r"\bsports\b",
        r"\bcultural\b", r"\bextracurricular\b",
    ],
}


def _classify_intent(message: str) -> tuple:
    """Classify intent using keyword matching."""
    msg_lower = message.lower().strip()

    # Short messages
    if len(msg_lower) < 3:
        return "greeting", 0.99

    # Score each intent category
    scores = {}
    for intent, patterns in INTENT_KEYWORDS.items():
        score = 0
        for pattern in patterns:
            if re.search(pattern, msg_lower):
                score += 1
        if score > 0:
            scores[intent] = score

    if not scores:
        return "faq", 0.5

    # Pick intent with highest keyword match count
    best_intent = max(scores, key=scores.get)
    confidence = min(0.5 + (scores[best_intent] * 0.1), 0.98)
    return best_intent, confidence


async def supervisor_node(state: AgentState) -> dict:
    """
    Classify the student's intent using keyword matching.
    No Ollama dependency required.
    """
    user_message = state["user_message"]
    intent, confidence = _classify_intent(str(user_message))

    return {
        "intent": intent,
        "confidence": confidence,
        "messages": [{
            "role": "system",
            "content": f"Supervisor classified intent as '{intent}' with {confidence:.0%} confidence",
            "agent": "supervisor",
        }],
    }
