import os
import requests
from nyaya_lens import analyze_claim

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

def handle_update(update):
    msg = update.get("message", {})
    text = msg.get("text", "")
    chat_id = msg.get("chat", {}).get("id")
    if not text or not chat_id: return
    if text == "/start":
        send_message(chat_id, "⚖️ Nyaya Lens Bot\n\nSend any claim. I'll analyze it for truth.\nBuilt from Nyaya Sutras (~2nd century BCE).")
        return
    result = analyze_claim(text)
    s = result['pramana_score']
    emoji = "✅" if s >= 70 else "⚠️" if s >= 40 else "🚨"
    reply = f"{emoji} Score: {s}/100\nSource: {result['primary_source']}\nVerdict: {result['five_step_scaffold']['5. Nigamana (Conclusion)']}"
    if result['hallucination_flags']:
        reply += f"\n\n{len(result['hallucination_flags'])} red flags:\n"
        for f in result['hallucination_flags'][:5]:
            reply += f"• {f['explanation']}\n"
    send_message(chat_id, reply)

if __name__ == '__main__':
    print("Set TELEGRAM_BOT_TOKEN environment variable and deploy.")
