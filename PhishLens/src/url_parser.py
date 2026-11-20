"""Safe, offline URL parsing helpers."""
from urllib.parse import urlsplit, unquote
import ipaddress, re
SCHEME_RE=re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
def parse_url(raw_url: str) -> dict:
    if not isinstance(raw_url,str) or not raw_url.strip(): raise ValueError("Enter a URL to analyse.")
    raw=raw_url.strip()
    if len(raw)>2048: raise ValueError("URL is too long (maximum 2,048 characters).")
    candidate=raw if SCHEME_RE.match(raw) else "http://"+raw
    try: parts=urlsplit(candidate); hostname=parts.hostname or ""; port=parts.port
    except ValueError as exc: raise ValueError("The URL format or port is invalid.") from exc
    if not hostname or any(ch.isspace() for ch in hostname): raise ValueError("Enter a valid URL containing a hostname.")
    try: ascii_host=hostname.encode("idna").decode("ascii").lower().rstrip(".")
    except UnicodeError as exc: raise ValueError("The hostname could not be parsed safely.") from exc
    try: ipaddress.ip_address(ascii_host); is_ip=True
    except ValueError: is_ip=False
    return {"raw":raw,"scheme":parts.scheme.lower(),"hostname":ascii_host,"path":unquote(parts.path or "/"),"query":parts.query,"fragment":parts.fragment,"port":port,"username_present":parts.username is not None,"password_present":parts.password is not None,"is_ip":is_ip,"has_query":bool(parts.query),"url_length":len(raw),"subdomain_count":max(0,len(ascii_host.split("."))-2)}
