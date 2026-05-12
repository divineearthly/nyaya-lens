from flask import Flask, request, jsonify
from nyaya_lens import analyze_claim
import os

app = Flask(__name__)

API_KEYS = {
    "free_trial_123": {"plan": "trial", "remaining": 50},
    "pro_key_456": {"plan": "pro", "remaining": 999999}
}

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    api_key = request.headers.get('X-API-Key')
    if not api_key or api_key not in API_KEYS:
        return jsonify({"error": "Invalid API key"}), 401
    
    if API_KEYS[api_key]['remaining'] <= 0:
        return jsonify({"error": "Quota exceeded. Upgrade at nyaya-lens.com"}), 429
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    
    result = analyze_claim(data['text'])
    API_KEYS[api_key]['remaining'] -= 1
    
    return jsonify({
        "pramana_score": result['pramana_score'],
        "primary_source": result['primary_source'],
        "hallucination_risk": "HIGH" if result['pramana_score'] < 35 else "MODERATE" if result['pramana_score'] < 65 else "LOW",
        "flag_count": len(result['hallucination_flags']),
        "flags": [f['explanation'] for f in result['hallucination_flags']],
        "remaining_quota": API_KEYS[api_key]['remaining']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
