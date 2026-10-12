# Rule-Based Chatbot — Portfolio Edition

A Python chatbot with a Streamlit chat interface. It uses predefined rules to answer selected questions about greetings, general knowledge, education, entertainment, dates, and basic arithmetic.

> **Project type:** Rule-based chatbot, not a generative AI assistant.

## Features
- Interactive chat interface with message history
- Suggested questions in the sidebar
- Predefined responses organized by category
- Basic arithmetic with `+`, `-`, `*`, and `/`
- Date response, help command, and fallback response
- Handles empty input and division by zero
- Unit tests for key behaviours

## Project structure
```text
Rule-Based-Chatbot/
├── app.py
├── chatbot.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_chatbot.py
```

## Setup (Python 3.10+)
Optional virtual environment on Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

## Run the web app
```powershell
python -m streamlit run app.py
```
Open the local URL Streamlit prints, usually `http://localhost:8501`.

## Run tests
```powershell
python -m unittest discover -s tests
```

## Example prompts
- `hello`
- `what is python`
- `what is machine learning`
- `what is 25 + 37`
- `what day is it today`
- `help`
- `what is java` (demonstrates the fallback)

## How it works
1. Normalize input to lowercase and consistent whitespace.
2. Check exit and help commands.
3. Detect basic arithmetic with a regular expression.
4. Check the date question and predefined response categories.
5. Return a fallback response if no rule matches.

## Limitations
- Only supported questions and exact predefined phrases are answered, except calculator matching.
- It does not learn from conversations or generate new knowledge.
- Arithmetic is intentionally limited to whole numbers and basic operators.
- The date response uses the computer's local date.

## Future improvements
- Add more intents and phrase variations
- Move responses to a JSON knowledge base
- Expand tests and deploy the app publicly
