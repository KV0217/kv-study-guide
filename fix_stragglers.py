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

# p31 block[1]: IsolationForest mid-block (has em-dash header above)
rep(
'\nfrom sklearn.ensemble import IsolationForest\niso = IsolationForest',
'\nfrom sklearn.ensemble import IsolationForest  # tree-based outlier detector: anomalies get isolated in fewer splits\niso = IsolationForest'
)

# p32 block[2]: torchvision mid-block
rep(
'\nfrom torchvision import models\nresnet = models.resnet50',
'\nfrom torchvision import models  # pretrained model zoo (ResNet, VGG, EfficientNet, etc.)\nresnet = models.resnet50'
)

# p36 block[0]: fractions (first line of block)
rep(
'<div class="code-block"><pre>from fractions import Fraction\n',
'<div class="code-block"><pre>from fractions import Fraction  # exact rational arithmetic for demonstrating probability rules\n'
)

# p37 block[6]: silhouette mid-block
rep(
'from sklearn.metrics import silhouette_score\nscores = []',
'from sklearn.metrics import silhouette_score  # measure cluster quality (-1 worst, +1 best)\nscores = []'
)

# p38 block[1]: implicit ALS mid-block
rep(
'from implicit import als\nmodel = als.AlternatingLeastSquares',
'from implicit import als  # library for implicit feedback (clicks/purchases, not star ratings)\nmodel = als.AlternatingLeastSquares'
)

# p41 block[4]: precision_recall metrics mid-block
rep(
'from sklearn.metrics import average_precision_score, precision_recall_curve\n',
'from sklearn.metrics import average_precision_score, precision_recall_curve  # for rare event evaluation\n'
)

# p43 block[5]: os + dotenv
rep(
'import os\nfrom dotenv import load_dotenv\n',
'import os  # read environment variables with os.environ[]\nfrom dotenv import load_dotenv  # load .env file into environment variables\n'
)

# p44 block[3]: PCA imports mid-block
rep(
'from sklearn.preprocessing import StandardScaler\nfrom sklearn.decomposition import PCA\nimport numpy as np\n',
'from sklearn.preprocessing import StandardScaler  # scale features to zero mean, unit variance before PCA\nfrom sklearn.decomposition import PCA  # Principal Component Analysis: find directions of max variance\nimport numpy as np  # array operations and explained variance calculations\n'
)

# p45 block[1]: torch mid-block (chain rule section)
rep(
'\nimport torch\n\n',
'\nimport torch  # autograd: compute gradients of any computation graph automatically\n\n'
)

# p46 block[6]: time mid-block
rep(
'\nimport time\n',
'\nimport time  # time.time() used inside timing decorator\n'
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
