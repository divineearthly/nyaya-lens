from nyaya_lens import analyze_claim
from datetime import datetime

def generate_html_report(claim, result):
    s = result['pramana_score']
    if s >= 70:
        risk_color, risk_text = "#4ecca3", "LOW RISK"
    elif s >= 40:
        risk_color, risk_text = "#f0b040", "MODERATE RISK"
    else:
        risk_color, risk_text = "#e94560", "HIGH RISK"
    
    flags_html = ""
    for f in result['hallucination_flags']:
        flags_html += f'<tr><td style="color:#e94560">⚠️</td><td>{f["explanation"]}</td></tr>'
    
    steps_html = ""
    for step, content in result['five_step_scaffold'].items():
        steps_html += f'<tr><td style="font-weight:bold;color:#f0b040;width:200px">{step}</td><td>{content}</td></tr>'
    
    report = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Nyaya Lens Report</title>
<style>
body{{font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:20px;color:#333}}
.header{{text-align:center;border-bottom:3px solid #f0b040;padding-bottom:20px;margin-bottom:20px}}
.score{{font-size:72px;font-weight:bold;text-align:center;color:{risk_color};margin:20px 0}}
.badge{{text-align:center;font-size:24px;color:{risk_color};margin-bottom:20px}}
table{{width:100%;border-collapse:collapse;margin:15px 0}}
td,th{{padding:10px;border:1px solid #ddd;text-align:left;vertical-align:top}}
.footer{{text-align:center;color:#999;font-size:11px;margin-top:30px;border-top:1px solid #ddd;padding-top:15px}}
.watermark{{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-30deg);font-size:100px;color:rgba(240,176,64,0.05);z-index:-1}}
</style></head><body>
<div class="watermark">NYAYA LENS</div>
<div class="header">
<h1>Nyaya Lens — Truth Verification Report</h1>
<p>Generated: {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
<p>Sutra 65: Pramana-Nyaya Epistemic Kernel</p>
</div>
<div class="score">{s}</div>
<div class="badge">PRAMANA SCORE — {risk_text}</div>
<h2>Claim Analyzed</h2>
<p style="background:#f5f5f5;padding:15px;border-radius:5px">{claim}</p>
<h2>Primary Epistemic Source</h2>
<p style="font-size:18px">{result['primary_source']}</p>
<h2>5-Step Verification (Pancha Avayava)</h2>
<table>{steps_html}</table>
<h2>Hallucination Indicators ({len(result['hallucination_flags'])})</h2>
<table>{flags_html if flags_html else '<tr><td colspan="2" style="color:#4ecca3">✅ No hallucination flags detected</td></tr>'}</table>
<div class="footer">
<strong>Nyaya Lens</strong> — AI Hallucination Detection Engine<br>
Built from the Nyaya Sutras (~2nd century BCE)<br>
72 Sutras + 13 Upa-Sutras Vedic AI Framework<br>
<em>Satyam Eva Jayate — Truth Alone Triumphs</em>
</div></body></html>'''
    return report

if __name__ == '__main__':
    text = input("Enter claim to analyze: ")
    result = analyze_claim(text)
    report = generate_html_report(text, result)
    filename = f"nyaya_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"Report saved: {filename}")
