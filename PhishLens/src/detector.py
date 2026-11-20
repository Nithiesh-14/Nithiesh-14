from .url_parser import parse_url
from .pattern_detector import detect_patterns
from .domain_similarity import find_lookalikes
from .risk_scorer import score_url
def analyze_url(raw_url: str) -> dict:
    parsed=parse_url(raw_url); flags=detect_patterns(parsed); lookalikes=find_lookalikes(parsed["hostname"]); risk=score_url(flags,lookalikes)
    return {"input":parsed["raw"],"hostname":parsed["hostname"],"scheme":parsed["scheme"],"risk":risk,"lookalikes":lookalikes,"summary":f"PhishLens found {len(risk['reasons'])} signal(s) to review.","disclaimer":"Heuristic demonstration only. PhishLens does not visit the URL, query threat-intelligence feeds, or certify that a website is safe or malicious."}
