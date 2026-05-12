chrome.contextMenus.create({
  id: "verifyClaim",
  title: "Verify with Nyaya Lens",
  contexts: ["selection"]
});

chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "verifyClaim" && info.selectionText) {
    try {
      const response = await fetch("https://divinesouljoy-nyaya-lens-api.hf.space/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": "nyaya_free_demo"
        },
        body: JSON.stringify({ text: info.selectionText })
      });
      const result = await response.json();
      
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: showResult,
        args: [result]
      });
    } catch (e) {
      console.error("Nyaya Lens error:", e);
    }
  }
});

function showResult(result) {
  const score = result.pramana_score;
  const color = score >= 70 ? "#4ecca3" : score >= 40 ? "#f0b040" : "#e94560";
  const risk = score >= 70 ? "LOW RISK" : score >= 40 ? "MODERATE" : "HIGH RISK";
  
  const div = document.createElement("div");
  div.style.cssText = `position:fixed;top:20px;right:20px;z-index:99999;background:#0d0d1a;color:#fff;padding:20px;border-radius:12px;border:2px solid ${color};max-width:400px;box-shadow:0 10px 40px rgba(0,0,0,0.5);font-family:Arial,sans-serif;font-size:14px`;
  div.innerHTML = `
    <div style="font-size:36px;font-weight:bold;color:${color};text-align:center">${score}</div>
    <div style="text-align:center;color:${color};margin-bottom:10px">${risk}</div>
    <div style="font-size:12px;color:#a0a0b0">${result.primary_source}</div>
    ${result.flags?.length ? `<div style="color:#e94560;font-size:11px;margin-top:8px">⚠️ ${result.flag_count} red flags</div>` : ''}
    <button onclick="this.parentElement.remove()" style="margin-top:10px;padding:4px 12px;background:#333;color:#fff;border:none;border-radius:4px;cursor:pointer;font-size:11px">Close</button>
  `;
  document.body.appendChild(div);
}
