# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

old = '\n# --- Make predictions ---\nimport numpy as np\nresult = predictor'
new = '\n# --- Make predictions ---\nimport numpy as np  # wrap input list as array for prediction\nresult = predictor'

if old in html:
    html = html.replace(old, new, 1)
    print("Fixed p52 sagemaker numpy import")
else:
    print("MISS - checking context...")
    # Try just the line
    if 'import numpy as np\nresult = predictor' in html:
        html = html.replace('import numpy as np\nresult = predictor',
                           'import numpy as np  # wrap input list as array for prediction\nresult = predictor', 1)
        print("Fixed via alternate pattern")
    else:
        print("Could not find target")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
