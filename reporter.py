from datetime import datetime

def generate_report(target, nmap_data, gobuster_data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report_filename = f"reports/report_{target.replace('.', '_')}.html"

    html = f"""
    <html>
    <head>
        <title>Vulnerability Scan Report - {target}</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            h1 {{ color: #007acc; }}
            pre {{ background: #f4f4f4; padding: 10px; border-left: 4px solid #007acc; }}
        </style>
    </head>
    <body>
        <h1>Vulnerability Report for {target}</h1>
        <p><strong>Scan Timestamp:</strong> {timestamp}</p>

        <h2>🛡️ Open Ports (Nmap)</h2>
        <pre>{chr(10).join(nmap_data)}</pre>

        <h2>📂 Discovered Directories (Gobuster)</h2>
        <pre>{chr(10).join(gobuster_data)}</pre>
    </body>
    </html>
    """

    with open(report_filename, "w") as file:
        file.write(html)

    print(f"📄 Report generated: {report_filename}")