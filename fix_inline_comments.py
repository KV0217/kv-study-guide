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

# ============================================================
# p37 -- mid-block import lines
# ============================================================

# block[0]: LinearRegression + statsmodels mid-block (after cross-val section)
rep(
'from sklearn.linear_model import LinearRegression\nimport statsmodels.api as sm',
'from sklearn.linear_model import LinearRegression  # sklearn version: predict, score\nimport statsmodels.api as sm  # statsmodels: p-values, confidence intervals, OLS summary'
)

rep(
'from sklearn.linear_model import ElasticNet\n',
'from sklearn.linear_model import ElasticNet  # combines L1+L2 penalty (best of Lasso+Ridge)\n'
)

# block[1]: LogisticRegression -- import pandas mid-block
rep(
'from sklearn.metrics import roc_curve\nimport pandas as pd\n',
'from sklearn.metrics import roc_curve  # compute ROC curve points\nimport pandas as pd  # display feature coefficients as a table\n'
)

# block[2]: DecisionTree -- numpy mid-block
rep(
'<div class="code-block"><pre>from sklearn.tree import DecisionTreeClassifier, export_text  # tree model + text visualisation\nimport numpy as np\n',
'<div class="code-block"><pre>from sklearn.tree import DecisionTreeClassifier, export_text  # tree model + text visualisation\nimport numpy as np  # array operations for feature indices\n'
)

# block[3]: RandomForest -- numpy mid-block
rep(
'<div class="code-block"><pre>from sklearn.ensemble import RandomForestClassifier  # ensemble of decision trees\nimport numpy as np\n',
'<div class="code-block"><pre>from sklearn.ensemble import RandomForestClassifier  # ensemble of decision trees\nimport numpy as np  # array slicing for top feature selection\n'
)

# block[6]: KMeans -- silhouette mid-block
rep(
'from sklearn.metrics import silhouette_score\n',
'from sklearn.metrics import silhouette_score  # measure cluster quality (-1 bad, +1 perfect)\n'
)

print(f"p37 done ({replaced} replacements so far)")

# ============================================================
# p40 -- fix import lines that have next-line comments but not inline
# ============================================================

# block[1]: CountVectorizer/TfidfVectorizer -- move comment inline
rep(
'from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\n# CountVectorizer: counts word occurrences (Bag of Words)\n# TfidfVectorizer: weights words by how unique they are to each document\n',
'from sklearn.feature_extraction.text import CountVectorizer  # BoW: counts occurrences\nfrom sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF: weights by term rarity across docs\n'
)

# block[2]: gensim, nltk, torchtext, numpy mid-block
rep(
'from gensim.models import Word2Vec\nimport nltk\n',
'from gensim.models import Word2Vec  # train word embeddings (skip-gram or CBOW)\nimport nltk  # Natural Language Toolkit -- tokenization utilities\n'
)

rep(
'import torchtext\n',
'import torchtext  # pretrained GloVe/FastText word vectors\n'
)

rep(
'import numpy as np\ndef doc_embedding',
'import numpy as np  # average word vectors to create document embeddings\ndef doc_embedding'
)

# block[3]: transformers + torch mid-block
rep(
'from transformers import AutoTokenizer, AutoModel\nimport torch\n',
'from transformers import AutoTokenizer, AutoModel  # HuggingFace BERT tokenizer and model\nimport torch  # needed to run BERT inference without gradient computation\n'
)

print(f"p40 done ({replaced} replacements so far)")

# ============================================================
# p41 -- remaining mid-block
# ============================================================
# p41 block[1] line 22 was IsolationForest -- mid-block in p31 not p41
# p41 scan shows 1 missing -- let's check which it is
# (previously checked: p41 block[1] in rewrite_p35_p47 was fixed)
# The scanner shows p41 still has 1 missing

# ============================================================
# p43 -- shell/venv blocks
# ============================================================
# These are bash/shell command blocks -- 2 missing import-style lines
# They're likely `import` in shell-format, not Python

# ============================================================
# p44 -- 3 remaining
# ============================================================
# These were replacements that may have failed due to unicode
# Let me check what's remaining

# ============================================================
# p46 -- fix blocks with next-line comments
# ============================================================

# block[2]: sklearn.base inline fix
rep(
'from sklearn.base import BaseEstimator, TransformerMixin\n# BaseEstimator: auto get_params/set_params (needed for GridSearchCV)\n# TransformerMixin: auto fit_transform method',
'from sklearn.base import BaseEstimator, TransformerMixin  # base classes for custom sklearn transformers\n# BaseEstimator: auto get_params/set_params (needed for GridSearchCV)\n# TransformerMixin: auto fit_transform method'
)

# block[2]: Pipeline mid-block
rep(
'from sklearn.pipeline import Pipeline\npipe = Pipeline',
'from sklearn.pipeline import Pipeline  # chain transformers into a single object\npipe = Pipeline'
)

# block[3]: torch + TorchDataset mid-block
rep(
'import torch\nfrom torch.utils.data import Dataset as TorchDataset\n',
'import torch  # PyTorch tensors for GPU-accelerated data loading\nfrom torch.utils.data import Dataset as TorchDataset  # base class for custom datasets\n'
)

# block[5]: typing imports
rep(
'from dataclasses import dataclass, field  # auto-generate __init__, __repr__, __eq__\nfrom typing import',
'from dataclasses import dataclass, field  # auto-generate __init__, __repr__, __eq__\nfrom typing import'
)

# typing import already commented -- need to check what's on that line
# Let's also fix the from typing import line and from dataclasses import asdict
rep(
'from dataclasses import asdict\n',
'from dataclasses import asdict  # convert dataclass to dictionary\n'
)

# block[6]: imports inside function bodies
rep(
'        import re\n',
'        import re  # regex: remove punctuation, clean URLs\n'
)

rep(
'import time\n',
'import time  # measure function execution duration\n'
)

print(f"p46 done ({replaced} replacements so far)")

# ============================================================
# p46 block[5]: typing List Optional
# ============================================================
rep(
'\nfrom typing import List, Optional\n',
'\nfrom typing import List, Optional  # type hints for function signatures\n'
)

# ============================================================
# p48 -- indented imports inside functions
# ============================================================

rep(
'    import matplotlib.pyplot as plt\n    plt.figure',
'    import matplotlib.pyplot as plt  # plot feature importance chart\n    plt.figure'
)

rep(
'    from sklearn.ensemble import GradientBoostingClassifier\n',
'    from sklearn.ensemble import GradientBoostingClassifier  # sklearn GBM variant\n'
)

rep(
'    import xgboost as xgb\n',
'    import xgboost as xgb  # native XGBoost API for DMatrix training\n'
)

rep(
'            from mlflow.tracking import MlflowClient\n',
'            from mlflow.tracking import MlflowClient  # query experiment runs programmatically\n'
)

print(f"p48 done ({replaced} replacements so far)")

# ============================================================
# p49 -- indented imports inside Airflow task functions
# ============================================================

rep(
'def extract_data():\n    import pandas as pd\n    df = pd.read_sql',
'def extract_data():\n    import pandas as pd  # local import: loads only when task runs, not at DAG parse time\n    df = pd.read_sql'
)

rep(
'def transform_data():\n    import pandas as pd\n    df = pd.read_csv("/tmp/raw_orders.csv")',
'def transform_data():\n    import pandas as pd  # local import: avoids loading pandas during DAG parsing\n    df = pd.read_csv("/tmp/raw_orders.csv")'
)

rep(
'def load_to_warehouse():\n    import pandas as pd\n    df = pd.read_csv("/tmp/transformed_orders.csv")',
'def load_to_warehouse():\n    import pandas as pd  # local import inside task function\n    df = pd.read_csv("/tmp/transformed_orders.csv")'
)

print(f"p49 done ({replaced} replacements so far)")

# ============================================================
# p50 -- remaining pyspark imports
# ============================================================

rep(
'from pyspark.ml.evaluation import BinaryClassificationEvaluator\n',
'from pyspark.ml.evaluation import BinaryClassificationEvaluator  # AUC evaluator for Spark ML\n'
)

rep(
'from pyspark.ml import PipelineModel\n',
'from pyspark.ml import PipelineModel  # load a saved Spark ML pipeline\n'
)

print(f"p50 done ({replaced} replacements so far)")

print(f"\nTotal replacements: {replaced}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
