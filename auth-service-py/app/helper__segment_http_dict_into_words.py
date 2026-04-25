import urllib.parse
import re
from typing import Dict, List

# Split ONLY on major HTTP delimiters, not symbols
DELIMITER_REGEX = re.compile(r"[/?&=\s]+")

def segment_http_dict_into_words(request: Dict) -> List[str]:
    """
    Preprocess an HTTP request JSON object to extract segmented words
    without destroying attack payloads.
    """

    tokens = []

    # 1. HTTP method
    method = request.get("method", "")
    if method:
        tokens.append(method.upper())

    # 2. URL parsing
    raw_url = request.get("url", "")
    decoded_url = urllib.parse.unquote(raw_url)

    parsed = urllib.parse.urlparse(decoded_url)

    # --- Path tokens ---
    tokens.extend(segment_preserving_symbols(parsed.path))

    # --- Query tokens ---
    tokens.extend(segment_preserving_symbols(parsed.query))

    # 3. Request body
    body = request.get("data", "")
    if body:
        decoded_body = urllib.parse.unquote(body)
        tokens.extend(segment_preserving_symbols(decoded_body))

    return [t for t in tokens if t]


def segment_preserving_symbols(text: str) -> List[str]:
    """
    Split text into tokens while preserving symbolic attack payloads.
    """
    if not text:
        return []

    text = text.strip().lower()

    # Split only on HTTP delimiters
    tokens = DELIMITER_REGEX.split(text)

    return tokens
