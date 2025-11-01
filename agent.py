import os
import asyncio
# Import the warnings module
import warnings 
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mem0 import MemoryClient
from dotenv import load_dotenv

# --- Warning Suppression ---
# Suppress all warnings for a cleaner console output during the chat session.
# NOTE: This is generally only recommended for clean terminal output in simple scripts,
# as it hides potentially important issues in a production environment.
warnings.filterwarnings("ignore")

load_dotenv()

# --- Memory Client Initialization ---
try:
    # Initialize Mem0 client
    mem0 = MemoryClient()
except Exception as e:
    # Print the initialization error but continue with placeholder functions
    print(f"Error initializing Mem0 client (memory features disabled): {e}")
    mem0 = None

# --- Define memory function tools ---
# Check if mem0 is initialized before defining functions that use it
if mem0:
    def search_memory(query: str, user_id: str) -> dict:
        """Search through past conversations and memories"""
        filters = {"user_id": user_id}
        try:
            memories = mem0.search(query, filters=filters)
            if memories.get('results', []):
                memory_list = memories['results']
                memory_context = "\n".join([f"- {mem['memory']}" for mem in memory_list])
                return {"status": "success", "memories": memory_context}
            return {"status": "no_memories", "message": "No relevant memories found"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to search memory: {str(e)}"}

    def save_memory(content: str, user_id: str) -> dict:
        """Save important information to memory"""
        try:
            result = mem0.add([{"role": "user", "content": content}], user_id=user_id)
            return {"status": "success", "message": "Information saved to memory", "result": result}
        except Exception as e:
            return {"status": "error", "message": f"Failed to save memory: {str(e)}"}
else:
    # Define placeholder functions if mem0 failed to initialize
    def search_memory(query: str, user_id: str) -> dict:
        return {"status": "error", "message": "Memory client not initialized."}
    def save_memory(content: str, user_id: str) -> dict:
        return {"status": "error", "message": "Memory client not initialized."}


# --- Create agent with memory capabilities ---
root_agent = Agent(
    name="personal_assistant",
    model="gemini-2.0-flash",
    instruction="""You are a helpful personal assistant with memory capabilities.
    Use the search_memory function to recall past conversations and user preferences.
    Use the save_memory function to store important information about the user.
    Always personalize your responses based on available memory.""",
    description="A personal assistant that remembers user preferences and past interactions",
    tools=[search_memory, save_memory]
)
