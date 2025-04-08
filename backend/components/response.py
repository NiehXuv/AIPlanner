# backend/components/response.py
def clean_gemini_response(response_text: str) -> str:
    """Clean Gemini response by removing Markdown code block formatting."""
    cleaned = response_text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-len("```")].strip()
    return cleaned