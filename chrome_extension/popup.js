document.getElementById('analyze').addEventListener('click', async () => {
  const claim = document.getElementById('claim').value;
  if (!claim) return;
  
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = 'Analyzing...';
  
  try {
    const res = await fetch('https://divinesouljoy-nyaya-lens-api.hf.space/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-API-Key': 'nyaya_free_demo' },
      body: JSON.stringify({ text: claim })
    });
    const data = await res.json();
    const c = data.pramana_score >= 70 ? '#4ecca3' : data.pramana_score >= 40 ? '#f0b040' : '#e94560';
    resultDiv.innerHTML = `<div style="text-align:center;font-size:36px;color:${c}">${data.pramana_score}</div>
      <p style="color:#a0a0b0">${data.primary_source}</p>
      <p style="color:${c}">${data.hallucination_risk} RISK</p>
      ${data.flag_count ? `<p style="color:#e94560">⚠️ ${data.flag_count} flags</p>` : ''}`;
  } catch (e) {
    resultDiv.innerHTML = '<p style="color:#e94560">Error connecting</p>';
  }
});
