import psutil
from flask import Flask
from datetime import datetime

app = Flask(__name__)

def get_html_status():
    # CSS 样式保持不变
    style = """
    <style>
        body { background-color: #0d1117; color: #00ff41; font-family: 'Courier New', Courier, monospace; padding: 20px; max-width: 800px; margin: 0 auto; }
        h2 { color: #fff; border-bottom: 2px solid #333; padding-bottom: 10px; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .label { color: #8b949e; font-size: 0.9em; }
        .value { font-size: 1.2em; font-weight: bold; margin-top: 5px; }
        .progress-bg { background: #333; height: 10px; border-radius: 5px; overflow: hidden; margin-top: 10px; }
        .progress-bar { background: #238636; height: 100%; }
    </style>
    """
    
    html = [style]
    html.append(f"<h2>🖥️ SERVER MONITOR (Docker版)</h2>")
    html.append(f"<p class='label'>Last Updated: {datetime.now().strftime('%H:%M:%S')}</p>")
    
    # --- 1. CPU ---
    # loadavg 依然可以从 os 读取，或者用 psutil.cpu_percent()
    try:
        load1, load5, load15 = psutil.getloadavg()
        val_color = "#ff7b72" if load1 > 2.0 else "#00ff41"
        html.append("<div class='card'>")
        html.append("<div>🔥 CPU LOAD (1min)</div>")
        html.append(f"<div class='value' style='color:{val_color}'>{load1}</div>")
        html.append("</div>")
    except: html.append("<div class='card'>CPU Err</div>")

    # --- 2. 磁盘 ---
    try:
        du = psutil.disk_usage('/')
        # 转换单位为 GB
        total = round(du.total / (1024**3), 1)
        used = round(du.used / (1024**3), 1)
        percent = du.percent
        
        bar_color = "#238636"
        if percent > 80: bar_color = "#d29922"
        if percent > 90: bar_color = "#ff7b72"

        html.append("<div class='card'>")
        html.append(f"<div>💾 DISK USAGE</div>")
        html.append(f"<div class='value'>{used}G / {total}G ({percent}%)</div>")
        html.append(f"<div class='progress-bg'><div class='progress-bar' style='width:{percent}%; background:{bar_color}'></div></div>")
        html.append("</div>")
    except: pass

    # --- 3. 内存 ---
    try:
        mem = psutil.virtual_memory()
        # available 是真实可用内存
        avail_gb = round(mem.available / (1024**3), 2)
        total_gb = round(mem.total / (1024**3), 2)
        
        html.append("<div class='card'>")
        html.append("<div>🧠 MEMORY AVAILABLE</div>")
        html.append(f"<div class='value'>{avail_gb}G <span class='label'>/ {total_gb}G</span></div>")
        html.append("</div>")
    except: pass
        
    return "".join(html)

@app.route('/')
def dashboard():
    return get_html_status()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
