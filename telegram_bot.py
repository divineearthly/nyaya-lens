import requests
import json
from nyaya_lens import analyze_claim

# Get token from @BotFather on Telegram
TOKEN = "8623123631:AAFbO9pwFcrqV2gZgxXRjzQCrzLjzCiq0rU"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

def handle_update(update):
    msg = update.get("message", {})
    text = msg.get("text", "")
    chat_id = msg.get("chat", {}).get("id")
    
    if not text or not chat_id:
        return
    
    if text == "/start":
        send_message(chat_id, "⚖️ <b>Nyaya Lens Bot</b>\n\nSend me any claim, news, or text. I'll analyze it for truth.\n\nBuilt from the Nyaya Sutras (~2nd century BCE).")
        return
    
    result = analyze_claim(text)
    s = result['pramana_score']
    emoji = "✅" if s >= 70 else "⚠️" if s >= 40 else "🚨"
    
    reply = f"{emoji} <b>Pramana Score: {s}/100</b>\n\n"
    reply += f"📌 <b>Source:</b> {result['primary_source']}\n\n"
    reply += f"📜 <b>Verdict:</b> {result['five_step_scaffold']['5. Nigamana (Conclusion)']}\n\n"
    
    if result['hallucination_flags']:
        reply += f"⚠️ <b>{len(result['hallucination_flags'])} Red Flags:</b>\n"
        for f in result['hallucination_flags'][:5]:
            reply += f"• {f['explanation']}\n"
    
    send_message(chat_id, reply)

if __name__ == '__main__':
    print("Nyaya Lens Telegram Bot starting...")
    print("1. Get token from @BotFather")
    print("2. Replace TOKEN in this file")
    print("3. Run this script")
    print("4. Use webhook or polling")
