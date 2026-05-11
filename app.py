from flask import Flask, render_template_string, request
from nyaya_lens import analyze_claim
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nyaya Lens — Truth Verification</title>
    <style>
        :root {
            --bg: #0d0d1a;
            --card: #13132b;
            --input: #1a1a3a;
            --border: #2a2a5a;
            --text: #d0d0e0;
            --dim: #7878a0;
            --gold: #f0b040;
            --red: #e94560;
            --green: #4ecca3;
            --purple: #7b4fd8;
            --accent: #ff6b35;
            --radius: 16px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            padding: 16px;
        }
        .container { max-width: 680px; margin: 0 auto; }
        .hero { text-align: center; padding: 32px 0 24px; }
        .hero-icon { font-size: 48px; margin-bottom: 8px; }
        .hero h1 {
            font-size: 32px;
            background: linear-gradient(135deg, #f0b040, #ff6b35);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }
        .hero .tagline { color: var(--dim); font-size: 13px; margin-top: 4px; font-style: italic; }
        .info-row { display: flex; gap: 10px; margin-bottom: 16px; flex-wrap: wrap; }
        .info-chip {
            flex: 1; min-width: 100px; background: var(--card);
            border: 1px solid var(--border); border-radius: 12px;
            padding: 12px; text-align: center; font-size: 12px; color: var(--dim);
        }
        .info-chip strong { display: block; color: var(--text); font-size: 16px; margin-bottom: 2px; }
        .card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 20px; margin-bottom: 16px;
        }
        .card-label {
            font-size: 13px; font-weight: 600; color: var(--dim);
            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
        }
        textarea {
            width: 100%; min-height: 120px; padding: 14px;
            background: var(--input); color: var(--text);
            border: 1px solid var(--border); border-radius: 12px;
            font-size: 15px; line-height: 1.5; resize: vertical;
            font-family: inherit; transition: border 0.2s;
        }
        textarea:focus { outline: none; border-color: var(--gold); }
        textarea::placeholder { color: #555; font-style: italic; }
        .btn {
            display: block; width: 100%; padding: 16px;
            background: linear-gradient(135deg, #f0b040, #e08030);
            color: #0d0d1a; border: none; border-radius: 14px;
            font-size: 17px; font-weight: 700; cursor: pointer; margin-top: 12px;
        }
        .btn:active { transform: scale(0.98); }
        .quick-tests { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
        .quick-btn {
            flex: 1; min-width: 80px; padding: 10px;
            background: var(--input); color: var(--dim);
            border: 1px solid var(--border); border-radius: 10px;
            font-size: 11px; cursor: pointer; text-align: center;
        }
        .quick-btn:active { background: var(--purple); color: white; }
        .result-card {
            background: var(--card); border: 1px solid var(--border);
            border-radius: var(--radius); padding: 24px;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .score-ring {
            width: 130px; height: 130px; border-radius: 50%;
            margin: 0 auto 16px; display: flex; align-items: center; justify-content: center;
            border: 6px solid; font-size: 42px; font-weight: 900;
        }
        .score-ring.green { border-color: var(--green); color: var(--green); box-shadow: 0 0 30px rgba(78, 204, 163, 0.2); }
        .score-ring.yellow { border-color: var(--gold); color: var(--gold); box-shadow: 0 0 30px rgba(240, 176, 64, 0.2); }
        .score-ring.red { border-color: var(--red); color: var(--red); box-shadow: 0 0 30px rgba(233, 69, 96, 0.2); }
        .score-label {
            text-align: center; font-size: 13px; color: var(--dim);
            margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;
        }
        .score-emoji { text-align: center; font-size: 36px; margin-bottom: 8px; }
        .source-badge {
            display: inline-block; padding: 6px 14px; border-radius: 20px;
            font-size: 13px; font-weight: 600; margin: 0 auto 16px;
            display: block; width: fit-content;
        }
        .source-badge.pratyaksha { background: rgba(78, 204, 163, 0.15); color: var(--green); border: 1px solid rgba(78, 204, 163, 0.3); }
        .source-badge.anumana { background: rgba(240, 176, 64, 0.15); color: var(--gold); border: 1px solid rgba(240, 176, 64, 0.3); }
        .source-badge.upamana { background: rgba(123, 79, 216, 0.15); color: #a78bfa; border: 1px solid rgba(123, 79, 216, 0.3); }
        .source-badge.shabda { background: rgba(233, 69, 96, 0.15); color: var(--red); border: 1px solid rgba(233, 69, 96, 0.3); }
        .steps { margin-top: 16px; }
        .step {
            background: var(--input); padding: 12px 14px; border-radius: 10px;
            margin-bottom: 8px; font-size: 13px; line-height: 1.5;
            border-left: 3px solid var(--border);
        }
        .step strong {
            color: var(--gold); font-size: 11px; text-transform: uppercase;
            letter-spacing: 0.5px; display: block; margin-bottom: 2px;
        }
        .flags-section {
            margin-top: 16px; background: rgba(233, 69, 96, 0.08);
            border: 1px solid rgba(233, 69, 96, 0.25); border-radius: 12px; padding: 16px;
        }
        .flags-section h3 { color: var(--red); font-size: 14px; margin-bottom: 10px; }
        .flag {
            padding: 8px 12px; background: rgba(233, 69, 96, 0.1);
            border-radius: 8px; margin-bottom: 6px; font-size: 12px; color: #ff8a9e;
        }
        .flag::before { content: "⚠️ "; }
        .dist-bars { margin-top: 16px; }
        .dist-bar-wrap { margin-bottom: 6px; }
        .dist-label { font-size: 11px; color: var(--dim); margin-bottom: 2px; }
        .dist-bar {
            height: 20px; border-radius: 6px; min-width: 4px;
            transition: width 0.5s ease; display: flex; align-items: center;
            padding-left: 8px; font-size: 10px; font-weight: 600;
        }
        .dist-bar.p { background: var(--green); color: #0d0d1a; }
        .dist-bar.a { background: var(--gold); color: #0d0d1a; }
        .dist-bar.u { background: #a78bfa; color: white; }
        .dist-bar.s { background: var(--red); color: white; }
        .footer { text-align: center; padding: 24px; color: var(--dim); font-size: 11px; }
        .footer a { color: var(--gold); text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <div class="hero-icon">⚖️</div>
            <h1>Nyaya Lens</h1>
            <p class="tagline">Truth detection engine — 2,500-year-old Indian formal logic</p>
        </div>
        <div class="info-row">
            <div class="info-chip"><span>🔍</span><br>Analyzes <strong>any text</strong><br>AI, news, claims, posts</div>
            <div class="info-chip"><span>🧠</span><br>Based on <strong>Sutra 65</strong><br>Pramana-Nyaya logic</div>
            <div class="info-chip"><span>⚡</span><br>Runs <strong>100% offline</strong><br>No API, no tracking</div>
        </div>
        <div class="card">
            <div class="card-label">🔎 Paste any claim or AI-generated text</div>
            <form method="POST" id="analyzeForm">
                <textarea name="claim" id="claimInput" placeholder="Example: &quot;Scientists have just proved that drinking green tea cures all types of cancer overnight with zero side effects.&quot;&#10;&#10;Or paste a ChatGPT / news / WhatsApp forward here...">{{ claim or '' }}</textarea>
                <button type="submit" class="btn">⚡ Analyze Truth</button>
            </form>
            <div class="quick-tests">
                <button class="quick-btn" onclick="setTest('hallucination')">🔴 Fake Claim</button>
                <button class="quick-btn" onclick="setTest('inference')">🟡 Inference</button>
                <button class="quick-btn" onclick="setTest('observation')">🟢 Observation</button>
                <button class="quick-btn" onclick="setTest('news')">📰 News Style</button>
            </div>
        </div>
        {% if result %}
        <div class="result-card">
            {% if result.pramana_score >= 70 %}
                <div class="score-emoji">✅</div>
                <div class="score-ring green">{{ result.pramana_score }}</div>
                <div class="score-label">Truth Confidence — High</div>
            {% elif result.pramana_score >= 40 %}
                <div class="score-emoji">🤔</div>
                <div class="score-ring yellow">{{ result.pramana_score }}</div>
                <div class="score-label">Truth Confidence — Moderate</div>
            {% else %}
                <div class="score-emoji">🚨</div>
                <div class="score-ring red">{{ result.pramana_score }}</div>
                <div class="score-label">Truth Confidence — Low</div>
            {% endif %}
            {% set source = result.primary_source %}
            {% if 'Pratyaksha' in source %}
                <span class="source-badge pratyaksha">👁️ {{ source }}</span>
            {% elif 'Anumana' in source %}
                <span class="source-badge anumana">🧠 {{ source }}</span>
            {% elif 'Upamana' in source %}
                <span class="source-badge upamana">🔄 {{ source }}</span>
            {% else %}
                <span class="source-badge shabda">📢 {{ source }}</span>
            {% endif %}
            <div class="dist-bars">
                {% for label, score in result.source_scores.items() %}
                    {% if score > 0 %}
                        {% set pct = (score * 50) %}
                        {% if pct > 100 %}{% set pct = 100 %}{% endif %}
                        {% if 'Pratyaksha' in label %}{% set cls = 'p' %}
                        {% elif 'Anumana' in label %}{% set cls = 'a' %}
                        {% elif 'Upamana' in label %}{% set cls = 'u' %}
                        {% else %}{% set cls = 's' %}{% endif %}
                        <div class="dist-bar-wrap">
                            <div class="dist-label">{{ label }}</div>
                            <div class="dist-bar {{ cls }}" style="width: {{ pct }}%">{{ score }}</div>
                        </div>
                    {% endif %}
                {% endfor %}
            </div>
            <div class="steps">
                <div class="card-label" style="margin-top: 8px;">📜 5-Step Reasoning (Pancha Avayava)</div>
                {% for step, content in result.five_step_scaffold.items() %}
                    <div class="step"><strong>{{ step }}</strong>{{ content }}</div>
                {% endfor %}
            </div>
            {% if result.hallucination_flags %}
                <div class="flags-section">
                    <h3>⚠️ Hallucination Indicators ({{ result.hallucination_flags|length }})</h3>
                    {% for flag in result.hallucination_flags %}
                        <div class="flag">{{ flag.explanation }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        </div>
        {% endif %}
        <div class="footer">
            <strong>Nyaya Lens</strong> · Sutra 65: Pramana-Nyaya Epistemic Kernel<br>
            From the Vedic AI Framework · <a href="#">72 Sutras + 13 Upa-Sutras</a>
        </div>
    </div>
    <script>
        function setTest(type) {
            const tests = {
                hallucination: "BREAKING: Scientists have just proved that drinking turmeric tea cures all types of cancer within 3 days with zero side effects.",
                inference: "The leaves are turning yellow and the soil feels dry to touch, so the plant probably needs water.",
                observation: "I measured the soil pH with a digital meter at 9:00 AM today. The reading was 6.8.",
                news: "According to a new study published in Nature, researchers claim that artificial intelligence will replace 40% of jobs by 2030."
            };
            document.getElementById('claimInput').value = tests[type] || '';
            document.getElementById('analyzeForm').submit();
        }
    </script>
<div style="text-align:center;padding:16px;background:#1a1a3a;border-radius:12px;margin:16px auto;max-width:680px;"><p style="color:#f0b040;font-weight:700;font-size:18px;">🚀 Developers: Add truth verification to your AI app</p><p style="font-size:13px;color:#a0a0b0;">REST API · 10,000 checks/month · 100% offline</p><a href="https://gumroad.com/l/nyaya-lens-api" style="display:inline-block;padding:14px 28px;background:linear-gradient(135deg,#f0b040,#e08030);color:#0d0d1a;border-radius:10px;text-decoration:none;font-weight:700;font-size:16px;margin-top:8px;">Get API Key — $9/month</a></div>
<div style="text-align:center;padding:20px;background:linear-gradient(135deg,#1a1a3a,#0f0f2a);border:1px solid #2a2a5a;border-radius:16px;margin:20px auto;max-width:680px;"><p style="color:#f0b040;font-weight:800;font-size:20px;">🚀 Get API Access — $9/month</p><p style="font-size:14px;color:#d0d0e0;margin:10px 0;">Add truth verification to your AI app</p><div style="background:#0d0d1a;padding:12px;border-radius:8px;margin:10px 0;font-size:13px;color:#a0a0b0;">10,000 checks/month • Hallucination detection • 5-step verification • Instant key</div><p style="font-size:15px;color:#fff;font-weight:600;">📧 divinesouljoy@pnb</p><p style="font-size:12px;color:#7878a0;">Email for payment details • Get API key within 1 hour</p></div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    claim = ''
    if request.method == 'POST':
        claim = request.form.get('claim', '')
        if claim.strip():
            analysis = analyze_claim(claim)
            score = analysis['pramana_score']
            if score >= 70:
                score_color = 'green'
            elif score >= 40:
                score_color = 'yellow'
            else:
                score_color = 'red'
            scaffold_text = {}
            for step, content in analysis['five_step_scaffold'].items():
                scaffold_text[step] = content
            result = {
                'pramana_score': score,
                'score_color': score_color,
                'primary_source': analysis['primary_source'],
                'source_scores': analysis['source_scores'],
                'five_step_scaffold': scaffold_text,
                'hallucination_flags': analysis['hallucination_flags']
            }
    return render_template_string(HTML_TEMPLATE, claim=claim, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7860))
    app.run(host='0.0.0.0', port=port)

# No need to modify — button already added
