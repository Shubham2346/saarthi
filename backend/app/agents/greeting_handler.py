"""
Greeting Handler — handles simple greetings, thanks, and goodbyes.

This is a lightweight node that doesn't need the LLM.
Fast, deterministic, and saves Ollama calls for real queries.
"""

import random
from app.agents.state import AgentState


GREETING_RESPONSES = [
    "Hello! 👋 Welcome to Saarthi, your onboarding assistant! How can I help you today? You can ask me about admissions, your pending tasks, college facilities, or anything else related to your onboarding journey.",
    "Hi there! 😊 I'm Saarthi, here to help you with your college onboarding. Feel free to ask me about your tasks, documents, fees, hostel, or anything else!",
    "Hey! Welcome aboard! 🎓 I'm your onboarding buddy. Ask me anything — from deadlines and documents to hostel rules and LMS access.",
]

THANKS_RESPONSES = [
    "You're welcome! 😊 Let me know if you need anything else. I'm always here to help!",
    "Happy to help! Feel free to ask if you have more questions about your onboarding.",
    "Glad I could assist! Don't hesitate to reach out anytime. Good luck with your onboarding! 🎉",
]

GOODBYE_RESPONSES = [
    "Goodbye! 👋 Best of luck with your onboarding. Remember, I'm here whenever you need help!",
    "See you later! Don't forget to check your pending tasks. You've got this! 💪",
    "Take care! Feel free to come back anytime you have questions. Welcome to the college! 🎓",
]


async def greeting_node(state: AgentState) -> dict:
    """
    Handle simple greetings without invoking the LLM.
    Fast and deterministic.
    """
    user_message = state["user_message"].lower().strip()

    # Detect which type of greeting
    if any(w in user_message for w in ["thank", "thanks", "thx", "appreciated"]):
        response = random.choice(THANKS_RESPONSES)
    elif any(w in user_message for w in ["bye", "goodbye", "see you", "later", "cya"]):
        response = random.choice(GOODBYE_RESPONSES)
    else:
        response = random.choice(GREETING_RESPONSES)

    return {
        "response": response,
        "messages": [{
            "role": "assistant",
            "content": f"Greeting handler: responded to '{user_message[:30]}...'",
            "agent": "greeting",
            "metadata": None,
        }],
    }
