# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

replaced = 0

def rep(old, new):
    global html, replaced
    if old in html:
        html = html.replace(old, new, 1)
        replaced += 1
        return True
    print(f"MISS: {old[:60]!r}")
    return False

# p37 block[1]: pandas import mid-block
rep(
'# Feature importance (coefficient magnitude)\nimport pandas as pd\n',
'# Feature importance (coefficient magnitude)\nimport pandas as pd  # display coefficients as a sorted table\n'
)

# p48 block[0]: matplotlib inside artifact logging section
rep(
'    # Log any file as artifact (charts, reports, data samples)\n    import matplotlib.pyplot as plt\n',
'    # Log any file as artifact (charts, reports, data samples)\n    import matplotlib.pyplot as plt  # create feature importance chart to log as MLflow artifact\n'
)

print(f"Fixed {replaced} items")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

# Final count
import re

with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

phases = [f'p{i}' for i in range(30, 53)]
total = 0
for ph in phases:
    next_ph = f'p{int(ph[1:])+1}'
    idx = html.find(f'id="{ph}"')
    idx_next = html.find(f'id="{next_ph}"')
    if idx == -1: continue
    seg = html[idx:idx_next]
    blocks = re.findall(r'<div class="code-block"><pre>(.*?)</pre></div>', seg, re.DOTALL)
    c = 0
    for block in blocks:
        for line in block.split('\n'):
            s = line.strip()
            if (s.startswith('import ') or s.startswith('from ')) and '#' not in line:
                c += 1
                total += 1
    if c > 0:
        print(f'{ph}: {c} still missing')

kb = len(html) / 1024
print(f"\nTotal remaining: {total}")
print(f"File size: {kb:.0f} KB")
