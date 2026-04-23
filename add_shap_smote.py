# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 1. SHAP PLOTS -- inject into p53 before closing </div>
# ============================================================

shap_content = '''
  <!-- SHAP Plot Types -->
  <div class="concept-card">
    <h3 class="concept-title">SHAP Plot Types — Complete Visual Guide</h3>
    <div class="concept-body">
      <p>SHAP has 6 core plot types. Each answers a different question about your model.</p>
      <table class="data-table">
        <thead><tr><th>Plot</th><th>Question it answers</th><th>Scope</th><th>Best used when</th></tr></thead>
        <tbody>
          <tr><td><strong>Bar</strong></td><td>Which features matter most overall?</td><td>Global</td><td>First step: quick feature ranking</td></tr>
          <tr><td><strong>Beeswarm</strong></td><td>Which features matter AND how does value affect direction?</td><td>Global</td><td>Main explainability slide — shows everything</td></tr>
          <tr><td><strong>Waterfall</strong></td><td>Why did the model predict X for THIS row?</td><td>Local (1 row)</td><td>Explaining a single decision (loan, fraud alert)</td></tr>
          <tr><td><strong>Force</strong></td><td>Visual waterfall — stacked for many rows</td><td>Local or global</td><td>Interactive dashboards, presentations</td></tr>
          <tr><td><strong>Scatter / Dependence</strong></td><td>How does feature value relate to its SHAP impact?</td><td>Global (1 feature)</td><td>Finding thresholds and non-linearities</td></tr>
          <tr><td><strong>Heatmap</strong></td><td>How do all features × all samples look together?</td><td>Global</td><td>Spotting clusters and outlier rows</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Bar Plot -->
  <div class="concept-card">
    <h3 class="concept-title">1. Bar Plot — Global Feature Importance</h3>
    <div class="concept-body">
      <p><strong>What it shows:</strong> Mean absolute SHAP value per feature. Longer bar = more impact on average.</p>
      <p><strong>Limitation:</strong> Does NOT show direction — a feature that always pushes predictions up looks identical to one that always pushes them down.</p>
      <div class="code-block"><pre>import shap                          # SHAP library
import xgboost as xgb                # model we want to explain
from sklearn.datasets import load_breast_cancer  # sample dataset
from sklearn.model_selection import train_test_split  # hold-out split
import matplotlib.pyplot as plt      # show plots inline

# --- Train a model ---
data = load_breast_cancer()          # 569 samples, 30 features, binary target
X, y = data.data, data.target        # features and labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss")
model.fit(X_train, y_train)          # train XGBoost classifier

# --- Compute SHAP values ---
explainer = shap.Explainer(model)    # auto-detects TreeExplainer for tree models
shap_values = explainer(X_test)      # shap_values.values shape: (n_samples, n_features)

# --- Bar plot ---
shap.plots.bar(shap_values)          # ranks features by mean |SHAP value|
# Each bar = average impact magnitude across all test samples
# Top bar = most important feature globally</pre></div>
      <div class="alert-box info-box" style="margin:10px 0 0;">
        <strong>Interview tip:</strong> "I use the bar plot first to get a quick global ranking, then switch to beeswarm to understand direction and distribution."
      </div>
    </div>
  </div>

  <!-- Beeswarm Plot -->
  <div class="concept-card">
    <h3 class="concept-title">2. Beeswarm Plot — Direction + Distribution</h3>
    <div class="concept-body">
      <p><strong>What it shows:</strong> Every sample as a dot. X-axis = SHAP value. Color = feature value (red=high, blue=low). Features ranked by importance (top = most impactful).</p>
      <p><strong>How to read it:</strong></p>
      <ul style="margin:6px 0 10px 18px;line-height:1.8;">
        <li>Dot to the RIGHT = this feature pushed prediction UP for this sample</li>
        <li>Dot to the LEFT = this feature pushed prediction DOWN</li>
        <li>Red dots on right = high feature value increases prediction (positive relationship)</li>
        <li>Red dots on left = high feature value DECREASES prediction (negative relationship)</li>
        <li>Wide spread = feature has variable impact (non-linear or interaction effects)</li>
      </ul>
      <div class="code-block"><pre>import shap                          # SHAP library
import xgboost as xgb                # gradient boosted tree model
import numpy as np                   # array operations

# (continuing from Bar Plot example above)

# --- Beeswarm plot ---
shap.plots.beeswarm(shap_values)
# Each row = one feature (ranked by mean |SHAP|)
# Each dot = one test sample
# X-axis = SHAP value (positive = pushed prediction up)
# Color = feature value (red = high, blue = low)

# --- Beeswarm with feature names for readability ---
import pandas as pd                  # wrap data with feature names
X_test_df = pd.DataFrame(X_test, columns=data.feature_names)  # named columns
shap_values_named = explainer(X_test_df)  # recompute with named features
shap.plots.beeswarm(shap_values_named)    # now shows feature names on Y-axis

# --- Limit to top 15 features ---
shap.plots.beeswarm(shap_values_named, max_display=15)  # show only top 15</pre></div>
      <div class="alert-box info-box" style="margin:10px 0 0;">
        <strong>Classic interview answer:</strong> "Beeswarm is my go-to plot — it combines global importance (Y-axis ranking) with direction (X-axis sign) and feature value context (color) in one view. It tells me both WHAT matters and HOW it matters."
      </div>
    </div>
  </div>

  <!-- Waterfall Plot -->
  <div class="concept-card">
    <h3 class="concept-title">3. Waterfall Plot — Explain One Prediction</h3>
    <div class="concept-body">
      <p><strong>What it shows:</strong> For a SINGLE row, how each feature pushed the prediction from the base value (average prediction) to the final output. Each bar is additive.</p>
      <p><strong>When to use:</strong> Regulatory explanations, customer-facing decisions, debugging a specific wrong prediction.</p>
      <div class="code-block"><pre>import shap                          # SHAP library

# (continuing from above — shap_values already computed)

# --- Waterfall for sample index 0 ---
shap.plots.waterfall(shap_values[0])
# Bottom = base value (E[f(X)] = avg prediction on training data)
# Each bar = one feature's contribution (red=pushes up, blue=pushes down)
# Top = final model output for this row
# Features sorted by |SHAP value| (biggest contributors shown first)

# --- Explain the prediction in plain English ---
sample_idx = 5                       # pick any row to explain
sv = shap_values[sample_idx]         # SHAP object for this row

base   = sv.base_values              # model's average prediction
output = sv.base_values + sv.values.sum()  # actual prediction for this row
top3   = sorted(zip(data.feature_names, sv.values),
                key=lambda x: abs(x[1]), reverse=True)[:3]  # top 3 drivers

print(f"Base value: {base:.3f}")     # e.g., 0.62
print(f"Prediction: {output:.3f}")   # e.g., 0.91
print("Top 3 drivers:")
for feat, val in top3:               # print each feature and its contribution
    direction = "increased" if val > 0 else "decreased"  # direction of impact
    print(f"  {feat}: {direction} prediction by {abs(val):.3f}")</pre></div>
    </div>
  </div>

  <!-- Force Plot -->
  <div class="concept-card">
    <h3 class="concept-title">4. Force Plot — Horizontal Waterfall (Stackable)</h3>
    <div class="concept-body">
      <p><strong>What it shows:</strong> Same information as waterfall but horizontal. Red features push prediction right (higher), blue push left (lower). Can be stacked for ALL samples into an interactive HTML visualization.</p>
      <div class="code-block"><pre>import shap                          # SHAP library
import matplotlib.pyplot as plt      # needed for static rendering

# --- Single prediction force plot ---
shap.initjs()                        # initialise JavaScript for interactive plot

# Interactive force plot (works in Jupyter notebooks)
shap.plots.force(shap_values[0])
# Same as waterfall but horizontal layout — easier to share in slides

# --- Static version (for non-Jupyter environments) ---
shap.plots.force(shap_values[0], matplotlib=True)  # renders as matplotlib figure
plt.tight_layout()
plt.savefig("force_plot.png", dpi=150, bbox_inches="tight")  # save to file

# --- Stack ALL samples (most powerful use case) ---
shap.plots.force(shap_values)
# Creates a scrollable interactive HTML chart
# Each row = one sample, sorted by prediction value
# Reveals natural clusters — groups of similar explanations
# Export to HTML for sharing with stakeholders:
shap.save_html("all_predictions.html", shap.plots.force(shap_values))</pre></div>
      <div class="alert-box info-box" style="margin:10px 0 0;">
        <strong>Pro tip:</strong> Stacked force plot for all samples is excellent for finding segments — e.g., "these 200 churned customers were all driven by high support_calls, while these 150 were driven by low tenure."
      </div>
    </div>
  </div>

  <!-- Scatter / Dependence Plot -->
  <div class="concept-card">
    <h3 class="concept-title">5. Scatter Plot (Dependence Plot) — Feature Deep Dive</h3>
    <div class="concept-body">
      <p><strong>What it shows:</strong> For one feature: X = raw feature value, Y = SHAP value. The shape of the curve reveals the relationship the model learned.</p>
      <p><strong>What you can spot:</strong></p>
      <ul style="margin:6px 0 10px 18px;line-height:1.8;">
        <li><strong>Linear:</strong> straight line — model learned a proportional relationship</li>
        <li><strong>Step function:</strong> flat then jump — model found a threshold</li>
        <li><strong>Diminishing returns:</strong> curve flattens — impact saturates after a point</li>
        <li><strong>Interaction:</strong> dots scatter widely at the same X value — another feature is modifying the effect (color = interaction feature)</li>
      </ul>
      <div class="code-block"><pre>import shap                          # SHAP library
import pandas as pd                  # feature names for readability

# (continuing — shap_values_named computed with feature names)

# --- Scatter for one feature ---
shap.plots.scatter(shap_values_named[:, "mean radius"])
# X-axis = raw value of "mean radius"
# Y-axis = SHAP value (impact on prediction)
# Color = auto-selected interaction feature with highest correlation

# --- Manually choose interaction color feature ---
shap.plots.scatter(shap_values_named[:, "mean radius"],
                   color=shap_values_named[:, "mean texture"])
# Now color = SHAP value of mean_texture
# If red dots (high texture) cluster at top of a band → interaction effect

# --- Loop over top features ---
top_features = pd.Series(
    shap_values_named.values.mean(axis=0),  # mean SHAP per feature
    index=data.feature_names
).abs().nlargest(5).index  # top 5 feature names

for feat in top_features:            # plot scatter for each top feature
    shap.plots.scatter(shap_values_named[:, feat])  # separate plot per feature</pre></div>
    </div>
  </div>

  <!-- Heatmap Plot -->
  <div class="concept-card">
    <h3 class="concept-title">6. Heatmap — All Features × All Samples</h3>
    <div class="concept-body">
      <p><strong>What it shows:</strong> Grid where rows = features, columns = samples. Color = SHAP value magnitude. Samples are clustered by similar explanation patterns.</p>
      <p><strong>When to use:</strong> Spotting sample clusters that are explained differently, detecting outliers with unusual SHAP patterns, validating model consistency.</p>
      <div class="code-block"><pre>import shap                          # SHAP library

# (continuing — shap_values already computed)

# --- Heatmap ---
shap.plots.heatmap(shap_values)
# Rows = features (sorted by importance)
# Columns = test samples (clustered by similar SHAP patterns)
# Color = SHAP value (red = large positive, blue = large negative)
# Top bar = model output per sample

# --- Heatmap for a subset (faster for large datasets) ---
shap.plots.heatmap(shap_values[:200])   # show only first 200 samples

# What to look for:
# Vertical red/blue bands = a group of samples dominated by one feature
# Horizontal bands = a feature with consistent impact across all samples
# Diagonal patterns = interactions between features
# Isolated dots = outlier rows with unusual SHAP values (worth investigating)</pre></div>
    </div>
  </div>

  <!-- Choosing the Right Plot -->
  <div class="concept-card">
    <h3 class="concept-title">Choosing the Right SHAP Plot — Decision Guide</h3>
    <div class="concept-body">
      <table class="data-table">
        <thead><tr><th>Situation</th><th>Use this plot</th><th>Why</th></tr></thead>
        <tbody>
          <tr><td>Stakeholder asks "what drives predictions?"</td><td>Beeswarm</td><td>Shows importance + direction + distribution</td></tr>
          <tr><td>Slide deck needs simple feature ranking</td><td>Bar</td><td>Clean, easy to read, no jargon</td></tr>
          <tr><td>Explain ONE rejected loan / flagged transaction</td><td>Waterfall</td><td>Shows exact per-feature contribution for that row</td></tr>
          <tr><td>Interactive dashboard / Jupyter notebook</td><td>Force (stacked)</td><td>Interactive, shows all samples, reveals clusters</td></tr>
          <tr><td>Feature engineering — understand non-linearity</td><td>Scatter</td><td>Shows raw value vs. SHAP impact curve</td></tr>
          <tr><td>Find sample clusters with different explanations</td><td>Heatmap</td><td>Full feature × sample view with clustering</td></tr>
          <tr><td>Bias audit on protected attribute</td><td>Scatter (colored by protected attr)</td><td>See if protected feature systematically drives SHAP</td></tr>
        </tbody>
      </table>

      <div class="code-block"><pre>import shap                          # SHAP library
import matplotlib.pyplot as plt      # for saving figures

# --- Complete workflow: 4 plots in one analysis ---
explainer    = shap.Explainer(model)       # create explainer (auto-detects algorithm)
shap_values  = explainer(X_test)          # compute SHAP values for test set

# 1. Global importance (quick summary)
shap.plots.bar(shap_values, max_display=10)     # top 10 features by mean |SHAP|

# 2. Global importance with direction (main slide)
shap.plots.beeswarm(shap_values, max_display=10)  # distribution + direction

# 3. Explain a specific wrong prediction
wrong_idx = (model.predict(X_test) != y_test).nonzero()[0][0]  # first wrong prediction
shap.plots.waterfall(shap_values[wrong_idx])      # debug why this one was wrong

# 4. Understand most important feature's relationship
top_feat_idx = shap_values.abs.mean(0).values.argmax()  # index of most important feature
shap.plots.scatter(shap_values[:, top_feat_idx])         # how value affects impact</pre></div>
    </div>
  </div>

'''

# Inject before closing </div> <!-- end Phase 53 -->
target = '</div>\n<!-- end Phase 53 -->'
if target in html:
    html = html.replace(target, shap_content + target, 1)
    print("SHAP plots content injected into p53")
else:
    print("MISS: p53 closing tag not found")

# ============================================================
# 2. SMOTE DEEP DIVE -- inject into p31 after existing SMOTE block
# ============================================================

smote_content = '''
  <h3>SMOTE Deep Dive — Why, When, and How</h3>
  <div class="code-block"><pre>import numpy as np                   # array operations and visualization data
import pandas as pd                  # check class distribution before/after
import matplotlib.pyplot as plt      # visualize original vs. synthetic samples
from imblearn.over_sampling import (
    SMOTE,          # Synthetic Minority Over-sampling TEchnique (standard)
    ADASYN,         # Adaptive Synthetic Sampling (focuses on hard samples)
    BorderlineSMOTE,# only synthesizes near the decision boundary (often better)
    SVMSMOTE        # uses SVM support vectors to guide synthesis
)
from imblearn.under_sampling import RandomUnderSampler  # reduce majority class
from imblearn.pipeline import Pipeline as ImbPipeline   # chain resampling + model
from sklearn.datasets import make_classification        # generate synthetic dataset
from sklearn.ensemble import RandomForestClassifier     # model to test on balanced data
from sklearn.model_selection import StratifiedKFold, cross_val_score  # stratified CV
from sklearn.metrics import classification_report, roc_auc_score       # evaluation

# ============================================================
# WHAT IS SMOTE?
# ============================================================
# SMOTE creates NEW synthetic minority samples -- not copies of existing ones.
# Algorithm:
#   1. Pick a minority sample (the "seed")
#   2. Find its k nearest neighbors (also minority samples)
#   3. Draw a random point on the LINE between seed and one of those neighbors
#   4. That random point becomes a new synthetic sample
#
# Result: minority class gets populated with plausible new examples
# that fill the feature space between existing minority samples.

# ============================================================
# WHY USE SMOTE? (The Problem It Solves)
# ============================================================
# Class imbalance breaks standard ML training because:
#   - Model learns to predict "majority class always" → 99% accuracy but 0% recall on minority
#   - Loss function penalizes majority errors more (there are more majority samples)
#   - Decision boundary shifts away from minority class
#
# Real examples of class imbalance:
#   - Fraud detection:     fraud = 0.1% of transactions
#   - Medical diagnosis:   disease = 1-5% of patients
#   - Churn prediction:    churners = 3-8% of users
#   - Loan default:        defaults = 2-10% of loans
#   - Anomaly detection:   anomalies = <1% of data

# ============================================================
# WHEN TO USE SMOTE (Decision Rules)
# ============================================================
# USE SMOTE when:
#   - Minority class < 10-20% of data AND you need high minority recall
#   - You tried class_weight="balanced" first but recall is still too low
#   - You have enough minority samples to synthesize from (rule of thumb: >50)
#   - Features are continuous (or mixed continuous/categorical)
#
# DO NOT USE SMOTE when:
#   - Minority class is already >30% (not enough imbalance to warrant it)
#   - You have very few minority samples (<20) -- too little to synthesize from
#   - Features are purely categorical (SMOTE interpolates -- meaningless for categories)
#   - You are doing time series (SMOTE ignores temporal order)
#   - Minority samples cluster in a tiny region (SMOTE will create samples in wrong areas)
#
# ALWAYS apply SMOTE ONLY on training data, NEVER on test data
# (otherwise you're evaluating on synthetic samples, which inflates metrics)

# ============================================================
# STEP-BY-STEP EXAMPLE
# ============================================================
X, y = make_classification(
    n_samples=10000,        # 10,000 total samples
    n_features=20,          # 20 features
    weights=[0.95, 0.05],   # 95% majority, 5% minority (severe imbalance)
    random_state=42
)

print("Before SMOTE:")
unique, counts = np.unique(y, return_counts=True)  # count each class
for u, c in zip(unique, counts):
    print(f"  Class {u}: {c} samples ({c/len(y)*100:.1f}%)")

# Apply SMOTE
smote = SMOTE(
    sampling_strategy=0.3,  # after SMOTE, minority will be 30% of majority count
    k_neighbors=5,           # use 5 nearest minority neighbors (default)
    random_state=42
)
X_resampled, y_resampled = smote.fit_resample(X, y)  # create synthetic samples

print("\nAfter SMOTE:")
unique, counts = np.unique(y_resampled, return_counts=True)
for u, c in zip(unique, counts):
    print(f"  Class {u}: {c} samples ({c/len(y_resampled)*100:.1f}%)")
# Before: Class 0: 9500, Class 1: 500
# After:  Class 0: 9500, Class 1: 2850 (30% of 9500)</pre></div>

  <div class="code-block"><pre>import numpy as np                   # array and math operations
import pandas as pd                  # display comparison results
from imblearn.over_sampling import SMOTE, BorderlineSMOTE, SVMSMOTE  # SMOTE variants
from imblearn.pipeline import Pipeline as ImbPipeline   # safe resampling inside CV
from sklearn.ensemble import RandomForestClassifier     # model to compare
from sklearn.model_selection import StratifiedKFold     # preserve class ratio in folds
from sklearn.metrics import roc_auc_score, recall_score # key metrics for imbalanced data
from sklearn.model_selection import train_test_split    # hold out test set

# ============================================================
# SMOTE VARIANTS -- when to use which
# ============================================================

# SMOTE: standard -- synthesizes everywhere in minority feature space
smote = SMOTE(sampling_strategy="minority", k_neighbors=5, random_state=42)
# Best for: general imbalance, moderate overlap between classes

# BorderlineSMOTE: only synthesizes near the decision boundary
borderline = BorderlineSMOTE(kind="borderline-1", random_state=42)
# Best for: when standard SMOTE creates too many easy/redundant samples
# "borderline-1": synthesizes between minority borderline samples and their neighbors
# "borderline-2": also synthesizes toward majority samples (riskier but aggressive)

# SVMSMOTE: uses SVM support vectors to find hard-to-classify minority samples
svmsmote = SVMSMOTE(random_state=42)
# Best for: highly imbalanced data with complex decision boundary
# Slower than standard SMOTE (trains an SVM internally)

# ADASYN: gives more weight to minority samples that are harder to learn
from imblearn.over_sampling import ADASYN  # Adaptive Synthetic Sampling
adasyn = ADASYN(sampling_strategy=0.5, random_state=42)
# Best for: when some minority regions are more important than others

# ============================================================
# CORRECT WAY: use SMOTE inside a pipeline to prevent data leakage
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42  # stratify preserves class ratio
)

# WRONG way (data leakage):
# X_res, y_res = smote.fit_resample(X, y)  # never apply to full dataset!
# model.fit(X_res, y_res)                  # test set contains synthetic variants of train

# CORRECT way: pipeline applies SMOTE only inside each CV fold
pipeline = ImbPipeline([
    ("smote",  SMOTE(sampling_strategy=0.3, random_state=42)),  # resample train fold only
    ("model",  RandomForestClassifier(n_estimators=100, random_state=42))  # then train model
])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)  # preserve class ratio
# Use roc_auc for imbalanced data -- NOT accuracy
scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="roc_auc")
print(f"ROC-AUC: {scores.mean():.3f} +/- {scores.std():.3f}")

# Final evaluation on held-out test set (NO SMOTE on test)
pipeline.fit(X_train, y_train)       # fit pipeline on full training set
y_pred  = pipeline.predict(X_test)   # predict on original (not resampled) test set
y_proba = pipeline.predict_proba(X_test)[:, 1]  # probability of minority class

print(f"Test ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}")
print(f"Minority Recall: {recall_score(y_test, y_pred):.3f}")  # did we catch the rare cases?</pre></div>

  <div class="code-block"><pre>import numpy as np                   # array operations
import pandas as pd                  # organize strategy comparison results
from sklearn.ensemble import RandomForestClassifier     # consistent model for comparison
from sklearn.model_selection import train_test_split, StratifiedKFold  # evaluation setup
from sklearn.metrics import classification_report, roc_auc_score, f1_score  # metrics
from imblearn.over_sampling import SMOTE                # standard oversampling
from imblearn.under_sampling import RandomUnderSampler  # undersampling
from imblearn.pipeline import Pipeline as ImbPipeline  # safe pipeline with resampling

# ============================================================
# STRATEGY COMPARISON: which approach works best?
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

base_model = RandomForestClassifier(n_estimators=100, random_state=42)  # same model throughout

strategies = {
    "No resampling":
        base_model,

    "class_weight=balanced":
        RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42),

    "SMOTE only":
        ImbPipeline([("smote", SMOTE(0.3, random_state=42)),
                     ("model", RandomForestClassifier(n_estimators=100, random_state=42))]),

    "Undersample majority":
        ImbPipeline([("under", RandomUnderSampler(sampling_strategy=0.5, random_state=42)),
                     ("model", RandomForestClassifier(n_estimators=100, random_state=42))]),

    "SMOTE + Undersample":
        ImbPipeline([("smote", SMOTE(sampling_strategy=0.3, random_state=42)),    # oversample minority to 30%
                     ("under", RandomUnderSampler(sampling_strategy=0.7, random_state=42)),  # undersample majority
                     ("model", RandomForestClassifier(n_estimators=100, random_state=42))]),
}

results = {}
for name, pipe in strategies.items():           # try each strategy
    pipe.fit(X_train, y_train)                  # train on training data
    y_proba = pipe.predict_proba(X_test)[:, 1]  # minority class probability
    y_pred  = pipe.predict(X_test)              # hard predictions
    results[name] = {
        "ROC-AUC":        round(roc_auc_score(y_test, y_proba), 3),
        "Minority Recall": round(__import__("sklearn.metrics", fromlist=["recall_score"]).recall_score(y_test, y_pred), 3),
        "Minority F1":    round(f1_score(y_test, y_pred), 3),
    }

print(pd.DataFrame(results).T.to_string())  # compare all strategies side by side
# Expected result: "SMOTE + Undersample" often best for ROC-AUC and recall
# "class_weight=balanced" is cheapest and often surprisingly competitive

# ============================================================
# RULE OF THUMB:
# 1. Start: class_weight="balanced" (zero cost, often 80% of the gain)
# 2. If recall still too low: add SMOTE (sampling_strategy=0.2 to 0.5)
# 3. Memory / speed constraint: add RandomUnderSampler after SMOTE
# 4. Complex boundary: try BorderlineSMOTE or SVMSMOTE
# 5. ALWAYS evaluate with ROC-AUC + Precision-Recall, NOT accuracy
# ============================================================</pre></div>
'''

# Find end of p31 -- inject before closing tag of p31 section
# p31 uses phase-section structure, find the closing </div> before p32
idx31 = html.find('id="p31"')
idx32 = html.find('id="p32"')
p31_seg = html[idx31:idx32]

# Find the last </div> before Phase 32 starts (the phase-section closing tag)
# Look for the comment that closes p31
close_tag = '\n\n<!-- ═══'
insert_pos = html.find(close_tag, idx31)
if insert_pos != -1 and insert_pos < idx32:
    html = html[:insert_pos] + '\n' + smote_content + html[insert_pos:]
    print("SMOTE deep dive injected into p31")
else:
    # fallback: find </div> right before p32
    fallback = html.rfind('</div>', idx31, idx32)
    if fallback != -1:
        html = html[:fallback] + smote_content + html[fallback:]
        print("SMOTE deep dive injected (fallback)")
    else:
        print("MISS: could not find p31 insertion point")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
