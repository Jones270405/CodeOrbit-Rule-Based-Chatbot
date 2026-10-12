"""Core response logic for the Rule-Based Chatbot."""
from datetime import date
import re

HELP_TEXT = """Here are some things you can ask me:
• Hello / Good morning
• Who are you?
• What is Python?
• What is Artificial Intelligence?
• What is Machine Learning?
• What is hydrogen?
• What is Newton's third law?
• What direction does the sun rise?
• How many months are there in a year?
• What day is it today?
• What are some good movie genres?
• Which music is good for studying?
• 25 + 37 (you can also use -, *, or /)
Type 'bye' to end a terminal conversation."""

RULES = {
    "greetings": {
        "hi": "Hello! How can I help you?",
        "hello": "Hi! How can I help you?",
        "hey": "Hey! What would you like to know?",
        "howdy": "Howdy! How can I help you?",
        "good morning": "Good morning! How can I help you?",
        "good afternoon": "Good afternoon! How can I help you?",
        "good evening": "Good evening! How can I help you?",
    },
    "about": {
        "who are you": "I am a rule-based chatbot built with Python.",
        "what do you do": "I answer selected questions using predefined rules.",
        "how can you help me": "I can answer predefined questions about general knowledge, education, entertainment, dates, and basic arithmetic.",
    },
    "general": {
        "what direction does the sun rise": "The Sun rises in the east and sets in the west.",
        "how many seasons are there": "Many regions commonly describe four seasons: spring, summer, autumn, and winter. The number can vary by climate and region.",
        "how many months are there in a year": "There are 12 months in a year.",
    },
    "education": {
        "what is python": "Python is a general-purpose programming language known for its readable syntax.",
        "what is the third law of newton": "Newton's third law states that for every action, there is an equal and opposite reaction.",
        "what is hydrogen": "Hydrogen is the lightest chemical element.",
        "what is artificial intelligence": "Artificial intelligence (AI) is a field focused on building systems that perform tasks commonly associated with human intelligence.",
        "what is machine learning": "Machine learning is a branch of AI in which computer systems learn patterns from data.",
    },
    "entertainment": {
        "what are some best genres in movies": "Popular movie genres include comedy, drama, action, thriller, romance, animation, science fiction, and mystery.",
        "what is the best cartoon to improve english": "Try shows with clear dialogue, such as Martha Speaks or Phineas and Ferb. Choose content that suits your age and interests.",
        "which music is best for relaxation": "Many people find slow, soothing, or instrumental music relaxing.",
        "what is a good movie for family": "Family-friendly animation, comedy, and adventure films can be good choices. Check the age rating before watching.",
        "what music is good for studying": "Instrumental, classical, ambient, or lo-fi music may help some people focus.",
    },
    "conversation": {
        "how are you": "I'm running well—thanks for asking! What can I help you with?",
        "i am feeling good": "That's great to hear!",
        "i am not feeling well": "I'm sorry you're not feeling well. I hope things improve soon.",
        "help me solve this": "Tell me what you need help with. I can answer supported questions or calculate basic arithmetic.",
        "thank you": "You're welcome!",
        "thanks": "You're welcome!",
    },
}

EXIT_MESSAGES = {
    "bye": "Goodbye! Thanks for chatting.",
    "goodbye": "Goodbye! Have a great day.",
    "see you later": "See you later!",
    "talk to you later": "Talk to you later!",
    "exit": "Goodbye! Thanks for chatting.",
    "quit": "Goodbye! Thanks for chatting.",
}


def normalize(text: str) -> str:
    """Normalize case, whitespace, and common punctuation."""
    text = text.lower().strip()
    text = re.sub(r"[?!.,]+$", "", text)
    return " ".join(text.split())


def calculate(text: str):
    """Calculate a basic whole-number expression if one is present."""
    match = re.search(r"(?<!\d)(\d+)\s*([+\-*/])\s*(\d+)(?!\d)", text)
    if not match:
        return None
    left, operator, right = match.groups()
    a, b = int(left), int(right)
    if operator == "+":
        result = a + b
    elif operator == "-":
        result = a - b
    elif operator == "*":
        result = a * b
    else:
        if b == 0:
            return "Division by zero is undefined. Please try a non-zero divisor."
        result = a / b
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return f"{a} {operator} {b} = {result}"

def get_response(user_input: str) -> str:
    """Return a response using predefined rules and a fallback."""
    text = normalize(user_input)
    if not text:
        return "Please type a question or enter 'help' to see what I can answer."
    if text in EXIT_MESSAGES:
        return EXIT_MESSAGES[text]
    if text in {"help", "what can i ask", "what can you answer"}:
        return HELP_TEXT
    math_response = calculate(text)
    if math_response:
        return math_response
    if text in {"what day is it today", "what is today's date", "what is the date today"}:
        return f"Today's date is {date.today().strftime('%d %B %Y')}."
    for category in RULES.values():
        if text in category:
            return category[text]
    return "I don't have a predefined response for that yet.\nType 'help' to see supported questions."

def is_exit_command(user_input: str) -> bool:
    return normalize(user_input) in EXIT_MESSAGES
