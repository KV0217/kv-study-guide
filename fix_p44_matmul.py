# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

old = '<div class="code-block"><pre>import numpy as np\n\n# Matrix multiplication: (m×n) × (n×p) = (m×p)'
new = '<div class="code-block"><pre>import numpy as np  # @ operator and np.dot for matrix multiplication\n\n# Matrix multiplication: (m×n) × (n×p) = (m×p)'

if old in html:
    html = html.replace(old, new, 1)
    print("Fixed p44 matrix multiply block")
else:
    print("MISS")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
