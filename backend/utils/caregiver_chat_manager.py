from utils.ai_manager import get_query_intent
from utils.action_resolver import resolve_action


def process_caregiver_query(query_text: str, senior_id: str) -> str:
    """Processes a caregiver's text query and returns a text response."""

    intent_data = get_query_intent(query_text)
    intent = intent_data.get("intent", "unknown")
    entities = intent_data.get("entities", {})

    response_text = resolve_action(intent, senior_id, entities)

    return response_text
