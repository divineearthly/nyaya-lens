from flask import Flask, render_template_string, request
from nyaya_lens import analyze_claim
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    claim = ''
    if request.method == 'POST':
        claim = request.form.get('claim', '')
        if claim.strip():
            analysis = analyze_claim(claim)
            score = analysis['pramana_score']
            result = {
                'pramana_score': score,
                'primary_source': analysis['primary_source'],
                'source_scores': analysis['source_scores'],
                'five_step_scaffold': analysis['five_step_scaffold'],
                'hallucination_flags': analysis['hallucination_flags']
            }
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nyaya Lens — Truth Verification</title>
<style>
:root{--bg:#0d0d1a;--card:#13132b;--input:#1a1a3a;--border:#2a2a5a;--text:#d0d0e0;--dim:#7878a0;--gold:#f0b040;--red:#e94560;--green:#4ecca3;--purple:#7b4fd8}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:16px}
.container{max-width:680px;margin:0 auto}
.hero{text-align:center;padding:32px 0 24px}
.hero h1{font-size:32px;background:linear-gradient(135deg,#f0b040,#ff6b35);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:800}
.hero .tagline{color:var(--dim);font-size:13px;margin-top:4px}
.info-row{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.info-chip{flex:1;min-width:100px;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px;text-align:center;font-size:12px;color:var(--dim)}
.info-chip strong{display:block;color:var(--text);font-size:16px}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px;margin-bottom:16px}
.card-label{font-size:13px;font-weight:600;color:var(--dim);text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}
textarea{width:100%;min-height:120px;padding:14px;background:var(--input);color:var(--text);border:1px solid var(--border);border-radius:12px;font-size:15px;line-height:1.5;resize:vertical;font-family:inherit}
textarea:focus{outline:none;border-color:var(--gold)}
.btn{display:block;width:100%;padding:16px;background:linear-gradient(135deg,#f0b040,#e08030);color:#0d0d1a;border:none;border-radius:14px;font-size:17px;font-weight:700;cursor:pointer;margin-top:12px}
.quick-tests{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.quick-btn{flex:1;min-width:80px;padding:10px;background:var(--input);color:var(--dim);border:1px solid var(--border);border-radius:10px;font-size:11px;cursor:pointer}
.result-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px}
.score-ring{width:130px;height:130px;border-radius:50%;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;border:6px solid;font-size:42px;font-weight:900}
.score-ring.green{border-color:var(--green);color:var(--green);box-shadow:0 0 30px rgba(78,204,163,0.2)}
.score-ring.yellow{border-color:var(--gold);color:var(--gold);box-shadow:0 0 30px rgba(240,176,64,0.2)}
.score-ring.red{border-color:var(--red);color:var(--red);box-shadow:0 0 30px rgba(233,69,96,0.2)}
.score-label{text-align:center;font-size:13px;color:var(--dim);margin-bottom:20px}
.score-emoji{text-align:center;font-size:36px;margin-bottom:8px}
.source-badge{display:inline-block;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:600;margin:0 auto 16px;display:block;width:fit-content}
.source-badge.pratyaksha{background:rgba(78,204,163,0.15);color:var(--green)}
.source-badge.anumana{background:rgba(240,176,64,0.15);color:var(--gold)}
.source-badge.upamana{background:rgba(123,79,216,0.15);color:#a78bfa}
.source-badge.shabda{background:rgba(233,69,96,0.15);color:var(--red)}
.step{background:var(--input);padding:12px 14px;border-radius:10px;margin-bottom:8px;font-size:13px;line-height:1.5;border-left:3px solid var(--border)}
.step strong{color:var(--gold);font-size:11px;text-transform:uppercase;display:block;margin-bottom:2px}
.flags-section{margin-top:16px;background:rgba(233,69,96,0.08);border:1px solid rgba(233,69,96,0.25);border-radius:12px;padding:16px}
.flags-section h3{color:var(--red);font-size:14px;margin-bottom:10px}
.flag{padding:8px 12px;background:rgba(233,69,96,0.1);border-radius:8px;margin-bottom:6px;font-size:12px;color:#ff8a9e}
.footer{text-align:center;padding:24px;color:var(--dim);font-size:11px}
.pricing-card{text-align:center;padding:24px;background:linear-gradient(135deg,#1a1a3a,#0f0f2a);border:2px solid #f0b040;border-radius:16px;margin:20px auto;max-width:680px}
.pricing-card h3{color:#f0b040;font-size:22px}
.pricing-card a{display:inline-block;padding:12px 24px;background:#f0b040;color:#0d0d1a;border-radius:10px;text-decoration:none;font-weight:700;margin:8px}
.pricing-card .upi-btn{background:#4ecca3}
</style>
</head>
<body>
<div class="container">
<div class="hero"><h1>Nyaya Lens</h1><p class="tagline">Truth detection engine — 2,500-year-old Indian formal logic</p></div>
<div class="info-row">
<div class="info-chip">🔍<br>Analyzes <strong>any text</strong><br>AI, news, claims, posts</div>
<div class="info-chip">🧠<br>Based on <strong>Sutra 65</strong><br>Pramana-Nyaya logic</div>
<div class="info-chip">⚡<br>Runs <strong>100% offline</strong><br>No API, no tracking</div>
</div>
<div class="card">
<div class="card-label">Paste any claim or AI-generated text</div>
<form method="POST"><textarea name="claim" id="claimInput" placeholder="Example: Scientists have proved that drinking green tea cures all types of cancer overnight...">''' + (claim or '') + '''</textarea>
<button type="submit" class="btn">Analyze Truth</button></form>
<div class="quick-tests">
<button class="quick-btn" onclick="document.getElementById('claimInput').value='BREAKING: Scientists have just proved that drinking turmeric tea cures all types of cancer within 3 days with zero side effects.';this.form.submit()">Fake Claim</button>
<button class="quick-btn" onclick="document.getElementById('claimInput').value='The leaves are turning yellow and the soil feels dry, so the plant probably needs water.';this.form.submit()">Inference</button>
<button class="quick-btn" onclick="document.getElementById('claimInput').value='I measured the soil pH with a digital meter at 9:00 AM today. The reading was 6.8.';this.form.submit()">Observation</button>
<button class="quick-btn" onclick="document.getElementById('claimInput').value='According to a new study, researchers claim AI will replace 40% of jobs by 2030.';this.form.submit()">News Style</button>
</div>
</div>
'''
    
    if result:
        score = result['pramana_score']
        if score >= 70:
            emoji, ring_class, label = '✅', 'green', 'High'
        elif score >= 40:
            emoji, ring_class, label = '🤔', 'yellow', 'Moderate'
        else:
            emoji, ring_class, label = '🚨', 'red', 'Low'
        
        source = result['primary_source']
        if 'Pratyaksha' in source:
            badge_class = 'pratyaksha'; badge_icon = '👁️'
        elif 'Anumana' in source:
            badge_class = 'anumana'; badge_icon = '🧠'
        elif 'Upamana' in source:
            badge_class = 'upamana'; badge_icon = '🔄'
        else:
            badge_class = 'shabda'; badge_icon = '📢'
        
        html += f'<div class="result-card"><div class="score-emoji">{emoji}</div><div class="score-ring {ring_class}">{score}</div><div class="score-label">Truth Confidence — {label}</div><span class="source-badge {badge_class}">{badge_icon} {source}</span><div class="steps"><div class="card-label">5-Step Reasoning (Pancha Avayava)</div>'
        
        for step, content in result['five_step_scaffold'].items():
            html += f'<div class="step"><strong>{step}</strong>{content}</div>'
        html += '</div>'
        
        if result['hallucination_flags']:
            html += f'<div class="flags-section"><h3>Hallucination Indicators ({len(result["hallucination_flags"])})</h3>'
            for flag in result['hallucination_flags']:
                html += f'<div class="flag">{flag["explanation"]}</div>'
            html += '</div>'
        html += '</div>'
    
    html += '''
<div class="pricing-card">
<h3>Get API Access — $9/month</h3>
<p style="color:#d0d0e0;margin:10px 0;">Add truth verification to your AI app</p>
<p style="font-size:14px;">📧 divineearthly@gmail.com</p>
<p style="font-size:14px;">📧 jdas794@gmail.com</p>
<p style="font-size:14px;">💳 UPI: divinesouljoy@pnb</p>
<p style="font-size:12px;color:#a0a0b0;margin:10px 0;">Email or pay via UPI. API key within 1 hour.</p>
<a href="mailto:divineearthly@gmail.com?subject=Nyaya%20Lens%20API">📧 Email Us</a>
<a href="upi://pay?pa=divinesouljoy@pnb&pn=NyayaLens&am=499&tn=API" class="upi-btn">💳 Pay via UPI</a>
<p style="font-size:12px;color:#7878a0;margin-top:12px;">₹499/month · 10,000 checks · Instant setup</p>
</div>
<div class="footer"><strong>Nyaya Lens</strong> · Sutra 65: Pramana-Nyaya Epistemic Kernel<br>From the Vedic AI Framework · 72 Sutras + 13 Upa-Sutras</div>
</div>
</body>
</html>'''
    
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)
