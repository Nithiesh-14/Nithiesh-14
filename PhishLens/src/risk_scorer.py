"""Explainable weighted risk score."""
def score_url(flags: list, lookalikes: list) -> dict:
    reasons=list(flags)
    if lookalikes:
        best=lookalikes[0]; reasons.append({"code":"lookalike_domain","title":"Possible brand lookalike domain","detail":f"The hostname resembles '{best['brand']}' (similarity {best['similarity']:.0%}). This is heuristic, not proof of impersonation.","points":24})
    score=min(100,sum(x["points"] for x in reasons))
    if score>=60: level,label,advice="high","High risk","Do not enter credentials or payment details. Verify the domain through an independently obtained official source."
    elif score>=30: level,label,advice="medium","Suspicious","Treat this URL cautiously. Check the exact domain and navigate to the service directly if needed."
    else: level,label,advice="low","No major red flags detected","No major heuristic warning was found. This does not guarantee the site is safe."
    return {"score":score,"level":level,"label":label,"advice":advice,"reasons":reasons}
