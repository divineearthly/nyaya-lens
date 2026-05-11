import re
from datetime import datetime

PRATYAKSHA_KEYWORDS = [
    "I measured", "I saw", "I observed", "I recorded", "I tested",
    "I witnessed", "I heard", "I counted", "I weighed",
    "reading was", "the meter showed", "my observation",
    "personally observed", "first-hand", "directly witnessed",
    "I found", "I noticed", "I detected"
]

ANUMANA_KEYWORDS = [
    "therefore", "implies", "suggests", "indicates",
    "likely", "probability", "trend", "correlation",
    "because", "thus", "consequently", "probably",
    "might be", "could be", "appears to",
    "the pattern shows", "this means", "so the",
    "chances are", "odds are", "estimated"
]

UPAMANA_KEYWORDS = [
    "similar to", "like", "analogous", "comparable",
    "resembles", "just as", "same as", "parallel to",
    "reminds of", "akin to", "comparable to",
    "in the same way", "similarly", "likewise"
]

SHABDA_KEYWORDS = [
    "according to", "reportedly", "sources say",
    "experts claim", "studies show", "announced",
    "stated", "said", "told reporters",
    "allegedly", "purportedly", "reported by",
    "officials confirmed", "government announced",
    "sources confirmed", "media reports",
    "has launched", "has announced", "has revealed",
    "successfully tested", "conducted a", "highlighted",
    "the times of", "the hindu", "the economic times",
    "times of india", "hindustan times", "reported"
]

HALLUCINATION_FLAGS = [
    (r"(scientists|researchers|experts)\s+(say|claim|believe|proved|discovered|have just|revealed)",
     "Anonymous authority — no named individual or institution"),
    (r"(studies|research)\s+(show|prove|demonstrate|confirm)",
     "Citation without specific reference (which study? published where?)"),
    (r"(it is known that|everyone knows|obviously|clearly|undoubtedly|without doubt)",
     "Bare assertion — stated as fact without supporting evidence"),
    (r"\b(always|never|all|none|every|no one)\b",
     "Absolute claim — requires extraordinary evidence"),
    (r"(breakthrough|revolutionary|game.?changing|miracle|cure.?all|magic)",
     "Hype/clickbait language — reduces credibility"),
    (r"within\s+\d+\s+(days?|hours?|minutes?)",
     "Suspiciously specific immediate-result claim"),
    (r"with zero\s+(side effects|effort|cost|risk)",
     "Zero-downside claim — statistically improbable"),
    (r"(completely|100%|perfectly)\s+(cures?|eliminates?|solves?|prevents?)",
     "Oversimplified total-solution claim"),
    (r"[❤️🔥💯😱🚨‼️🎉🙏💪🧪]",
     "Emoji-laden — emotional manipulation, not evidence"),
]

def classify_pramana(text):
    text_lower = text.lower()
    scores = {
        "Pratyaksha (Direct Observation)": 0,
        "Anumana (Logical Inference)": 0,
        "Upamana (Comparison/Analogy)": 0,
        "Shabda (Testimony/Report)": 0
    }
    for kw in PRATYAKSHA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Pratyaksha (Direct Observation)"] += 1
    for kw in ANUMANA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Anumana (Logical Inference)"] += 1
    for kw in UPAMANA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Upamana (Comparison/Analogy)"] += 1
    for kw in SHABDA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Shabda (Testimony/Report)"] += 1
    
    news_markers = ["announced", "launched", "reported", "confirmed", "stated", "highlighted"]
    if any(m in text_lower for m in news_markers) and not re.search(r"\bI\s+(measured|saw|observed|tested)", text_lower):
        scores["Shabda (Testimony/Report)"] += 2
    
    primary = max(scores, key=scores.get)
    if sum(scores.values()) == 0:
        if re.search(r"(I|we)\s+(think|believe|feel)", text_lower):
            primary = "Anumana (Logical Inference)"
        else:
            primary = "Shabda (Testimony/Report) [unverified]"
    return primary, scores

def detect_hallucination_flags(text):
    flags = []
    for pattern, explanation in HALLUCINATION_FLAGS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            flags.append({
                "pattern": pattern,
                "matched": str(matches[0]) if matches else "",
                "explanation": explanation
            })
    return flags

def generate_five_step_scaffold(claim):
    primary_source, _ = classify_pramana(claim)
    flags = detect_hallucination_flags(claim)
    
    pratijna = f"Claim analyzed: '{claim[:150]}{'...' if len(claim) > 150 else ''}'"
    
    hetu = f"Primary epistemic source identified as: {primary_source}"
    if flags:
        hetu += f" | {len(flags)} grounding issue(s) detected"
    
    udaharana = "Verification method: "
    if "Pratyaksha" in primary_source:
        udaharana += "This claim can be verified through direct measurement or personal observation. Anyone present could confirm."
    elif "Anumana" in primary_source:
        udaharana += "This is a logical inference. Check whether the premises are true and the reasoning is valid."
    elif "Upamana" in primary_source:
        udaharana += "This uses comparison. Verify that the base comparison is accurate and the analogy holds."
    else:
        udaharana += "This is reported testimony. To verify: locate the original source, named authority, or official announcement."
    
    upanaya = "Practical application: "
    if len(flags) >= 3:
        upanaya += "Multiple credibility red flags. Treat this claim with high skepticism. Do not share without verification."
    elif len(flags) >= 2:
        upanaya += "Two or more grounding issues detected. Cross-check with primary sources before accepting."
    elif len(flags) == 1:
        upanaya += "One element lacks proper grounding. Verify that specific part before accepting the full claim."
    else:
        upanaya += "This claim appears properly structured. Proceed with appropriate caution for its source type."
    
    nigamana = "Final verdict: "
    if len(flags) >= 3:
        nigamana += "HIGH RISK — Multiple indicators of potential misinformation. Requires direct evidence from a named, verifiable source."
    elif len(flags) >= 2:
        nigamana += "MODERATE-HIGH RISK — Several credibility concerns. Seek primary source before relying on this information."
    elif len(flags) == 1:
        nigamana += "MODERATE RISK — One unverified element detected. Quick fact-check recommended."
    else:
        if "Pratyaksha" in primary_source:
            nigamana += "LOW RISK — Based on direct observation. Reliable if the observer has no reason to deceive."
        elif "Anumana" in primary_source:
            nigamana += "LOW-MODERATE RISK — Logical inference. Sound conclusion if the underlying facts are correct."
        elif "Upamana" in primary_source:
            nigamana += "MODERATE RISK — Analogical reasoning. Only as strong as the comparison itself."
        else:
            nigamana += "CAUTION — This is second-hand information. Always seek the original source before citing as fact."
    
    return {
        "1. Pratijna (Hypothesis)": pratijna,
        "2. Hetu (Reason/Grounding)": hetu,
        "3. Udaharana (Example/Verification)": udaharana,
        "4. Upanaya (Application)": upanaya,
        "5. Nigamana (Conclusion)": nigamana
    }

def calculate_pramana_score(text):
    _, scores = classify_pramana(text)
    flags = detect_hallucination_flags(text)
    
    base_score = 50
    base_score += scores["Pratyaksha (Direct Observation)"] * 20
    base_score += scores["Anumana (Logical Inference)"] * 10
    base_score += scores["Upamana (Comparison/Analogy)"] * 6
    base_score -= scores["Shabda (Testimony/Report)"] * 6
    base_score -= len(flags) * 15
    
    hype_count = len(re.findall(r'(breakthrough|revolutionary|miracle|cure.all|instant|magic|amazing|incredible)', text, re.IGNORECASE))
    base_score -= hype_count * 10
    absolute_count = len(re.findall(r'\b(always|never|all|none|every|no one|perfectly|completely)\b', text, re.IGNORECASE))
    base_score -= absolute_count * 6
    emoji_count = len(re.findall(r'[❤️🔥💯😱🚨‼️🎉🙏💪🧪]', text))
    base_score -= emoji_count * 4
    
    specific_detail = len(re.findall(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', text))
    specific_detail += len(re.findall(r'\b\d{1,2}\s(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b', text))
    base_score += min(specific_detail * 5, 20)
    
    return max(0, min(100, base_score))

def analyze_claim(claim):
    primary_source, source_scores = classify_pramana(claim)
    flags = detect_hallucination_flags(claim)
    scaffold = generate_five_step_scaffold(claim)
    pramana_score = calculate_pramana_score(claim)
    return {
        "timestamp": datetime.now().isoformat(),
        "claim": claim,
        "primary_source": primary_source,
        "source_scores": source_scores,
        "pramana_score": pramana_score,
        "hallucination_flags": flags,
        "five_step_scaffold": scaffold
    }

def print_banner():
    banner = """
╔══════════════════════════════════════════════╗
║        NYAYA LENS — Truth Verification       ║
║  Hallucination Detection via 2,500-yr Logic  ║
║    Sutra 65: Pramana-Nyaya Epistemic Kernel  ║
╚══════════════════════════════════════════════╝
    """
    print(banner)

def print_analysis(result):
    print("\n" + "="*50)
    print("PRAMANA SCORE:", result['pramana_score'], "/ 100")
    print("="*50)
    print(f"\nPRIMARY SOURCE: {result['primary_source']}")
    print("\nSOURCE DISTRIBUTION:")
    for source, score in result['source_scores'].items():
        bar = "█" * score
        print(f"  {source}: {bar} ({score})")
    print("\n" + "="*50)
    print("5-STEP REASONING (Pancha Avayava)")
    print("="*50)
    for step, content in result['five_step_scaffold'].items():
        print(f"\n  {step}:")
        print(f"  {content}")
    if result['hallucination_flags']:
        print("\n" + "="*50)
        print("HALLUCINATION FLAGS DETECTED")
        print("="*50)
        for i, flag in enumerate(result['hallucination_flags'], 1):
            print(f"\n  Flag {i}: {flag['explanation']}")
            print(f"  Matched: '{flag['matched']}'")
    print("\n" + "="*50)

def main():
    print_banner()
    while True:
        print("\n" + "-"*50)
        print("Enter a claim to verify (or 'quit' to exit):")
        print("-"*50)
        claim = input("\n> ")
        if claim.lower() in ['quit', 'exit', 'q']:
            print("\nNyaya Lens shutting down. Satyameva Jayate.")
            break
        if not claim.strip():
            continue
        print("\nAnalyzing claim through Nyaya Pramana system...")
        result = analyze_claim(claim)
        print_analysis(result)

if __name__ == "__main__":
    main()
