import logging
import os

from dotenv import load_dotenv

from server.utils.trello_api import TrelloClient

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# Initialize Trello client and service
try:
    api_key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    if not api_key or not token:
        raise ValueError(
            "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
        )
    client = TrelloClient(api_key=api_key, token=token)
    logger.info("Trello client and service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Trello client: {str(e)}")
    raise


# Add a prompt for common Trello operations
def trello_help() -> str:
    """Provides help information about available Trello operations."""
    return """
    Available Trello Operations:
    1. Board Operations:
       - Get a specific board
       - List all boards
       - Get board labels
       - Add label to a board
    2. List Operations:
       - Get a specific list
       - List all lists in a board
       - Create a new list
       - Update a list's name
       - Archive a list
    3. Card Operations:
       - Get a specific card
       - List all cards in a list
       - Create a new card
       - Update a card's attributes
       - Delete a card
    4. Comment & Attachment Operations:
       - Get all comments on a card
       - Add a comment to a card (supports markdown and @mentions)
       - Update an existing comment
       - Delete a comment
       - Get all attachments on a card
       - Add a URL attachment to a card
       - Delete an attachment
    5. Checklist Operations:
       - Get a specific checklist
       - List all checklists in a card
       - Create a new checklist
       - Update a checklist
       - Delete a checklist
       - Add checkitem to checklist
       - Update checkitem
       - Delete checkitem
    """
