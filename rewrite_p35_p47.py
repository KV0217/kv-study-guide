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
# PHASE 35 -- Data Storytelling
# ============================================================

# Block [0]: matplotlib/seaborn visualization
rep(
'<div class="code-block"><pre>import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# Set style\nsns.set_theme(style="whitegrid", palette="muted")',
'<div class="code-block"><pre>import pandas as pd              # data manipulation and loading\nimport matplotlib.pyplot as plt  # core plotting library (figures, axes, labels)\nimport seaborn as sns            # statistical visualization built on matplotlib\n\n# Set style\nsns.set_theme(style="whitegrid", palette="muted")'
)

# Block [2]: Plotly interactive charts
rep(
'<div class="code-block"><pre>import plotly.express as px\nimport plotly.graph_objects as go\n\n# Interactive line chart',
'<div class="code-block"><pre>import plotly.express as px          # high-level API: one-line interactive charts\nimport plotly.graph_objects as go    # low-level API: full control over chart elements\n\n# Interactive line chart'
)

# Block [3]: EDA narrative function
rep(
'<div class="code-block"><pre>import pandas as pd\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\n# Complete EDA narrative structure\ndef tell_the_story(df, target_col):',
'<div class="code-block"><pre>import pandas as pd              # data loading and aggregation\nimport matplotlib.pyplot as plt  # plotting distributions and charts\nimport seaborn as sns            # heatmaps and styled plots\n\n# Complete EDA narrative structure -- wraps common EDA steps into a single function\ndef tell_the_story(df, target_col):'
)

print(f"p35 done ({replaced} replacements so far)")

# ============================================================
# PHASE 36 -- Statistics: fix remaining missed block
# ============================================================

# Block [4]: t-test with sample array
rep(
'<div class="code-block"><pre>import numpy as np\nimport scipy.stats as stats\n\nsample = np.array([12.5, 11.8, 13.2, 12.1, 12.9, 11.5, 13.0, 12.7])',
'<div class="code-block"><pre>import numpy as np               # array creation and mean/std calculations\nimport scipy.stats as stats      # t-test, confidence intervals, p-values\n\nsample = np.array([12.5, 11.8, 13.2, 12.1, 12.9, 11.5, 13.0, 12.7])'
)

print(f"p36 done ({replaced} replacements so far)")

# ============================================================
# PHASE 38 -- Recommendation Systems
# ============================================================

# Block [0]: User-Item matrix + collaborative filtering
rep(
'<div class="code-block"><pre>import numpy as np\nimport pandas as pd\nfrom scipy.sparse import csr_matrix\nfrom sklearn.metrics.pairwise import cosine_similarity',
'<div class="code-block"><pre>import numpy as np               # array operations\nimport pandas as pd              # create pivot tables from ratings data\nfrom scipy.sparse import csr_matrix  # memory-efficient sparse matrix (most ratings are 0)\nfrom sklearn.metrics.pairwise import cosine_similarity  # compute user/item similarity'
)

# Block [1]: SVD matrix factorization
rep(
'<div class="code-block"><pre>from scipy.sparse.linalg import svds\nimport numpy as np\n\n# Core idea: decompose the user-item matrix into latent factors',
'<div class="code-block"><pre>from scipy.sparse.linalg import svds  # truncated SVD for sparse matrices (memory efficient)\nimport numpy as np                    # matrix operations and reconstruction\n\n# Core idea: decompose the user-item matrix into latent factors'
)

# Block [2]: Content-based filtering with TF-IDF
rep(
'<div class="code-block"><pre>from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.metrics.pairwise import cosine_similarity\nimport pandas as pd\n\n# Uses item features (title, description, genre, tags)',
'<div class="code-block"><pre>from sklearn.feature_extraction.text import TfidfVectorizer  # convert text descriptions to vectors\nfrom sklearn.metrics.pairwise import cosine_similarity  # measure similarity between items\nimport pandas as pd                # store movie data as a DataFrame\n\n# Uses item features (title, description, genre, tags)'
)

# Block [3]: Two-Tower neural network
rep(
'<div class="code-block"><pre>import torch\nimport torch.nn as nn\n\n# Modern approach at scale (used by YouTube, Pinterest, Spotify)',
'<div class="code-block"><pre>import torch                # PyTorch deep learning framework\nimport torch.nn as nn       # neural network layers (Linear, ReLU, Sequential)\n\n# Modern approach at scale (used by YouTube, Pinterest, Spotify)'
)

# Block [4]: Recommendation metrics
rep(
'<div class="code-block"><pre>import numpy as np\n\n# Precision@K: of top K recommendations, how many are relevant?',
'<div class="code-block"><pre>import numpy as np  # used for log calculations in NDCG\n\n# Precision@K: of top K recommendations, how many are relevant?'
)

print(f"p38 done ({replaced} replacements so far)")

# ============================================================
# PHASE 39 -- Business Case / Metric Drop
# ============================================================

# Block [1]: investigate_metric_drop function
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# Template for isolating a metric change\ndef investigate_metric_drop(df, metric_col, date_col, breakdown_cols):',
'<div class="code-block"><pre>import pandas as pd  # groupby, before/after comparison, percentage change\n\n# Template for isolating a metric change\ndef investigate_metric_drop(df, metric_col, date_col, breakdown_cols):'
)

print(f"p39 done ({replaced} replacements so far)")

# ============================================================
# PHASE 40 -- NLP
# ============================================================

# Block [0]: text preprocessing pipeline
rep(
'<div class="code-block"><pre>import re\nimport nltk\nfrom nltk.tokenize import word_tokenize\nfrom nltk.corpus import stopwords\nfrom nltk.stem import PorterStemmer, WordNetLemmatizer',
'<div class="code-block"><pre>import re                            # regular expressions for cleaning text\nimport nltk                          # Natural Language Toolkit -- tokenization, stopwords, stemming\nfrom nltk.tokenize import word_tokenize   # split text into individual word tokens\nfrom nltk.corpus import stopwords         # common words to remove (the, a, is, ...)\nfrom nltk.stem import PorterStemmer, WordNetLemmatizer  # reduce words to root form'
)

# Block [1]: BoW + TF-IDF
rep(
'<div class="code-block"><pre>from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\n\ncorpus = [',
'<div class="code-block"><pre>from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer\n# CountVectorizer: counts word occurrences (Bag of Words)\n# TfidfVectorizer: weights words by how unique they are to each document\n\ncorpus = ['
)

# Block [2]: Word2Vec / GloVe embeddings
rep(
'<div class="code-block"><pre>\n# Problem with TF-IDF: "cat" and "feline" are completely di',
'<div class="code-block"><pre># Problem with TF-IDF: "cat" and "feline" are completely di'
)

# Block [3]: TF-IDF + LogReg pipeline + BERT
rep(
'<div class="code-block"><pre>import pandas as pd\nfrom sklearn.pipeline import Pipeline\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import classification_report\n\n# TF-IDF + Logistic Regression',
'<div class="code-block"><pre>import pandas as pd                  # load CSV reviews dataset\nfrom sklearn.pipeline import Pipeline  # chain vectorizer + classifier into one step\nfrom sklearn.feature_extraction.text import TfidfVectorizer  # text -> numeric features\nfrom sklearn.linear_model import LogisticRegression  # fast and strong text classifier\nfrom sklearn.model_selection import train_test_split  # hold out test set\nfrom sklearn.metrics import classification_report    # precision, recall, F1 per class\n\n# TF-IDF + Logistic Regression'
)

print(f"p40 done ({replaced} replacements so far)")

# ============================================================
# PHASE 41 -- Anomaly Detection
# ============================================================

# Block [0]: Z-score + IQR
rep(
'<div class="code-block"><pre>import numpy as np\nimport pandas as pd\nfrom scipy import stats\n\n# Method 1: Z-score (assumes normal distribution)',
'<div class="code-block"><pre>import numpy as np               # absolute values and array operations\nimport pandas as pd              # apply anomaly flags as DataFrame columns\nfrom scipy import stats          # zscore function and robust statistics\n\n# Method 1: Z-score (assumes normal distribution)'
)

# Block [1]: Isolation Forest
rep(
'<div class="code-block"><pre>from sklearn.ensemble import IsolationForest\nimport numpy as np\nimport pandas as pd\n\n# Key intuition: anomalies are EASIER to isolate',
'<div class="code-block"><pre>from sklearn.ensemble import IsolationForest  # tree-based unsupervised anomaly detector\nimport numpy as np               # array slicing and operations\nimport pandas as pd              # input DataFrame, store predictions as a column\n\n# Key intuition: anomalies are EASIER to isolate'
)

# Block [2]: Local Outlier Factor
rep(
'<div class="code-block"><pre>from sklearn.neighbors import LocalOutlierFactor\n\n# LOF compares the local density',
'<div class="code-block"><pre>from sklearn.neighbors import LocalOutlierFactor  # density-based unsupervised anomaly detection\n\n# LOF compares the local density'
)

# Block [3]: Autoencoder anomaly detection
rep(
'<div class="code-block"><pre>import torch\nimport torch.nn as nn\nimport numpy as np\n\n# Autoencoder learns to compress normal data',
'<div class="code-block"><pre>import torch              # deep learning framework\nimport torch.nn as nn     # neural network layers (Linear, ReLU)\nimport numpy as np        # convert tensors to numpy for threshold calculation\n\n# Autoencoder learns to compress normal data'
)

# Block [4]: XGBoost fraud detection
rep(
'<div class="code-block"><pre>from xgboost import XGBClassifier\nfrom sklearn.metrics import classification_report, roc_auc_score\n\n# If you HAVE labeled fraud/anomaly examples',
'<div class="code-block"><pre>from xgboost import XGBClassifier    # gradient boosted trees: best for tabular fraud data\nfrom sklearn.metrics import classification_report, roc_auc_score  # evaluate on imbalanced data\n\n# If you HAVE labeled fraud/anomaly examples'
)

print(f"p41 done ({replaced} replacements so far)")

# ============================================================
# PHASE 44 -- Linear Algebra
# ============================================================

# Block [0]: Scalars, vectors, matrices
rep(
'<div class="code-block"><pre>import numpy as np\n\n# Scalar: a single number\ntemperature = 36.6',
'<div class="code-block"><pre>import numpy as np  # numerical computing -- the foundation of linear algebra in Python\n\n# Scalar: a single number\ntemperature = 36.6'
)

# Block [1]: Dot product
rep(
'<div class="code-block"><pre>import numpy as np\n\n# Dot product: element-wise multiply then sum\na = np.array([3, 4, 1])',
'<div class="code-block"><pre>import numpy as np  # np.dot and np.linalg for vector operations\n\n# Dot product: element-wise multiply then sum\na = np.array([3, 4, 1])'
)

# Block [2]: Matrix multiplication
rep(
'<div class="code-block"><pre>import numpy as np\n\n# Matrix multiplication: (m x n) x (n x p) = (m x p)',
'<div class="code-block"><pre>import numpy as np  # @ operator and np.dot for matrix multiplication\n\n# Matrix multiplication: (m x n) x (n x p) = (m x p)'
)

# Block [3]: Eigenvalues and eigenvectors
rep(
'<div class="code-block"><pre>import numpy as np\n\n# Intuition: for a matrix A, an eigenvector v has the special property:',
'<div class="code-block"><pre>import numpy as np  # np.linalg.eig to compute eigenvalues and eigenvectors\n\n# Intuition: for a matrix A, an eigenvector v has the special property:'
)

# Block [4]: Norms
rep(
'<div class="code-block"><pre>import numpy as np\n\nv = np.array([3, 4, 0])\n\n# L1 norm (Manhattan)',
'<div class="code-block"><pre>import numpy as np  # np.linalg.norm for L1/L2/Linfinity norms\n\nv = np.array([3, 4, 0])  # 3D vector example\n\n# L1 norm (Manhattan)'
)

print(f"p44 done ({replaced} replacements so far)")

# ============================================================
# PHASE 45 -- Calculus / Optimization
# ============================================================

# Block [0]: derivatives + gradient descent intuition
rep(
'<div class="code-block"><pre>import numpy as np\nimport matplotlib.pyplot as plt\n\n# Simple example: Loss = w²',
'<div class="code-block"><pre>import numpy as np               # array operations for computing loss and gradients\nimport matplotlib.pyplot as plt  # visualise the loss curve and gradient descent path\n\n# Simple example: Loss = w²'
)

# Block [2]: gradient descent variants
rep(
'<div class="code-block"><pre>import numpy as np\n\n# The full gradient descent update rule:',
'<div class="code-block"><pre>import numpy as np  # array operations for weight updates\n\n# The full gradient descent update rule:'
)

# Block [3]: SGD + learning rate schedules
rep(
'<div class="code-block"><pre>from sklearn.linear_model import SGDClassifier\nimport torch.optim as optim\n\n# Learning rate schedules',
'<div class="code-block"><pre>from sklearn.linear_model import SGDClassifier  # sklearn mini-batch SGD classifier\nimport torch.optim as optim  # PyTorch optimizers (Adam, SGD) and LR schedulers\n\n# Learning rate schedules'
)

# Block [4]: partial derivatives + gradient
rep(
'<div class="code-block"><pre>import numpy as np\n\n# When loss depends on MULTIPLE parameters (w1, w2, w3, ...),',
'<div class="code-block"><pre>import numpy as np  # array to store gradient vector [dL/dw1, dL/dw2, ...]\n\n# When loss depends on MULTIPLE parameters (w1, w2, w3, ...),'
)

print(f"p45 done ({replaced} replacements so far)")

# ============================================================
# PHASE 46 -- OOP for DS
# ============================================================

# Block [2]: sklearn Transformer
rep(
'<div class="code-block"><pre>from sklearn.base import BaseEstimator, TransformerMixin\n\n#',
'<div class="code-block"><pre>from sklearn.base import BaseEstimator, TransformerMixin\n# BaseEstimator: auto get_params/set_params (needed for GridSearchCV)\n# TransformerMixin: auto fit_transform method\n\n#'
)

# Block [5]: dataclasses
rep(
'<div class="code-block"><pre>from dataclasses import dataclass, field\nfrom typing import',
'<div class="code-block"><pre>from dataclasses import dataclass, field  # auto-generate __init__, __repr__, __eq__\nfrom typing import'
)

print(f"p46 done ({replaced} replacements so far)")

# ============================================================
# PHASE 42 -- Git & DVC (bash blocks -- just verify, minimal changes needed)
# Block [0] is bash -- already has # comments
# ============================================================

print(f"\nTotal replacements: {replaced}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
