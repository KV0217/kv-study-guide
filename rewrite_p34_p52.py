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
    print(f"MISS: {old[:55]!r}")
    return False

# ============================================================
# PHASE 34 -- Pandas / NumPy
# ============================================================

# Block 1: NumPy basics
rep(
'<div class="code-block"><pre>import numpy as np\n\n# Array creation\na = np.array([1, 2, 3, 4, 5])\nm = np.array([[1,2,3],[4,5,6]])        # 2D array\nz = np.zeros((3, 4))                   # 3x4 zeros\no = np.ones((2, 3))                    # 2x3 ones\nr = np.random.randn(100)               # 100 standard normal values\nl = np.linspace(0, 1, 50)             # 50 evenly spaced from 0 to 1\ne = np.arange(0, 10, 0.5)             # like range but with floats',
'<div class="code-block"><pre>import numpy as np              # numerical computing -- fast arrays, linear algebra, math\n\n# -- Array creation --------------------------------------------------\na = np.array([1, 2, 3, 4, 5])           # 1D array from a Python list\nm = np.array([[1,2,3],[4,5,6]])         # 2D array (matrix): 2 rows, 3 cols\nz = np.zeros((3, 4))                    # 3x4 array of all zeros (float64 by default)\no = np.ones((2, 3))                     # 2x3 array of all ones\nr = np.random.randn(100)                # 100 samples from standard normal (mean=0, std=1)\nl = np.linspace(0, 1, 50)              # 50 evenly spaced values between 0 and 1 inclusive\ne = np.arange(0, 10, 0.5)              # like Python range() but supports float step'
)

# Block 2: pandas read + select
rep(
'<div class="code-block"><pre>import pandas as pd\nimport numpy as np\n\n# Reading data\ndf = pd.read_csv("data.csv")\ndf = pd.read_excel("data.xlsx", sheet_name="Sheet1")\ndf = pd.read_json("data.json")\ndf = pd.read_sql("SELECT * FROM users", conn)',
'<div class="code-block"><pre>import pandas as pd              # data manipulation and analysis library\nimport numpy as np               # used alongside pandas for numerical operations\n\n# -- Load data from multiple sources ---------------------------------\ndf = pd.read_csv("data.csv")                           # load CSV file into a DataFrame\ndf = pd.read_excel("data.xlsx", sheet_name="Sheet1")   # load specific Excel sheet\ndf = pd.read_json("data.json")                         # load JSON file\ndf = pd.read_sql("SELECT * FROM users", conn)          # load from SQL database using a connection'
)

# Block 3: GroupBy
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# Basic groupby\ndf.groupby("dept")["salary"].mean()\ndf.groupby("dept")["salary"].agg(["mean", "max", "count"])',
'<div class="code-block"><pre>import pandas as pd              # data manipulation library\n\n# -- Basic groupby: split -> apply -> combine ------------------------\ndf.groupby("dept")["salary"].mean()   # mean salary per department\ndf.groupby("dept")["salary"].agg(["mean", "max", "count"])  # multiple stats at once'
)

# Block 4: Merge/Join
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# pd.merge = SQL JOIN\n# how: "inner", "left", "right", "outer"\nresult = pd.merge(employees, departments, on="dept_id", how="left")\nresult = pd.merge(df1, df2, left_on="emp_id", right_on="id", how="inner")\n\n# Merge on multiple keys\nresult = pd.merge(orders, products,\n                  on=["product_id", "category"], how="inner")\n\n# Concat -- stack DataFrames vertically or horizontally\ncombined = pd.concat([df_2022, df_2023], axis=0, ignore_index=True)\nwide_df  = pd.concat([df_features, df_labels], axis=1)  # side by side\n\n# Join (index-based merge)\ndf1.join(df2, how="left")\n\n# Check for duplicate keys after merge (common bug!)\nresult = pd.merge(df1, df2, on="id", how="left")\nassert result.shape[0] == df1.shape[0], "Merge created extra rows -- duplicate keys in df2!"',
'<div class="code-block"><pre>import pandas as pd              # data manipulation library\n\n# -- pd.merge: equivalent of SQL JOIN --------------------------------\n# how options: "inner" (matching rows only), "left" (all left rows), "right", "outer" (all rows)\nresult = pd.merge(employees, departments, on="dept_id", how="left")    # keep all employees, add dept info\nresult = pd.merge(df1, df2, left_on="emp_id", right_on="id", how="inner")  # different key names in each df\n\n# Merge on multiple columns (composite key)\nresult = pd.merge(orders, products,\n                  on=["product_id", "category"], how="inner")  # both columns must match\n\n# pd.concat: stack DataFrames vertically (axis=0) or horizontally (axis=1)\ncombined = pd.concat([df_2022, df_2023], axis=0, ignore_index=True)  # add rows (new data)\nwide_df  = pd.concat([df_features, df_labels], axis=1)               # add columns side by side\n\n# join: index-based merge (simpler when DataFrames share an index)\ndf1.join(df2, how="left")   # joins df2 onto df1 using index as key\n\n# ALWAYS validate after merge -- duplicate keys in df2 silently expand row count\nresult = pd.merge(df1, df2, on="id", how="left")\nassert result.shape[0] == df1.shape[0], "Merge created extra rows -- duplicate keys in df2!"'
)

# Block 7: DateTime
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# Parse dates\ndf["date"] = pd.to_datetime(df["date"])\ndf["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")  # custom format\n\n# Extract components\ndf["year"]        = df["date"].dt.year\ndf["month"]       = df["date"].dt.month\ndf["day"]         = df["date"].dt.day\ndf["hour"]        = df["date"].dt.hour\ndf["day_of_week"] = df["date"].dt.dayofweek  # 0=Mon\ndf["week"]        = df["date"].dt.isocalendar().week\ndf["quarter"]     = df["date"].dt.quarter\n\n# Date arithmetic\ndf["days_since_signup"] = (pd.Timestamp.now() - df["signup_date"]).dt.days\ndf["next_payment"]      = df["last_payment"] + pd.DateOffset(months=1)\ndf["30d_window_end"]    = df["event_date"] + pd.Timedelta(days=30)\n\n# Resample (aggregate by time period)\nmonthly_sales = df.set_index("date")["sales"].resample("ME").sum()  # Monthly End\nweekly_avg    = df.set_index("date")["sales"].resample("W").mean()',
'<div class="code-block"><pre>import pandas as pd              # data manipulation library\n\n# -- Parse string columns to proper datetime type --------------------\ndf["date"] = pd.to_datetime(df["date"])                      # auto-detect format\ndf["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")   # explicit format: day/month/year\n\n# -- Extract date components using .dt accessor ----------------------\ndf["year"]        = df["date"].dt.year           # 4-digit year (e.g., 2024)\ndf["month"]       = df["date"].dt.month          # month number 1-12\ndf["day"]         = df["date"].dt.day            # day of month 1-31\ndf["hour"]        = df["date"].dt.hour           # hour 0-23\ndf["day_of_week"] = df["date"].dt.dayofweek      # 0=Monday, 6=Sunday\ndf["week"]        = df["date"].dt.isocalendar().week  # ISO week number (1-53)\ndf["quarter"]     = df["date"].dt.quarter        # quarter number 1-4\n\n# -- Date arithmetic -------------------------------------------------\ndf["days_since_signup"] = (pd.Timestamp.now() - df["signup_date"]).dt.days  # age in days\ndf["next_payment"]      = df["last_payment"] + pd.DateOffset(months=1)       # add 1 calendar month\ndf["30d_window_end"]    = df["event_date"] + pd.Timedelta(days=30)           # add 30 exact days\n\n# -- Resample: aggregate time series by a time period ----------------\nmonthly_sales = df.set_index("date")["sales"].resample("ME").sum()   # sum per month-end\nweekly_avg    = df.set_index("date")["sales"].resample("W").mean()   # mean per week'
)

# Block 8: Performance
rep(
'<div class="code-block"><pre>import pandas as pd\nimport numpy as np\n\n# 1. Use appropriate dtypes (reduces memory dramatically)\ndf["age"] = df["age"].astype("int8")         # if values fit in -128 to 127\ndf["city"] = df["city"].astype("category")   # for low-cardinality strings\nprint(df.memory_usage(deep=True).sum() / 1024**2, "MB")\n\n# 2. Vectorization > apply > loops\n# BAD (slow):\ndf["bmi"] = df.apply(lambda row: row["weight"] / row["height"]**2, axis=1)\n# GOOD (fast):\ndf["bmi"] = df["weight"] / df["height"]**2  # vectorized\n\n# 3. query() for filtering (faster on large DataFrames)\ndf.query("age > 30 and salary > 50000")   # faster than boolean indexing\n\n# 4. Chunking for large files\nfor chunk in pd.read_csv("huge_file.csv", chunksize=100000):\n    process(chunk)  # process in pieces\n\n# 5. Use .values or .to_numpy() to get NumPy array (faster for math)\nx = df["salary"].to_numpy()\nresult = np.percentile(x, [25, 50, 75])',
'<div class="code-block"><pre>import pandas as pd              # data manipulation library\nimport numpy as np               # fast numerical arrays\n\n# -- Tip 1: use smaller dtypes to cut memory 2-4x --------------------\ndf["age"]  = df["age"].astype("int8")        # int8: -128 to 127 (vs int64: 8x bigger)\ndf["city"] = df["city"].astype("category")   # stores strings as integer codes -- huge memory saving\nprint(df.memory_usage(deep=True).sum() / 1024**2, "MB")  # print total memory in megabytes\n\n# -- Tip 2: vectorization is ~100x faster than apply/loops -----------\ndf["bmi"] = df.apply(lambda row: row["weight"] / row["height"]**2, axis=1)  # SLOW: row-by-row Python\ndf["bmi"] = df["weight"] / df["height"]**2   # FAST: pandas broadcasts C-level vectorized math\n\n# -- Tip 3: query() uses numexpr engine -- faster for large DataFrames\ndf.query("age > 30 and salary > 50000")      # compiled expression, faster than boolean mask\n\n# -- Tip 4: chunk large files that don\'t fit in RAM ------------------\nfor chunk in pd.read_csv("huge_file.csv", chunksize=100_000):  # read 100k rows at a time\n    process(chunk)                           # process each chunk, append results\n\n# -- Tip 5: convert to NumPy for pure math operations ----------------\nx      = df["salary"].to_numpy()             # returns underlying NumPy array (no pandas overhead)\nresult = np.percentile(x, [25, 50, 75])      # Q1, median, Q3 -- faster than df.quantile()'
)

print(f"p34 done ({replaced} replacements so far)")

# ============================================================
# PHASE 36 -- Statistics & Probability (add comments to imports)
# ============================================================
rep(
'<div class="code-block"><pre>import numpy as np\nimport scipy.stats as stats\n\n# Central Limit Theorem demo\nimport matplotlib.pyplot as plt',
'<div class="code-block"><pre>import numpy as np               # numerical computing (array operations, random sampling)\nimport scipy.stats as stats      # statistical distributions, tests, and functions\n\n# Central Limit Theorem demo -- shows that sample means are normally distributed\nimport matplotlib.pyplot as plt  # plotting library for visualisation'
)

rep(
'<div class="code-block"><pre>import numpy as np\nimport scipy.stats as stats\n\nsample = np.random.normal(loc=170',
'<div class="code-block"><pre>import numpy as np               # for array operations and random sampling\nimport scipy.stats as stats      # for t-test and confidence interval calculations\n\nsample = np.random.normal(loc=170'
)

rep(
'<div class="code-block"><pre>import numpy as np\n\n# Expected value E[X]: average outcome weighted by probability',
'<div class="code-block"><pre>import numpy as np               # numerical operations\n\n# Expected value E[X]: the average outcome weighted by its probability of occurring'
)

print(f"p36 done ({replaced} replacements so far)")

# ============================================================
# PHASE 37 -- ML Algorithms
# ============================================================
rep(
'<div class="code-block"><pre>import numpy as np\nimport matplotlib.pyplot as plt\nfrom sklearn.linear_model import LinearRegression, Ridge, Lasso\n\n# The model: y = β₀ + β₁x₁ + β₂x₂',
'<div class="code-block"><pre>import numpy as np                          # numerical operations\nimport matplotlib.pyplot as plt             # plotting residuals and predictions\nfrom sklearn.linear_model import LinearRegression, Ridge, Lasso  # regression models\n\n# The model: y = β₀ + β₁x₁ + β₂x₂'
)

rep(
'<div class="code-block"><pre>import numpy as np\nfrom sklearn.linear_model import LogisticRegression',
'<div class="code-block"><pre>import numpy as np                          # numerical operations\nfrom sklearn.linear_model import LogisticRegression  # logistic regression classifier'
)

rep(
'<div class="code-block"><pre>from sklearn.tree import DecisionTreeClassifier, export_text',
'<div class="code-block"><pre>from sklearn.tree import DecisionTreeClassifier, export_text  # tree model + text visualisation'
)

rep(
'<div class="code-block"><pre>from sklearn.ensemble import RandomForestClassifier',
'<div class="code-block"><pre>from sklearn.ensemble import RandomForestClassifier  # ensemble of decision trees'
)

rep(
'<div class="code-block"><pre>from xgboost import XGBClassifier\nimport numpy as np',
'<div class="code-block"><pre>from xgboost import XGBClassifier   # gradient boosted trees (fastest, most accurate tabular model)\nimport numpy as np                  # numerical operations'
)

rep(
'<div class="code-block"><pre>from sklearn.svm import SVC, SVR\nimport numpy as np',
'<div class="code-block"><pre>from sklearn.svm import SVC, SVR    # Support Vector Classifier / Regressor\nimport numpy as np                  # array operations'
)

rep(
'<div class="code-block"><pre>from sklearn.cluster import KMeans\nimport numpy as np',
'<div class="code-block"><pre>from sklearn.cluster import KMeans  # unsupervised clustering algorithm\nimport numpy as np                  # array operations'
)

rep(
'<div class="code-block"><pre>from sklearn.decomposition import PCA\nimport numpy as np',
'<div class="code-block"><pre>from sklearn.decomposition import PCA  # Principal Component Analysis -- dimensionality reduction\nimport numpy as np                     # numerical operations'
)

print(f"p37 done ({replaced} replacements so far)")

# ============================================================
# PHASE 48 -- MLOps / MLflow
# ============================================================
rep(
'<div class="code-block"><pre>import mlflow\nimport mlflow.sklearn\nimport pandas as pd\nimport numpy as np\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import accuracy_score, roc_auc_score, f1_score\n\n# Start MLflow server (run in terminal):',
'<div class="code-block"><pre>import mlflow                    # experiment tracking: logs params, metrics, models\nimport mlflow.sklearn            # auto-integration for sklearn models\nimport pandas as pd              # data loading and manipulation\nimport numpy as np               # array operations\nfrom sklearn.ensemble import RandomForestClassifier  # model to track\nfrom sklearn.model_selection import train_test_split # split into train/test\nfrom sklearn.metrics import accuracy_score, roc_auc_score, f1_score  # evaluation metrics\n\n# Start MLflow server (run in terminal):'
)

# ============================================================
# PHASE 49 -- Data Engineering
# ============================================================
rep(
'<div class="code-block"><pre>from airflow import DAG\nfrom airflow.operators.python import PythonOperator',
'<div class="code-block"><pre>from airflow import DAG                        # DAG = Directed Acyclic Graph (workflow definition)\nfrom airflow.operators.python import PythonOperator  # operator that runs a Python function'
)

# ============================================================
# PHASE 50 -- PySpark
# ============================================================
rep(
'<div class="code-block"><pre>from pyspark.sql import SparkSession\nfrom pyspark.sql import functions as F\nfrom pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType',
'<div class="code-block"><pre>from pyspark.sql import SparkSession    # entry point to all Spark functionality\nfrom pyspark.sql import functions as F  # built-in Spark SQL functions (col, sum, avg, etc.)\nfrom pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType\n# type classes: define schema explicitly for performance and error detection'
)

rep(
'<div class="code-block"><pre>from pyspark.ml.feature import VectorAssembler, StandardScaler\nfrom pyspark.ml.classification import LogisticRegression',
'<div class="code-block"><pre>from pyspark.ml.feature import VectorAssembler, StandardScaler  # feature prep transformers\nfrom pyspark.ml.classification import LogisticRegression  # Spark distributed LR classifier'
)

# ============================================================
# PHASE 51 -- Model Monitoring
# ============================================================
rep(
'<div class="code-block"><pre>import numpy as np\nimport pandas as pd\nfrom scipy import stats\n\n# Population Stability Index (PSI)',
'<div class="code-block"><pre>import numpy as np               # array operations and binning\nimport pandas as pd              # data loading and tabular operations\nfrom scipy import stats          # Kolmogorov-Smirnov test\n\n# Population Stability Index (PSI)'
)

# ============================================================
# PHASE 52 -- Cloud
# ============================================================
rep(
'<div class="code-block"><pre>import boto3\nimport pandas as pd\nfrom io import StringIO, BytesIO\n\n# S3 = Simple Storage Service: store ANY file (CSV, parquet, model, image)\n# Buckets = top-level containers (like folders)\n# Objects = files inside buckets',
'<div class="code-block"><pre>import boto3                     # AWS SDK for Python -- interact with S3, SageMaker, etc.\nimport pandas as pd              # read/write DataFrames\nfrom io import StringIO, BytesIO # in-memory file objects (needed to read S3 objects as DataFrames)\n\n# S3 = Simple Storage Service: store ANY file (CSV, parquet, pickled model, images)\n# Buckets = top-level containers (like Google Drive folders)\n# Objects = individual files stored inside a bucket'
)

print(f"\nTotal replacements: {replaced}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
