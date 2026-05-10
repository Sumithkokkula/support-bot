import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
def load_knowledge_base():
    with open("knowledge_base.txt", "r") as f:
        return f.read()
def detect_sentiment(message):
    frustrated_words = [
        "angry", "frustrated", "terrible", "worst", "useless",
        "pathetic", "ridiculous", "unacceptable", "disgusting",
        "hate", "stupid", "awful", "horrible", "scam", "cheated"
    ]
    message_lower = message.lower()
    return any(word in message_lower for word in frustrated_words)

def detect_confidence(response_text):
    unsure_phrases = [
        "i don't know", "i'm not sure", "i cannot find",
        "not mentioned", "no information", "unclear",
        "i don't have", "not available"
    ]
    response_lower = response_text.lower()
    return not any(phrase in response_lower for phrase in unsure_phrases)

def get_bot_response(user_message, chat_history):
    knowledge_base = load_knowledge_base()
    system_prompt = f"""
You are Alex, a friendly and professional customer support assistant for ShopEase, an online shopping platform.

YOUR KNOWLEDGE BASE:
{knowledge_base}

YOUR RULES:
1. ONLY answer from the knowledge base above
2. If the answer is not in the knowledge base, say exactly: "I don't have enough information on that, let me connect you with a human agent."
3. Be warm, empathetic, and professional
4. Keep answers concise and clear
5. If the user seems angry or frustrated, acknowledge their feelings first before answering
6. Always end with "Is there anything else I can help you with?"

YOU ARE: Alex from ShopEase Support
"""

    is_frustrated = detect_sentiment(user_message)
    if is_frustrated:
        frustration_prefix = "I completely understand your frustration and I sincerely apologize for the inconvenience. Let me help you right away.\n\n"
    else:
        frustration_prefix = ""

    history = []
    for msg in chat_history:
        history.append({
            "role": msg["role"],
            "parts": [msg["content"]]
        })

    model = genai.GenerativeModel(
      model_name="gemini-2.5-flash",

        system_instruction=system_prompt
    )
    chat = model.start_chat(history=history)
    response = chat.send_message(user_message)
    bot_reply = frustration_prefix + response.text
    is_confident = detect_confidence(bot_reply)

    return {
        "reply": bot_reply,
        "is_frustrated": is_frustrated,
        "is_confident": is_confident,
        "escalate": not is_confident or is_frustrated
    }