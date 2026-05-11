from flask import Flask, render_template_string, request
from nyaya_lens import analyze_claim

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nyaya Lens - Truth Verification</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, sans-serif;
            background: #1a1a2e;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: #16213e;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }
        h1 {
            color: #e94560;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #a0a0b0;
            margin-bottom: 20px;
            font-style: italic;
        }
        textarea {
            width: 100%;
            padding: 12px;
            background: #0f3460;
            color: #fff;
            border: 1px solid #533483;
            border-radius: 8px;
            font-size: 16px;
            resize: vertical;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            margin-top: 10px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #0f3460;
            border-radius: 8px;
            white-space: pre-wrap;
        }
        .score {
            font-size: 48px;
            text-align: center;
            font-weight: bold;
        }
        .green { color: #4ecca3; }
        .yellow { color: #f0c040; }
        .red { color: #e94560; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚖️ Nyaya Lens</h1>
        <p class="subtitle">Hallucination detection via 2,500-year-old Indian logic (Sutra 65)</p>
        
        <form method="POST">
            <textarea name="claim" rows="4" placeholder="Paste any claim or AI-generated text here...">{{ claim or '' }}</textarea>
            <button type="submit">Analyze Truth</button>
        </form>
        
        {% if result %}
        <div class="result">
            <div class="score {{ result.score_color }}">
                {{ result.pramana_score }} / 100
            </div>
            <p><strong>Source:</strong> {{ result.primary_source }}</p>
            <hr>
            <pre>{{ result.scaffold }}</pre>
            {% if result.flags %}
            <hr>
            <p style="color: #e94560;"><strong>⚠️ Hallucination Flags:</strong></p>
            <ul>
            {% for flag in result.flags %}
                <li>{{ flag.explanation }}</li>
            {% endfor %}
            </ul>
            {% endif %}
        </div>
        {% endif %}
    </div>
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
            
            scaffold_text = ''
            for step, content in analysis['five_step_scaffold'].items():
                scaffold_text += f"{step}: {content}\n"
            
            result = {
                'pramana_score': score,
                'score_color': score_color,
                'primary_source': analysis['primary_source'],
                'scaffold': scaffold_text,
                'flags': analysis['hallucination_flags']
            }
    
    return render_template_string(HTML_TEMPLATE, claim=claim, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
