from flask import Flask, render_template_string
import sutra68_vedic_math as sm

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sutra 68: Vedic Math CNN</title>
<style>
body{font-family:system-ui;background:#06060f;color:#d0d0e0;padding:20px;text-align:center}
h1{background:linear-gradient(135deg,#f0b040,#ff6b35);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.card{background:#0d0d20;border:1px solid #1a1a3a;border-radius:14px;padding:20px;margin:16px auto;max-width:650px;text-align:left}
h3{color:#f0b040}pre{background:#000;padding:14px;border-radius:8px;font-size:13px;color:#4ecca3}
b{color:#4ecca3}
</style></head><body>
<h1>Sutra 68: Vedic Math CNN</h1>
<p>Ultra-fast neural network operations using ancient Indian algorithms</p>
<div class="card"><h3>Urdhva-Tiryagbhyam</h3><p>1234 x 5678 = <b>""" + str(sm.VedicConvolution.urdhva_multiply(1234, 5678)) + """</b></p></div>
<div class="card"><h3>Nikhilam (Near Base 100)</h3><p>97 x 93 = <b>""" + str(sm.VedicConvolution.nikhilam_multiply(97, 93)) + """</b></p></div>
<div class="card"><h3>1D Convolution</h3><pre>Signal: [1,2,3,4,5]
Kernel: [1,0,-1]
Output: """ + str(sm.VedicConvolution.convolution_1d([1,2,3,4,5],[1,0,-1])) + """</pre></div>
<div class="card"><h3>Benchmark</h3><pre>""" + str(sm.VedicConvolution.benchmark()) + """</pre></div>
<p><a href="https://divineearthly.github.io" style="color:#f0b040">Divine Earthly Hub</a></p>
<p style="font-size:11px;color:#8888aa">Sutra 68 of 85</p>
</body></html>"""

@app.route('/')
def index():
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
