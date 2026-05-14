"""
Supervisor / Router Agent — the entry node of the LangGraph.

Analyzes the student's message and classifies it into an intent:
- "faq"        → route to FAQ/RAG Agent
- "task"       → route to Onboarding Task Agent
- "escalation" → route to Escalation Agent
- "greeting"   → handle inline with a friendly response

Uses Ollama for intent classification with a structured prompt.
"""

import json
from app.agents.state import AgentState
from app.services.ollama_service import ollama_service

SUPERVISOR_SYSTEM_PROMPT = """You are the Supervisor agent of Saarthi, a smart student onboarding assistant.

Your ONLY job is to classify the student's message into one of these intents. Respond with ONLY a JSON object — no extra text, no markdown fences.

Intents:
1. "greeting" — Simple greetings, hello, thanks, goodbye, how are you, etc.
2. "faq" — Questions about college info: admissions, fees, hostel, academics, LMS, exams, placements, dress code, timings, contacts, extracurricular, or any general knowledge question.
3. "task" — Anything about the student's onboarding checklist, pending tasks, deadlines, or what they need to do next.
4. "document" — Queries specifically about uploaded documents, document verification status, rejected documents, or how to upload a document.
5. "workflow" — Requests to perform an action or automate a process, such as "assign me a mentor" or "apply for hostel".
6. "escalation" — Complaints, frustration, repeated failures, requests to talk to a human, unresolved issues, or anything the AI cannot handle.

Respond with EXACTLY this JSON format (no markdown, no explanation):
{"intent": "faq", "confidence": 0.95}

Examples:
- "Hello!" → {"intent": "greeting", "confidence": 0.99}
- "What documents do I need?" → {"intent": "faq", "confidence": 0.95}
- "What is the fee structure?" → {"intent": "faq", "confidence": 0.95}
- "What tasks do I have pending?" → {"intent": "task", "confidence": 0.95}
- "Is my marksheet verified?" → {"intent": "document", "confidence": 0.95}
- "Why was my document rejected?" → {"intent": "document", "confidence": 0.85}
- "Please assign me a mentor" → {"intent": "workflow", "confidence": 0.95}
- "I want to apply for a hostel room" → {"intent": "workflow", "confidence": 0.95}
- "This is not working, I need help from a real person" → {"intent": "escalation", "confidence": 0.90}
- "How do I access LMS?" → {"intent": "faq", "confidence": 0.95}
- "What is my onboarding progress?" → {"intent": "task", "confidence": 0.95}"""


async def supervisor_node(state: AgentState) -> dict:
    """
    Classify the student's intent using the LLM.
    Returns updated state fields: intent, confidence, messages.
    """
    user_message = state["user_message"]
    user_msg_lower = user_message.lower()

    # --- Pre-filter overrides for extreme reliability ---
    # If the user explicitly asks for a mentor or hostel, bypass LLM guessing
    if "assign" in user_msg_lower and ("mentor" in user_msg_lower or "guide" in user_msg_lower):
        return {
            "intent": "workflow",
            "confidence": 1.0,
            "messages": [{
                "role": "system",
                "content": "Supervisor used keyword override to classify intent as 'workflow' (mentor assignment).",
                "agent": "supervisor"
            }]
        }
        
    if "apply" in user_msg_lower and ("hostel" in user_msg_lower or "room" in user_msg_lower):
        return {
            "intent": "workflow",
            "confidence": 1.0,
            "messages": [{
                "role": "system",
                "content": "Supervisor used keyword override to classify intent as 'workflow' (hostel application).",
                "agent": "supervisor"
            }]
        }

    try:
        raw_response = await ollama_service.generate(
            prompt=f'Classify this student message: "{user_message}"',
            system_prompt=SUPERVISOR_SYSTEM_PROMPT,
            temperature=0.1,  # Low temperature for deterministic classification
            max_tokens=100,
        )

        # Parse the JSON response
        # Clean up common LLM artifacts (markdown fences, extra text)
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()

        # Try to extract JSON from the response
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback: try to find JSON in the response
            import re
            json_match = re.search(r'\{[^}]+\}', cleaned)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Default to FAQ if classification fails
                result = {"intent": "faq", "confidence": 0.5}

        intent = result.get("intent", "faq").lower()
        confidence = float(result.get("confidence", 0.5))

        # Validate intent
        valid_intents = {"greeting", "faq", "task", "document", "workflow", "escalation"}
        if intent not in valid_intents:
            intent = "faq"
            confidence = 0.5

        return {
            "intent": intent,
            "confidence": confidence,
            "messages": [{
                "role": "system",
                "content": f"Supervisor classified intent as '{intent}' with {confidence:.0%} confidence",
                "agent": "supervisor",
                "metadata": {"raw_response": raw_response[:200]},
            }],
        }

    except Exception as e:
        # If Ollama is down or errors, default to FAQ
        return {
            "intent": "faq",
            "confidence": 0.3,
            "messages": [{
                "role": "system",
                "content": f"Supervisor fallback to 'faq' due to error: {str(e)[:100]}",
                "agent": "supervisor",
                "metadata": {"error": str(e)},
            }],
            "error": f"Supervisor error: {str(e)[:200]}",
        }
