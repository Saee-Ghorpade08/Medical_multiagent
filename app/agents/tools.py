from agno.tools import tool
from app.data.sample_documents import search_library as search_local_library


@tool
def search_library(query: str) -> str:
    """Search the local educational medical research notes for a topic."""
    results = search_local_library(query, limit=3)
    if not results:
        return "No matching note was found in the local sample library."
    return "\n\n".join(f"Source: {item['title']}\n{item['content']}" for item in results)
