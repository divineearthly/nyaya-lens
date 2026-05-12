from flask import Flask, request
from nyaya_lens import analyze_claim
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '')
    response = MessagingResponse()
    msg = response.message()
    
    result = analyze_claim(incoming_msg)
    s = result['pramana_score']
    emoji = "✅" if s >= 70 else "⚠️" if s >= 40 else "🚨"
    
    reply = f"{emoji} Score: {s}/100\n"
    reply += f"Source: {result['primary_source']}\n"
    reply += f"Verdict: {result['five_step_scaffold']['5. Nigamana (Conclusion)']}\n"
    
    if result['hallucination_flags']:
        reply += f"\n{len(result['hallucination_flags'])} red flags detected"
    
    msg.body(reply)
    return str(response)

if __name__ == '__main__':
    app.run(port=5002)
