"""Lightweight lookalike-domain checks; heuristic only."""
from difflib import SequenceMatcher
PROTECTED_BRANDS={"google":["google.com"],"microsoft":["microsoft.com","live.com","outlook.com"],"apple":["apple.com","icloud.com"],"amazon":["amazon.com","amazon.in"],"paypal":["paypal.com"],"facebook":["facebook.com"],"instagram":["instagram.com"],"netflix":["netflix.com"],"github":["github.com"],"linkedin":["linkedin.com"],"sbi":["sbi.co.in"],"hdfc":["hdfcbank.com"]}
def find_lookalikes(hostname: str) -> list:
    host=hostname.lower().strip("."); matches=[]
    noise={"login","secure","verify","account","online","support","service","bank","auth","update","signin"}
    for brand,domains in PROTECTED_BRANDS.items():
        if host in domains or any(host.endswith("."+d) for d in domains): continue
        best=0.0
        for label in host.split("."):
            tokens=[t for t in label.replace("_","-").split("-") if t and t not in noise]
            compact="".join(tokens).translate(str.maketrans({"1":"l","0":"o","3":"e","5":"s"}))
            if not compact: continue
            score=SequenceMatcher(None,compact,brand).ratio()
            if score>=0.72 or (brand in compact and len(compact)<=len(brand)+5): best=max(best,score)
        if best: matches.append({"brand":brand,"similarity":round(best,2)})
    return sorted(matches,key=lambda x:x["similarity"],reverse=True)[:3]
