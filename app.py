from flask import Flask, render_template_string, request
from nyaya_lens import analyze_claim
import os
import re
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPER = True
except:
    HAS_SCRAPER = False

app = Flask(__name__)

def extract_text_from_url(url):
    if not HAS_SCRAPER:
        return None, "Scraper not available"
    try:
        headers = {'User-Agent': 'Nyaya-Lens/1.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        text = soup.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)[:5000]
        return text, None
    except Exception as e:
        return None, str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    claim = ''
    url = ''
    url_error = None
    
    if request.method == 'POST':
        claim = request.form.get('claim', '')
        url = request.form.get('url', '')
        
        if url and not claim:
            extracted, url_error = extract_text_from_url(url)
            if extracted:
                claim = extracted
        
        if claim.strip():
            analysis = analyze_claim(claim)
            result = {
                'pramana_score': analysis['pramana_score'],
                'primary_source': analysis['primary_source'],
                'source_scores': analysis['source_scores'],
                'five_step_scaffold': analysis['five_step_scaffold'],
                'hallucination_flags': analysis['hallucination_flags']
            }
    
    # Simple inline HTML
    html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nyaya Lens</title>'
    html += '<style>:root{--bg:#0d0d1a;--card:#13132b;--inp:#1a1a3a;--b:#2a2a5a;--t:#d0d0e0;--d:#7878a0;--g:#f0b040;--r:#e94560;--gr:#4ecca3}*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--t);padding:16px}.c{max-width:680px;margin:0 auto}h1{text-align:center;background:linear-gradient(135deg,#f0b040,#ff6b35);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:28px}.tag{text-align:center;color:var(--d);font-size:12px;margin:4px 0 16px}.row{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}.chip{flex:1;min-width:90px;background:var(--card);border:1px solid var(--b);border-radius:10px;padding:10px;text-align:center;font-size:11px;color:var(--d)}.chip strong{color:var(--t);font-size:14px}.card{background:var(--card);border:1px solid var(--b);border-radius:14px;padding:16px;margin-bottom:12px}.lbl{font-size:12px;font-weight:600;color:var(--d);text-transform:uppercase;margin-bottom:8px}input[type=url],textarea{width:100%;padding:12px;background:var(--inp);color:var(--t);border:1px solid var(--b);border-radius:10px;font-size:14px;margin-bottom:8px;font-family:inherit}textarea{min-height:100px;resize:vertical}input:focus,textarea:focus{outline:none;border-color:var(--g)}.btn{width:100%;padding:14px;background:linear-gradient(135deg,#f0b040,#e08030);color:#0d0d1a;border:none;border-radius:12px;font-size:16px;font-weight:700;cursor:pointer}.qbtn{flex:1;min-width:70px;padding:8px;background:var(--inp);color:var(--d);border:1px solid var(--b);border-radius:8px;font-size:10px;cursor:pointer}.res{background:var(--card);border:1px solid var(--b);border-radius:14px;padding:20px;margin-top:12px}.ring{width:100px;height:100px;border-radius:50%;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;border:5px solid;font-size:36px;font-weight:900}.ring.g{border-color:var(--gr);color:var(--gr);box-shadow:0 0 20px rgba(78,204,163,0.2)}.ring.y{border-color:var(--g);color:var(--g);box-shadow:0 0 20px rgba(240,176,64,0.2)}.ring.r{border-color:var(--r);color:var(--r);box-shadow:0 0 20px rgba(233,69,96,0.2)}.sl{text-align:center;font-size:11px;color:var(--d);margin-bottom:12px}.badge{display:block;text-align:center;padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;margin:0 auto 12px;width:fit-content}.badge.p{background:rgba(78,204,163,0.15);color:var(--gr)}.badge.a{background:rgba(240,176,64,0.15);color:var(--g)}.badge.u{background:rgba(123,79,216,0.15);color:#a78bfa}.badge.s{background:rgba(233,69,96,0.15);color:var(--r)}.step{background:var(--inp);padding:10px;border-radius:8px;margin-bottom:6px;font-size:12px;border-left:3px solid var(--b)}.step strong{color:var(--g);font-size:10px;text-transform:uppercase;display:block}.flags{margin-top:12px;background:rgba(233,69,96,0.08);border:1px solid rgba(233,69,96,0.25);border-radius:10px;padding:12px}.flags h3{color:var(--r);font-size:13px;margin-bottom:8px}.flag{background:rgba(233,69,96,0.1);padding:6px 10px;border-radius:6px;margin-bottom:4px;font-size:11px;color:#ff8a9e}.pricing{text-align:center;padding:20px;background:linear-gradient(135deg,#1a1a3a,#0f0f2a);border:2px solid #f0b040;border-radius:14px;margin-top:16px}.pricing h3{color:#f0b040;font-size:18px}.pricing p{color:#d0d0e0;margin:6px 0;font-size:13px}.pricing a{display:inline-block;padding:10px 20px;background:#f0b040;color:#0d0d1a;border-radius:8px;text-decoration:none;font-weight:700;margin:6px;font-size:13px}.pricing .upi{background:#4ecca3}.footer{text-align:center;padding:20px;color:var(--d);font-size:10px}</style></head><body><div class="c"><h1>Nyaya Lens</h1><p class="tag">Truth detection engine — 2,500-year-old Indian formal logic</p><div class="row"><div class="chip">🔍<br>Analyzes <strong>any text</strong><br>AI, news, webpages</div><div class="chip">🧠<br>Based on <strong>Sutra 65</strong><br>Pramana-Nyaya</div><div class="chip">⚡<br>Runs <strong>100% offline</strong><br>No API, no tracking</div></div><div class="card"><div class="lbl">Paste a URL to analyze</div><form method="POST"><input type="url" name="url" placeholder="https://example.com/news-article" value="' + (url or '') + '"><div class="lbl" style="margin-top:8px">Or paste text directly</div><textarea name="claim" placeholder="Paste any claim, news, or AI-generated text here...">' + (claim or '') + '</textarea><button class="btn">Analyze Truth</button><div style="display:flex;gap:6px;margin-top:8px"><button type="button" class="qbtn" onclick="document.querySelector(\'textarea\').value=\'BREAKING: Scientists have just proved that drinking turmeric tea cures all types of cancer within 3 days with zero side effects.\';this.form.submit()">Fake Claim</button><button type="button" class="qbtn" onclick="document.querySelector(\'textarea\').value=\'The leaves are turning yellow and the soil feels dry, so the plant probably needs water.\';this.form.submit()">Inference</button><button type="button" class="qbtn" onclick="document.querySelector(\'textarea\').value=\'I measured the soil pH with a digital meter at 9:00 AM today. The reading was 6.8.\';this.form.submit()">Observation</button><button type="button" class="qbtn" onclick="document.querySelector(\'textarea\').value=\'According to a new study, researchers claim AI will replace 40% of jobs by 2030.\';this.form.submit()">News Style</button></div></form></div>'
    
    if url_error:
        html += f'<p style="color:#e94560;font-size:12px">URL error: {url_error}</p>'
    
    if result:
        s = result['pramana_score']
        em, rc, lb = ('✅','g','High') if s>=70 else ('🤔','y','Moderate') if s>=40 else ('🚨','r','Low')
        src = result['primary_source']
        bc, bi = ('p','👁️') if 'Pratyaksha' in src else ('a','🧠') if 'Anumana' in src else ('u','🔄') if 'Upamana' in src else ('s','📢')
        html += f'<div class="res"><div style="text-align:center;font-size:28px">{em}</div><div class="ring {rc}">{s}</div><div class="sl">Truth Confidence — {lb}</div><span class="badge {bc}">{bi} {src}</span>'
        html += '<div style="margin-top:12px"><div class="lbl">5-Step Reasoning</div>'
        for step, content in result['five_step_scaffold'].items():
            html += f'<div class="step"><strong>{step}</strong>{content}</div>'
        html += '</div>'
        if result['hallucination_flags']:
            html += f'<div class="flags"><h3>Hallucination Indicators ({len(result["hallucination_flags"])})</h3>'
            for f in result['hallucination_flags']:
                html += f'<div class="flag">{f["explanation"]}</div>'
            html += '</div>'
        html += '</div>'
    
    html += '<div class="pricing"><h3>Get API Access — $9/month</h3><p>REST API · 10,000 checks · 100% offline</p><p>📧 divineearthly@gmail.com | 💳 divinesouljoy@pnb</p><a href="mailto:divineearthly@gmail.com">📧 Email</a><a href="upi://pay?pa=divinesouljoy@pnb&pn=NyayaLens&am=499" class="upi">💳 UPI ₹499</a><p style="font-size:11px;color:#7878a0;margin-top:8px">API key within 1 hour</p></div><div class="footer"><strong>Nyaya Lens</strong> · Sutra 65 · Vedic AI Framework · 72 Sutras + 13 Upa-Sutras<br><em>Satyam Eva Jayate — Truth Alone Triumphs</em></div></div></body></html>'
    
    return render_template_string(html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)
