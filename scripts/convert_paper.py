import os
import re

base_dir = r"C:\Users\user\.gemini\antigravity-ide\scratch\edupro_analysis"
md_path = os.path.join(base_dir, "deliverables", "research_paper.md")
html_path = os.path.join(base_dir, "deliverables", "research_paper.html")

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learner Demographics and Course Enrollment Behavior Analysis on EduPro</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,300&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
        
        body {
            font-family: 'Merriweather', Georgia, serif;
            line-height: 1.8;
            color: #1e293b;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 30px;
            background: #ffffff;
        }
        .header-bar {
            position: sticky;
            top: 0;
            background: #0f172a;
            color: #ffffff;
            padding: 14px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 12px;
            margin-bottom: 40px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            z-index: 100;
        }
        .header-bar span {
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.02em;
        }
        .btn-print {
            background: #4f46e5;
            color: #ffffff;
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 700;
            font-size: 13px;
            transition: background 0.2s;
        }
        .btn-print:hover {
            background: #4338ca;
        }
        h1 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 28px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.3;
            margin-bottom: 8px;
            text-align: center;
        }
        .subtitle {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 16px;
            color: #475569;
            text-align: center;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .meta-info {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            color: #64748b;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 20px;
            line-height: 1.6;
        }
        h2 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 6px;
            margin-top: 40px;
        }
        h3 {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
            margin-top: 24px;
        }
        p {
            font-size: 15px;
            margin-bottom: 16px;
            text-align: justify;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13.5px;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 10px 12px;
            text-align: left;
        }
        th {
            background: #f1f5f9;
            font-weight: 700;
            color: #0f172a;
        }
        tr:nth-child(even) {
            background: #f8fafc;
        }
        pre {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 14px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: Consolas, Monaco, monospace;
            font-size: 13px;
            line-height: 1.5;
            color: #0f172a;
        }
        code {
            font-family: Consolas, Monaco, monospace;
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 13px;
        }
        @media print {
            .header-bar { display: none; }
            body { margin: 10mm; padding: 0; }
        }
    </style>
</head>
<body>
    <div class="header-bar">
        <span>📄 EduPro Research Paper — Academic Pre-Print & Policy Documentation</span>
        <button class="btn-print" onclick="window.print()">🖨️ Download / Print as PDF</button>
    </div>
"""

lines = md_content.split("\n")
in_table = False

for l in lines:
    ls = l.strip()
    if ls.startswith("# "):
        html_content += f"<h1>{ls[2:]}</h1>\n"
    elif ls.startswith("## "):
        html_content += f"<h2>{ls[3:]}</h2>\n"
    elif ls.startswith("### "):
        html_content += f"<h3>{ls[4:]}</h3>\n"
    elif ls.startswith("|") and ls.endswith("|"):
        parts = [p.strip() for p in ls.split("|")[1:-1]]
        if all(set(p).issubset({"-", ":", " "}) for p in parts):
            continue
        if not in_table:
            in_table = True
            html_content += "<table>\n<thead><tr>" + "".join(f"<th>{p}</th>" for p in parts) + "</tr></thead>\n<tbody>\n"
        else:
            html_content += "<tr>" + "".join(f"<td>{p}</td>" for p in parts) + "</tr>\n"
    else:
        if in_table:
            html_content += "</tbody>\n</table>\n"
            in_table = False
        if ls.startswith("```"):
            if ls == "```":
                html_content += "</pre>\n"
            else:
                html_content += "<pre>\n"
        elif ls == "---":
            html_content += "<hr style='margin: 25px 0; border: 0; border-top: 1px solid #e2e8f0;'>\n"
        elif ls != "":
            formatted = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", ls)
            formatted = re.sub(r"\*(.*?)\*", r"<em>\1</em>", formatted)
            html_content += f"<p>{formatted}</p>\n"

if in_table:
    html_content += "</tbody>\n</table>\n"

html_content += "</body>\n</html>"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Saved HTML research paper successfully to:", html_path)
