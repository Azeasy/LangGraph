from datetime import datetime, timezone
from typing import Dict, List
import logging

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import Graph
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Check for API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is required")


def get_current_time() -> dict:
    """Return the current UTC time in ISO‑8601 format.
    Example → {"utc": "2025‑05‑21T06:42:00Z"}"""
    now = datetime.now(timezone.utc)
    return {"utc": now.isoformat()}


# Create the chat model
model = ChatGoogleGenerativeAI(
    model=os.getenv("MODEL_NAME"),
    google_api_key=api_key,
    convert_system_message_to_human=True
)

# Create the agent using LangGraph's prebuilt React agent
graph = create_react_agent(
    model=model,
    tools=[get_current_time],
    prompt="""You are a helpful assistant that can tell the current time when asked.
If the user asks about time, use the get_current_time tool to get the current UTC time.
For all other questions, respond normally without using the tool."""
)

logger.info("Graph compiled and ready")
