# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── Inject CSS right before </style> ─────────────────────────────────────────
new_css = """
/* ── CONCEPT CARD (p53+) ──────────────────────────────────────────────────── */
.concept-card{background:#fff;border:1.5px solid #e2e8f0;border-radius:12px;
  margin:12px 20px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.06);}
.concept-title{font-size:14px;font-weight:700;color:#0f172a;
  padding:13px 18px 10px;border-bottom:1px solid #f1f5f9;margin:0;}
.concept-body{padding:14px 18px;}
.phase-badge{display:inline-block;background:linear-gradient(135deg,#3b82f6,#6366f1);
  color:#fff;font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;
  letter-spacing:.5px;text-transform:uppercase;margin-bottom:6px;}
.phase-title{font-size:20px;font-weight:800;color:#f1f5f9;margin:4px 0;}
.phase-subtitle{font-size:13px;color:#94a3b8;margin:3px 0 0;}
.qa-item{margin-bottom:16px;padding:12px 14px;background:#f8fafc;border-radius:8px;
  border-left:3px solid #3b82f6;}
.question{font-weight:700;color:#0f172a;font-size:13px;margin-bottom:5px;}
.answer{color:#475569;font-size:12.5px;line-height:1.75;}
.alert-box{padding:12px 16px;border-radius:8px;margin:12px 0;font-size:13px;}
.info-box{background:#eff6ff;border-left:4px solid #3b82f6;color:#1e40af;}
.warn-box{background:#fffbeb;border-left:4px solid #f59e0b;color:#92400e;}
.data-table{width:100%;border-collapse:collapse;margin-top:10px;border-radius:8px;overflow:hidden;}
.data-table th{background:#1e293b;color:#7dd3fc;font-size:11px;font-weight:600;
  padding:9px 13px;text-align:left;}
.data-table td{padding:9px 13px;border-bottom:1px solid #f1f5f9;font-size:12.5px;
  color:#475569;vertical-align:top;line-height:1.6;}
.data-table tr:last-child td{border-bottom:none;}
.data-table tr:hover td{background:#f8fafc;}

/* ── P30–P52 LEGACY STRUCTURE — give proper spacing ──────────────────────── */
.phase-section>h2{padding:22px 32px 16px;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 60%,#0c2a4a 100%);
  border-bottom:3px solid #3b82f6;color:#f1f5f9;font-size:18px;
  font-weight:700;margin:0 0 4px 0;}
.phase-section>h3{margin:22px 24px 8px;font-size:14px;font-weight:700;
  color:#0f172a;padding-bottom:5px;border-bottom:2px solid #e2e8f0;}
.phase-section>p{margin:8px 24px;color:#475569;font-size:13px;line-height:1.7;}
.phase-section>.code-block{margin:10px 24px;}
.phase-section>table{margin:10px 24px;width:calc(100% - 48px);
  border-collapse:collapse;border-radius:8px;overflow:hidden;}
.phase-section>table th{background:#1e293b;color:#7dd3fc;font-size:11px;
  font-weight:600;padding:9px 13px;text-align:left;}
.phase-section>table td{padding:9px 13px;border-bottom:1px solid #f1f5f9;
  font-size:12.5px;color:#475569;vertical-align:top;line-height:1.6;}
.phase-section>table tr:hover td{background:#f8fafc;}
.phase-section>.concept-box{margin:10px 24px;}
.phase-section>ul,.phase-section>ol{margin:8px 24px 8px 44px;
  color:#475569;font-size:13px;line-height:1.8;}
.phase-section>svg{display:block;margin:14px auto;}
.concept-box{background:#fff8e1;border-left:4px solid #f59e0b;border-radius:0 8px 8px 0;
  padding:12px 16px;font-size:13px;color:#334155;line-height:1.75;}
"""

# Inject before closing </style>
html = html.replace("</style>", new_css + "\n</style>", 1)

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"CSS injected — {kb:.0f} KB")
