"""Deterministic URL red-flag extraction."""
import re
SUSPICIOUS_TLDS={".zip",".mov",".click",".country",".kim",".work",".top",".xyz",".gq",".tk"}
SUSPICIOUS_TERMS={"login":7,"verify":8,"verification":8,"account":5,"password":9,"signin":7,"secure":4,"update":5,"wallet":7,"banking":7,"payment":6,"invoice":5,"confirm":5,"reset":5,"suspend":9,"urgent":7,"free-gift":7,"gift":3,"claim":5}
SHORTENERS={"bit.ly","tinyurl.com","t.co","is.gd","cutt.ly","rebrand.ly"}
def detect_patterns(parsed: dict) -> list:
    flags=[]; host=parsed["hostname"]; full=(host+parsed["path"]+"?"+parsed["query"]).lower()
    def add(code,title,detail,points): flags.append({"code":code,"title":title,"detail":detail,"points":points})
    if parsed["scheme"]!="https": add("no_https","Connection is not HTTPS","The URL uses HTTP. Data sent to the site may not be encrypted.",10)
    if parsed["is_ip"]: add("ip_host","IP address used as hostname","The destination is an IP address rather than a conventional domain name.",18)
    if parsed["username_present"] or parsed["password_present"]: add("userinfo","Embedded credentials in URL","The URL contains user-info before the hostname, a pattern sometimes used to disguise destinations.",20)
    if parsed["subdomain_count"]>=3: add("many_subdomains","Unusually deep subdomain chain",f"The hostname contains {parsed['subdomain_count']} subdomain label(s).",10)
    if parsed["url_length"]>100: add("long_url","Unusually long URL",f"The URL is {parsed['url_length']} characters long.",8)
    if parsed["port"] not in (None,80,443): add("nonstandard_port","Non-standard port",f"The URL specifies port {parsed['port']}.",8)
    if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS): add("uncommon_tld","Higher-risk TLD pattern","This TLD appears in abuse reports; it does not prove maliciousness.",8)
    if host in SHORTENERS: add("shortener","URL shortener detected","The final destination is hidden behind a URL-shortening service.",8)
    if re.search(r"xn--",host): add("punycode","Internationalized hostname encoding","The hostname contains punycode. Check carefully for lookalike characters.",12)
    if host.count("-")>=3: add("hyphens","Many hyphens in hostname","Multiple hyphens can be used to imitate trusted brand domains.",6)
    matched=[term for term in SUSPICIOUS_TERMS if term in full]
    if matched: add("keywords","Sensitive-action keywords","URL contains: "+", ".join(matched[:6])+("…" if len(matched)>6 else ""),min(18,sum(SUSPICIOUS_TERMS[t] for t in matched)))
    if "%" in parsed["raw"]: add("encoding","Percent-encoded URL characters","Encoded characters can obscure the visible destination or path.",4)
    return flags
