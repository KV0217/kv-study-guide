# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 30 — replace code blocks with per-line commented versions
# ─────────────────────────────────────────────────────────────────────────────

# Block 1: ROW_NUMBER vs RANK vs DENSE_RANK
html = html.replace(
    '''<div class="code-block"><pre>-- Scores: 100, 90, 90, 80
SELECT
  name,
  score,
  ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
  -- 1, 2, 3, 4  (always unique, no gaps, no ties)

  RANK()       OVER (ORDER BY score DESC) AS rnk,
  -- 1, 2, 2, 4  (ties get same rank, then gap — skips 3)

  DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rnk
  -- 1, 2, 2, 3  (ties get same rank, NO gap)
FROM scores;
</pre></div>''',
    '''<div class="code-block"><pre>-- Sample data: scores = 100, 90, 90, 80 (two rows tie at 90)
SELECT
  name,                                              -- employee name
  score,                                             -- raw test score
  ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num,
  -- row_num: 1,2,3,4 — ALWAYS unique, no ties, no gaps

  RANK()       OVER (ORDER BY score DESC) AS rnk,
  -- rnk: 1,2,2,4 — ties share the rank, then SKIPS to next (gap at 3)

  DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rnk
  -- dense_rnk: 1,2,2,3 — ties share rank, NO gap after tied rows
FROM scores;
-- Rule: use ROW_NUMBER for "top N per group" (guarantees exactly N rows)
-- Use DENSE_RANK when you want to keep all tied rows in top N
</pre></div>'''
)

# Block 2: Top N Per Group
html = html.replace(
    '''<div class="code-block"><pre>-- Top 2 selling products per category
WITH ranked AS (
  SELECT
    category,
    product,
    revenue,
    ROW_NUMBER() OVER (
      PARTITION BY category
      ORDER BY revenue DESC
    ) AS rn
  FROM sales
)
SELECT category, product, revenue
FROM ranked
WHERE rn <= 2;
-- This is asked in almost every DA interview
</pre></div>''',
    '''<div class="code-block"><pre>-- Classic interview pattern: Top 2 selling products per category
WITH ranked AS (               -- CTE to first assign row numbers
  SELECT
    category,                  -- partition column — separate window per category
    product,                   -- the value we want to rank
    revenue,                   -- the metric we rank by
    ROW_NUMBER() OVER (
      PARTITION BY category    -- reset counter for every new category
      ORDER BY revenue DESC    -- rank highest revenue as 1
    ) AS rn                    -- rn=1 → top seller, rn=2 → 2nd seller
  FROM sales
)
SELECT category, product, revenue   -- final output: only top 2 per category
FROM ranked
WHERE rn &lt;= 2;                      -- filter AFTER window function runs (not WHERE inside CTE)
-- NOTE: cannot use WHERE rn &lt;= 2 inside the CTE — window fn runs after WHERE
</pre></div>'''
)

# Block 3: LAG / LEAD
html = html.replace(
    '''<div class="code-block"><pre>-- Month-over-month growth
SELECT
  month,
  revenue,
  LAG(revenue, 1) OVER (ORDER BY month)        AS prev_month_revenue,
  revenue - LAG(revenue, 1) OVER (ORDER BY month) AS mom_change,
  ROUND(
    100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY month))
    / LAG(revenue, 1) OVER (ORDER BY month), 2
  )                                              AS mom_pct_change
FROM monthly_revenue;

-- LAG(col, n, default) — n rows behind, default if null
-- LEAD(col, n, default) — n rows ahead
</pre></div>''',
    '''<div class="code-block"><pre>-- Month-over-month revenue growth using LAG
SELECT
  month,                                          -- the current month
  revenue,                                        -- current month revenue
  LAG(revenue, 1) OVER (ORDER BY month)  AS prev_month_revenue,
  -- LAG(col, 1): look 1 row back (previous month); returns NULL for first row

  revenue - LAG(revenue, 1) OVER (ORDER BY month) AS mom_change,
  -- absolute change: current - previous; positive = growth

  ROUND(
    100.0 * (revenue - LAG(revenue, 1) OVER (ORDER BY month))
    / LAG(revenue, 1) OVER (ORDER BY month), 2   -- percentage change
  )                                              AS mom_pct_change
  -- multiply by 100.0 (not 100) to force float division, not integer
FROM monthly_revenue;
-- LAG(col, n, default) — go n rows BACKWARD; use default when no prior row exists
-- LEAD(col, n, default) — go n rows FORWARD; for lookahead calculations
</pre></div>'''
)

# Block 4: Running totals / Moving averages
html = html.replace(
    '''<div class="code-block"><pre>-- Running total (cumulative sum)
SELECT
  date,
  daily_sales,
  SUM(daily_sales) OVER (ORDER BY date)          AS running_total,

  -- 7-day moving average
  AVG(daily_sales) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW     -- frame clause
  )                                              AS ma_7day,

  -- Rolling 30-day max
  MAX(daily_sales) OVER (
    ORDER BY date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
  )                                              AS rolling_30d_max
FROM daily_sales;
</pre></div>''',
    '''<div class="code-block"><pre>-- Running total and moving averages using window frame clauses
SELECT
  date,                                           -- the date of each row
  daily_sales,                                    -- sales for that day only

  SUM(daily_sales) OVER (ORDER BY date) AS running_total,
  -- default frame: RANGE UNBOUNDED PRECEDING → CURRENT ROW
  -- adds all rows from start up to current date (cumulative sum)

  AVG(daily_sales) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW     -- ROWS = physical row count
  ) AS ma_7day,
  -- 7-day rolling average: this row + 6 rows before it (7 total)
  -- ROWS is preferred over RANGE for time-based windows (handles duplicate dates)

  MAX(daily_sales) OVER (
    ORDER BY date
    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW    -- 30-day rolling window
  ) AS rolling_30d_max                           -- highest daily sales in last 30 days
FROM daily_sales;
-- Frame options: UNBOUNDED PRECEDING, N PRECEDING, CURRENT ROW, N FOLLOWING, UNBOUNDED FOLLOWING
</pre></div>'''
)

# Block 5: NTILE
html = html.replace(
    '''<div class="code-block"><pre>-- Split customers into 4 quartiles by spend
SELECT
  customer_id,
  total_spend,
  NTILE(4) OVER (ORDER BY total_spend DESC) AS spend_quartile,
  -- 1 = top 25%, 4 = bottom 25%

  NTILE(100) OVER (ORDER BY total_spend DESC) AS spend_percentile
  -- percentile rank
FROM customers;
</pre></div>''',
    '''<div class="code-block"><pre>-- NTILE: divide rows into equal-sized buckets
SELECT
  customer_id,                                       -- unique customer
  total_spend,                                       -- total amount spent
  NTILE(4) OVER (ORDER BY total_spend DESC) AS spend_quartile,
  -- splits customers into 4 equal groups by spend
  -- 1 = top 25% spenders (highest), 4 = bottom 25% (lowest)
  -- if rows don't divide evenly, earlier buckets get the extra row

  NTILE(100) OVER (ORDER BY total_spend DESC) AS spend_percentile
  -- percentile rank: 1 = top 1%, 100 = bottom 1%
  -- use NTILE(10) for deciles, NTILE(4) for quartiles
FROM customers;
</pre></div>'''
)

# Block 6: FIRST_VALUE / LAST_VALUE
html = html.replace(
    '''<div class="code-block"><pre>-- Compare each sale to the first and last sale in that region
SELECT
  region,
  sale_date,
  amount,
  FIRST_VALUE(amount) OVER (
    PARTITION BY region ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS first_sale,
  LAST_VALUE(amount) OVER (
    PARTITION BY region ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    -- IMPORTANT: must specify full frame for LAST_VALUE
  ) AS last_sale
FROM sales;
</pre></div>''',
    '''<div class="code-block"><pre>-- FIRST_VALUE and LAST_VALUE: compare each row to first/last in its partition
SELECT
  region,                                        -- partition: separate window per region
  sale_date,                                     -- the date of this sale
  amount,                                        -- this sale's amount
  FIRST_VALUE(amount) OVER (
    PARTITION BY region ORDER BY sale_date       -- order: oldest sale first
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- see full partition
  ) AS first_sale,                               -- amount of the very first sale in this region

  LAST_VALUE(amount) OVER (
    PARTITION BY region ORDER BY sale_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    -- CRITICAL: without this full frame, LAST_VALUE default frame stops at CURRENT ROW
    -- that would give the current row's value, not the actual last row — common bug!
  ) AS last_sale                                 -- amount of the most recent sale in this region
FROM sales;
</pre></div>'''
)

# Block 7: Consecutive Days Streak
html = html.replace(
    '''<div class="code-block"><pre>-- Find users with 3+ consecutive login days
WITH numbered AS (
  SELECT
    user_id,
    login_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) AS rn
  FROM logins
),
grouped AS (
  SELECT
    user_id,
    login_date,
    -- If consecutive, date - rn is constant (the "island" trick)
    DATE_SUB(login_date, INTERVAL rn DAY) AS grp
  FROM numbered
)
SELECT user_id, MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*) AS streak_length
FROM grouped
GROUP BY user_id, grp
HAVING COUNT(*) >= 3
ORDER BY streak_length DESC;
</pre></div>''',
    '''<div class="code-block"><pre>-- Classic "Gaps and Islands" problem: find users with 3+ consecutive login days
WITH numbered AS (
  SELECT
    user_id,                                           -- group streaks per user
    login_date,                                        -- the date they logged in
    ROW_NUMBER() OVER (
      PARTITION BY user_id                             -- row number resets per user
      ORDER BY login_date                              -- number dates in chronological order
    ) AS rn                                            -- rn: 1,2,3,4... per user
  FROM logins
),
grouped AS (
  SELECT
    user_id,
    login_date,
    DATE_SUB(login_date, INTERVAL rn DAY) AS grp
    -- KEY TRICK: if dates are consecutive, (date - row_number) is CONSTANT
    -- e.g., Jan 3 - 1 = Jan 2, Jan 4 - 2 = Jan 2, Jan 5 - 3 = Jan 2 → same grp
    -- a gap breaks the streak → grp value changes
  FROM numbered
)
SELECT
  user_id,
  MIN(login_date) AS streak_start,   -- first day of this streak
  MAX(login_date) AS streak_end,     -- last day of this streak
  COUNT(*)        AS streak_length   -- how many days in the streak
FROM grouped
GROUP BY user_id, grp                -- each unique grp = one contiguous streak
HAVING COUNT(*) &gt;= 3                -- only keep streaks of 3+ days
ORDER BY streak_length DESC;         -- longest streaks first
</pre></div>'''
)

# Block 8: WINDOW alias
html = html.replace(
    '''<div class="code-block"><pre>SELECT
  dept,
  salary,
  AVG(salary)    OVER w AS dept_avg,
  MAX(salary)    OVER w AS dept_max,
  RANK()         OVER w AS dept_rank
FROM employees
WINDOW w AS (PARTITION BY dept ORDER BY salary DESC);
-- Define once, reuse — keeps SQL clean
</pre></div>''',
    '''<div class="code-block"><pre>-- WINDOW alias: define the OVER clause once, reuse many times
SELECT
  dept,                                  -- department column
  salary,                                -- individual salary
  AVG(salary) OVER w AS dept_avg,        -- average salary in this dept
  MAX(salary) OVER w AS dept_max,        -- highest salary in this dept
  RANK()      OVER w AS dept_rank        -- rank within department (1=highest)
FROM employees
WINDOW w AS (PARTITION BY dept ORDER BY salary DESC);
-- WINDOW w defines: same partition + order used by all 3 functions above
-- Alternative without alias: must repeat OVER(PARTITION BY dept ORDER BY salary DESC) 3 times
-- Supported in: PostgreSQL, MySQL 8+, BigQuery (not in older SQL Server)
</pre></div>'''
)

print("p30 done")

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 31 — Feature Engineering code blocks
# ─────────────────────────────────────────────────────────────────────────────

html = html.replace(
    '''<div class="code-block"><pre>import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

df = pd.read_csv("data.csv")

# --- Step 1: understand missingness pattern
print(df.isnull().sum() / len(df) * 100)  # % missing per column

# --- Strategy depends on WHY data is missing ---

# MCAR (Missing Completely At Random) — safe to drop or impute with mean/median
df["age"].fillna(df["age"].median(), inplace=True)

# MAR (Missing At Random) — impute using other columns
imputer = KNNImputer(n_neighbors=5)
df[["age", "income", "score"]] = imputer.fit_transform(df[["age", "income", "score"]])

# MNAR (Missing Not At Random) — missingness itself is signal
df["income_missing"] = df["income"].isnull().astype(int)  # flag before filling
df["income"].fillna(df["income"].median(), inplace=True)

# Categorical: most common or "Unknown" bucket
df["city"].fillna(df["city"].mode()[0], inplace=True)
df["city"].fillna("Unknown", inplace=True)
</pre></div>''',
    '''<div class="code-block"><pre>import pandas as pd                              # data manipulation library
import numpy as np                               # numerical computing
from sklearn.impute import SimpleImputer, KNNImputer  # imputation tools

df = pd.read_csv("data.csv")                     # load dataset

# Step 1: audit how much data is missing per column
print(df.isnull().sum() / len(df) * 100)         # shows % missing: e.g., age: 12.3%

# ── Strategy depends on WHY data is missing ───────────────────────────────────

# MCAR (Missing Completely At Random): no pattern — safe to impute with simple stats
df["age"].fillna(df["age"].median(), inplace=True)
# median is preferred over mean — more robust to outliers in age distribution

# MAR (Missing At Random): missing depends on OTHER observed columns
imputer = KNNImputer(n_neighbors=5)              # find 5 most similar complete rows
df[["age", "income", "score"]] = imputer.fit_transform(df[["age", "income", "score"]])
# KNN imputer fills each missing cell using the average of 5 nearest neighbours

# MNAR (Missing Not At Random): missingness IS information — e.g., "declined to answer"
df["income_missing"] = df["income"].isnull().astype(int)  # 1=was missing, 0=was present
df["income"].fillna(df["income"].median(), inplace=True)  # then fill numerically

# Categorical missing values
df["city"].fillna(df["city"].mode()[0], inplace=True)  # mode = most frequent category
df["city"].fillna("Unknown", inplace=True)             # or create explicit "Unknown" bucket
</pre></div>'''
)

html = html.replace(
    '''<div class="code-block"><pre>import scipy.stats as stats

# --- Method 1: IQR (robust, works on skewed data)
Q1 = df["salary"].quantile(0.25)
Q3 = df["salary"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# Remove outliers
df_clean = df[(df["salary"] >= lower) & (df["salary"] <= upper)]

# Cap outliers (winsorization — preferred for ML)
df["salary_capped"] = df["salary"].clip(lower, upper)

# --- Method 2: Z-score (works when data is roughly normal)
z_scores = np.abs(stats.zscore(df["salary"]))
df_clean = df[z_scores < 3]  # keep rows within 3 standard deviations

# --- Method 3: Isolation Forest (for multivariate outliers)
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.05, random_state=42)
df["outlier"] = iso.fit_predict(df[["salary", "age", "score"]])
df_clean = df[df["outlier"] == 1]
</pre></div>''',
    '''<div class="code-block"><pre>import scipy.stats as stats                       # statistical functions

# ── Method 1: IQR — best for skewed data like salary, price ──────────────────
Q1 = df["salary"].quantile(0.25)                  # 25th percentile (lower hinge)
Q3 = df["salary"].quantile(0.75)                  # 75th percentile (upper hinge)
IQR = Q3 - Q1                                     # interquartile range = middle 50% spread

lower = Q1 - 1.5 * IQR                            # anything below this is an outlier
upper = Q3 + 1.5 * IQR                            # anything above this is an outlier
# 1.5 * IQR is the standard Tukey fence; use 3.0 * IQR for "extreme" outliers only

# Option A: drop outlier rows entirely
df_clean = df[(df["salary"] >= lower) & (df["salary"] <= upper)]

# Option B: winsorize / cap — PREFERRED for ML (no data loss)
df["salary_capped"] = df["salary"].clip(lower, upper)  # clips to [lower, upper] bounds

# ── Method 2: Z-score — best for normally distributed data ───────────────────
z_scores = np.abs(stats.zscore(df["salary"]))     # standardised distance from mean
df_clean = df[z_scores < 3]                       # keep rows within 3 std deviations (~99.7%)

# ── Method 3: Isolation Forest — finds multivariate outliers ─────────────────
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.05,          # expect 5% of data to be outliers
                      random_state=42)
df["outlier"] = iso.fit_predict(df[["salary", "age", "score"]])
# returns: 1 = normal point, -1 = outlier
df_clean = df[df["outlier"] == 1]                 # keep only normal rows
</pre></div>'''
)

html = html.replace(
    '''<div class="code-block"><pre>import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import category_encoders as ce

# Label Encoding (ordinal)
le = LabelEncoder()
df["size_encoded"] = le.fit_transform(df["size"])  # S=0, M=1, L=2

# One-Hot Encoding
df = pd.get_dummies(df, columns=["color"], drop_first=True)
# drop_first avoids multicollinearity (dummy variable trap)

# Target Encoding (use category_encoders)
encoder = ce.TargetEncoder(cols=["city"], smoothing=10)
# smoothing blends global mean to prevent overfitting on rare categories
df["city_encoded"] = encoder.fit_transform(df["city"], df["target"])

# IMPORTANT: fit on train, transform on test — no leakage!
encoder.fit(X_train["city"], y_train)
X_train["city_enc"] = encoder.transform(X_train["city"])
X_test["city_enc"]  = encoder.transform(X_test["city"])

# Frequency Encoding (no target needed)
freq_map = df["city"].value_counts(normalize=True)
df["city_freq"] = df["city"].map(freq_map)
</pre></div>''',
    '''<div class="code-block"><pre>import pandas as pd                               # data manipulation
from sklearn.preprocessing import LabelEncoder   # for ordinal encoding
import category_encoders as ce                   # pip install category_encoders

# ── Label Encoding — only for ORDINAL categories (order matters) ──────────────
le = LabelEncoder()
df["size_encoded"] = le.fit_transform(df["size"])  # S=0, M=1, L=2 — implies S&lt;M&lt;L
# WARNING: never use label encoding for nominal data (city, color) — model sees fake order

# ── One-Hot Encoding — for NOMINAL categories with low cardinality (&lt;15 values) ──
df = pd.get_dummies(df, columns=["color"], drop_first=True)
# drop_first=True: removes first dummy column to avoid perfect multicollinearity
# e.g., if color has 3 values (red/blue/green): creates 2 columns (is_blue, is_green)

# ── Target Encoding — for HIGH cardinality nominal (city, product_id) ────────
encoder = ce.TargetEncoder(cols=["city"], smoothing=10)
# smoothing=10: blends category mean with global mean (prevents overfitting on rare cities)
# higher smoothing = more shrinkage toward global mean = less risk of leakage
df["city_encoded"] = encoder.fit_transform(df["city"], df["target"])

# CRITICAL RULE: always fit on train, transform on both — no target leakage!
encoder.fit(X_train["city"], y_train)             # learn encodings from train only
X_train["city_enc"] = encoder.transform(X_train["city"])  # apply to train
X_test["city_enc"]  = encoder.transform(X_test["city"])   # apply same mapping to test

# ── Frequency Encoding — replace category with how often it appears ───────────
freq_map = df["city"].value_counts(normalize=True)  # proportion of rows per city
df["city_freq"] = df["city"].map(freq_map)           # e.g., "Mumbai" → 0.23
</pre></div>'''
)

html = html.replace(
    '''<div class="code-block"><pre>from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import PowerTransformer, QuantileTransformer
import numpy as np

# StandardScaler (mean=0, std=1) — use with SVM, logistic regression, neural nets
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[num_cols])
X_test_scaled  = scaler.transform(X_test[num_cols])  # use same params!

# MinMaxScaler (range [0,1]) — use when you need bounded output (neural nets)
mm = MinMaxScaler()
X_scaled = mm.fit_transform(X[num_cols])

# RobustScaler (uses median/IQR) — best when outliers exist
rs = RobustScaler()
X_scaled = rs.fit_transform(X[num_cols])

# Log transform — fix right-skewed distributions (salary, price, counts)
df["log_income"] = np.log1p(df["income"])  # log1p handles zeros: log(1+x)

# Box-Cox / Yeo-Johnson — make any distribution more normal
pt = PowerTransformer(method="yeo-johnson")  # handles negatives unlike Box-Cox
df["income_normal"] = pt.fit_transform(df[["income"]])

# When to use which:
# Tree models (RF, XGBoost) — NO scaling needed (splits don't care about scale)
# Linear/logistic/SVM — StandardScaler
# KNN, PCA — StandardScaler or MinMaxScaler
# Neural nets — MinMaxScaler or StandardScaler
# Outliers present — RobustScaler
# Skewed data for linear model — log transform or PowerTransformer
</pre></div>''',
    '''<div class="code-block"><pre>from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.preprocessing import PowerTransformer  # for skewness correction
import numpy as np

# ── StandardScaler: z = (x - mean) / std → mean=0, std=1 ────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[num_cols])  # fit+transform on train
X_test_scaled  = scaler.transform(X_test[num_cols])       # transform ONLY on test (same params)
# use with: linear regression, logistic regression, SVM, PCA, neural nets

# ── MinMaxScaler: x_scaled = (x - min) / (max - min) → range [0, 1] ─────────
mm = MinMaxScaler()
X_scaled = mm.fit_transform(X[num_cols])
# use with: neural nets (sigmoid/softmax activations), image pixels
# WARNING: sensitive to outliers — one extreme value compresses all others

# ── RobustScaler: uses median and IQR, ignores outliers ──────────────────────
rs = RobustScaler()
X_scaled = rs.fit_transform(X[num_cols])
# best choice when data has outliers you can't remove

# ── Log Transform — fixes right-skewed data (salary, price, click counts) ────
df["log_income"] = np.log1p(df["income"])   # log(1+x): handles x=0 safely
# after log transform, exponentially growing values become linear → better for linear models

# ── Yeo-Johnson / Box-Cox — general normalization transform ──────────────────
pt = PowerTransformer(method="yeo-johnson")  # yeo-johnson handles zero and negative values
df["income_normal"] = pt.fit_transform(df[["income"]])  # makes distribution more Gaussian

# QUICK REFERENCE:
# Tree models (RF, XGBoost, LightGBM) → NO scaling needed — splits are scale-invariant
# Linear/Logistic/SVM/PCA/KNN         → StandardScaler
# Neural nets                          → MinMaxScaler or StandardScaler
# Data with outliers                   → RobustScaler
# Right-skewed continuous feature      → log1p or PowerTransformer
</pre></div>'''
)

print("p31 done")

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 32 — Deep Learning: find and replace key code blocks
# ─────────────────────────────────────────────────────────────────────────────
# Read p32 content to find code blocks
idx32 = html.find('id="p32"')
idx33 = html.find('id="p33"')
seg32 = html[idx32:idx33]

# Check what's there
import re
blocks32 = re.findall(r'<div class="code-block"><pre>(.*?)</pre></div>', seg32, re.DOTALL)
print(f"p32 code blocks found: {len(blocks32)}")
for i, b in enumerate(blocks32):
    print(f"  Block {i}: {b[:60].strip()!r}")

print("p32/p33 analysis done — will replace in next script")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved — {kb:.0f} KB")
