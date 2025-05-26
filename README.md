# LangGraph Chat Agent with Time Tool

A minimal LangGraph application demonstrating a stateless chat agent that can tell the current time using Google's Gemini model.

## Setup

Python >=3.11 is required!

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate.bat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Google API key:
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

You can get your API key from the [Google AI Studio](https://aistudio.google.com/apikey).

## Running the Application

Start the application with:
```bash
langgraph dev
```

The chat interface will be available at http://localhost:2024

## Testing

To test the time functionality, simply ask "What time is it?" in the chat interface. The agent will use the `get_current_time` tool to fetch and display the current UTC time.

You can also try variations like:
- "When is it now?"
- "Could you tell me the current time?"
- "What's the UTC time?"
- "Hello! I slept for like 6-9 hours and lost now. Help pls"
