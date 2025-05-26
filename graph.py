from datetime import datetime, timezone
from typing import Dict, List
import logging

from langgraph.graph import Graph
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(os.getenv("MODEL_NAME"))
logger.info(f"Initialized Gemini model: {os.getenv('MODEL_NAME')}")


@tool("get_current_time_tool", parse_docstring=True)
def get_current_time() -> str:
    """Return the current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat()


def create_agent():
    def run_step(state: Dict) -> Dict:
        """Run one step of the agent."""
        logger.info(f"Received state: {state}")

        messages = state.get("messages", [])
        if not messages:
            logger.warning("No messages in state")
            return state

        user_message = messages[-1]["content"]
        logger.info(f"Processing user message: {user_message}")

        # Simple prompt that includes both system behavior and user message
        prompt = f"""You are a helpful assistant that can tell the current time when asked.
If the user asks about time, respond with exactly 'GET_TIME'.
Otherwise, be helpful and respond normally.

User message: {user_message}"""

        try:
            response = model.generate_content(prompt)
            logger.info(f"Initial model response: {response.text}")

            if "GET_TIME" in response.text:
                time = get_current_time.invoke(prompt)
                logger.info(f"Getting current time: {time}")
                response = model.generate_content(f"The current UTC time is {time}. Please tell this to the user.")

            return {
                "messages": messages + [{"type": "ai", "content": response.text}]
            }

        except Exception as e:
            logger.error(f"Error in run_step: {str(e)}")
            return {
                "messages": messages + [{"type": "ai", "content": "I apologize, but I encountered an error. Please try again."}]
            }

    workflow = Graph()
    workflow.add_node("agent", run_step)
    workflow.set_entry_point("agent")
    workflow.set_finish_point("agent")

    logger.info("Created LangGraph workflow")
    return workflow.compile()


graph = create_agent()
logger.info("Graph compiled and ready")
