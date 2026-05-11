import re
from datetime import datetime

# Pramana Classification Rules (Sutra 65: Nyaya Pramana System)
# These are the "epistemic token classifiers"

PRATYAKSHA_KEYWORDS = [
    "observed", "measured", "tested", "saw", "recorded",
    "experiment", "data shows", "results indicate",
    "photograph", "video shows", "directly witnessed"
]

ANUMANA_KEYWORDS = [
    "therefore", "implies", "suggests", "indicates",
    "likely", "probability", "trend", "correlation",
    "if.*then", "because", "thus", "consequently",
    "inferred", "deduced", "reasoned"
]

UPAMANA_KEYWORDS = [
    "similar to", "like", "analogous", "comparable",
    "resembles", "just as", "same as", "parallel to",
    "reminds of", "akin to", "comparable to"
]

SHABDA_KEYWORDS = [
    "according to", "reportedly", "sources say",
    "experts claim", "studies show", "research published",
    "announced", "stated", "said", "told reporters",
    "the paper claims", "allegedly", "purportedly"
]

# Hallucination indicators (claims without epistemic grounding)
HALLUCINATION_FLAGS = [
    (r"(scientists|researchers|experts)\s+(say|claim|believe|proved|discovered)",
     "Anonymous authority appeal"),
    (r"(studies|research)\s+(show|prove|demonstrate|confirm)",
     "Citation without reference"),
    (r"(it is known that|everyone knows|obviously|clearly)",
     "Assertion without evidence"),
    (r"(always|never|all|none|every|no one)\s",
     "Absolute claim (high epistemic burden)"),
    (r"(breakthrough|revolutionary|game.changing|miracle)",
     "Hype language (emotional manipulation)"),
]

def classify_pramana(text):
    """
    Sutra 65 Implementation: Epistemic Token Classifier
    Returns the Pramana source type for the text.
    """
    text_lower = text.lower()
    
    # Count keyword matches per category
    scores = {
        "Pratyaksha (Direct Perception)": 0,
        "Anumana (Inference)": 0,
        "Upamana (Comparison)": 0,
        "Shabda (Testimony)": 0
    }
    
    for kw in PRATYAKSHA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Pratyaksha (Direct Perception)"] += 1
    
    for kw in ANUMANA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Anumana (Inference)"] += 1
    
    for kw in UPAMANA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Upamana (Comparison)"] += 1
    
    for kw in SHABDA_KEYWORDS:
        if re.search(kw, text_lower):
            scores["Shabda (Testimony)"] += 1
    
    # Primary classification (highest match)
    primary = max(scores, key=scores.get)
    
    # If no clear signal, default based on structure
    if sum(scores.values()) == 0:
        if re.search(r"(I|we)\s+(think|believe|feel)", text_lower):
            primary = "Anumana (Inference)"
        else:
            primary = "Shabda (Testimony) [unverified]"
    
    return primary, scores

def detect_hallucination_flags(text):
    """
    Runtime Receipt Verification (Sutra 65)
    Flags potential hallucinations in real-time.
    """
    flags = []
    for pattern, explanation in HALLUCINATION_FLAGS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            flags.append({
                "pattern": pattern,
                "matched": matches[0] if isinstance(matches[0], str) else str(matches[0]),
                "explanation": explanation
            })
    return flags

def generate_five_step_scaffold(claim):
    """
    Sutra 65: Pancha Avayava (5-Step Reasoning Scaffold)
    Generates structured reasoning for any claim.
    """
    primary_source, _ = classify_pramana(claim)
    flags = detect_hallucination_flags(claim)
    
    # Build the 5 steps
    pratijna = f"Claim: '{claim[:100]}{'...' if len(claim) > 100 else ''}'"
    
    hetu = f"Epistemic Source: {primary_source}"
    if flags:
        hetu += f" | ⚠️ {len(flags)} potential grounding issue(s) detected"
    
    udaharana = "Example verification: "
    if primary_source == "Pratyaksha (Direct Perception)":
        udaharana += "Can be verified through direct observation or measurement."
    elif primary_source == "Anumana (Inference)":
        udaharana += "Requires examination of the logical chain and premises."
    elif primary_source == "Upamana (Comparison)":
        udaharana += "Requires verification of the base comparison object."
    else:
        udaharana += "Requires citation of the original source/testimony."
    
    if flags:
        upanaya = f"Application: This claim contains {len(flags)} ungrounded elements. Treat with caution."
    else:
        upanaya = "Application: This claim is well-grounded in its primary epistemic category."
    
    nigamana = "Conclusion: "
    if len(flags) >= 2:
        nigamana += "❌ HIGH RISK OF HALLUCINATION. Seek direct evidence before accepting."
    elif len(flags) == 1:
        nigamana += "⚠️ MODERATE RISK. Verify the flagged element."
    else:
        nigamana += "✅ LOW RISK. Claim appears epistemically grounded."
    
    return {
        "Pratijna (Hypothesis)": pratijna,
        "Hetu (Reason)": hetu,
        "Udaharana (Example)": udaharana,
        "Upanaya (Application)": upanaya,
        "Nigamana (Conclusion)": nigamana
    }

def calculate_pramana_score(text):
    """
    Calculates a 0-100 truth confidence score based on epistemic grounding.
    """
    _, scores = classify_pramana(text)
    flags = detect_hallucination_flags(text)
    
    base_score = 50
    
    # Bonus for direct sources
    base_score += scores["Pratyaksha (Direct Perception)"] * 10
    base_score += scores["Anumana (Inference)"] * 5
    
    # Penalty for unverified testimony
    base_score -= scores["Shabda (Testimony)"] * 5
    
    # Penalty for hallucination flags
    base_score -= len(flags) * 15
    
    # Penalty for hype/absolutes
    hype_count = len(re.findall(r'(breakthrough|revolutionary|miracle|cure.all)', text, re.IGNORECASE))
    base_score -= hype_count * 10
    
    return max(0, min(100, base_score))

def analyze_claim(claim):
    """
    Main analysis function - combines all Sutra 65 components.
    """
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

# ==================== MAIN INTERFACE ====================

def print_banner():
    banner = """
╔══════════════════════════════════════════════╗
║        NYAYA LENS — Truth Verification        ║
║  Hallucination Detection via 2,500-yr Logic   ║
║    Sutra 65: Pramana-Nyaya Epistemic Kernel   ║
╚══════════════════════════════════════════════╝
    """
    print(banner)

def print_analysis(result):
    print("\n" + "="*50)
    print("📊 PRAMANA SCORE:", result['pramana_score'], "/ 100")
    print("="*50)
    
    print(f"\n🔍 PRIMARY SOURCE: {result['primary_source']}")
    
    print("\n📈 SOURCE DISTRIBUTION:")
    for source, score in result['source_scores'].items():
        bar = "█" * score
        print(f"  {source}: {bar} ({score})")
    
    print("\n" + "="*50)
    print("🧠 5-STEP REASONING (Pancha Avayava)")
    print("="*50)
    for step, content in result['five_step_scaffold'].items():
        print(f"\n  {step}:")
        print(f"  {content}")
    
    if result['hallucination_flags']:
        print("\n" + "="*50)
        print("⚠️  HALLUCINATION FLAGS DETECTED")
        print("="*50)
        for i, flag in enumerate(result['hallucination_flags'], 1):
            print(f"\n  Flag {i}: {flag['explanation']}")
            print(f"  Pattern matched: '{flag['matched']}'")
    
    print("\n" + "="*50)

def main():
    print_banner()
    
    while True:
        print("\n" + "-"*50)
        print("Enter a claim to verify (or 'quit' to exit):")
        print("-"*50)
        
        claim = input("\n> ")
        
        if claim.lower() in ['quit', 'exit', 'q']:
            print("\n🙏 Nyaya Lens shutting down. Satyameva Jayate.")
            break
        
        if not claim.strip():
            continue
        
        print("\n⏳ Analyzing claim through Nyaya Pramana system...")
        result = analyze_claim(claim)
        print_analysis(result)

if __name__ == "__main__":
    main()
