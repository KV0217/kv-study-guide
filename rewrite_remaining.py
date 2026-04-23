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
# PHASE 31 -- Feature Engineering (remaining blocks)
# ============================================================

# p31 block[3]: Scaling -- first 2 import lines missing comments
rep(
'<div class="code-block"><pre>from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler\nfrom sklearn.preprocessing import PowerTransformer  # for skewness correction\nimport numpy as np',
'<div class="code-block"><pre>from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler  # scalers for different distributions\nfrom sklearn.preprocessing import PowerTransformer  # for skewness correction\nimport numpy as np  # log1p transform for skewed features'
)

# p31 block[4]: Imbalanced classes -- all 4 import lines missing comments
rep(
'<div class="code-block"><pre>from imblearn.over_sampling import SMOTE, ADASYN\nfrom imblearn.under_sampling import RandomUnderSampler\nfrom imblearn.pipeline import Pipeline\nfrom sklearn.ensemble import RandomForestClassifier\n\n# Check imbalance',
'<div class="code-block"><pre>from imblearn.over_sampling import SMOTE, ADASYN  # create synthetic minority samples\nfrom imblearn.under_sampling import RandomUnderSampler  # reduce majority class size\nfrom imblearn.pipeline import Pipeline  # combine resampling + model into one step\nfrom sklearn.ensemble import RandomForestClassifier  # model to train on balanced data\n\n# Check imbalance'
)

# p31 block[5]: Feature engineering -- imports at top + PolynomialFeatures mid-block
rep(
'<div class="code-block"><pre>import pandas as pd\nimport numpy as np\n\n# --- Interaction features',
'<div class="code-block"><pre>import pandas as pd  # DataFrame operations and date parsing\nimport numpy as np   # log transforms and array operations\n\n# --- Interaction features'
)

rep(
'from sklearn.preprocessing import PolynomialFeatures\npoly = PolynomialFeatures(degree=2',
'from sklearn.preprocessing import PolynomialFeatures  # auto-generate x^2, x1*x2, etc.\npoly = PolynomialFeatures(degree=2'
)

# p31 block[6]: Feature selection -- 5 import lines + VIF import mid-block
rep(
'<div class="code-block"><pre>from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif\nfrom sklearn.feature_selection import RFE\nfrom sklearn.ensemble import RandomForestClassifier\nimport pandas as pd\nimport numpy as np',
'<div class="code-block"><pre>from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif  # statistical feature scoring\nfrom sklearn.feature_selection import RFE  # recursive feature elimination\nfrom sklearn.ensemble import RandomForestClassifier  # used for importance-based selection\nimport pandas as pd  # store features and their scores as DataFrame\nimport numpy as np  # upper-triangle masking for correlation matrix'
)

rep(
'from statsmodels.stats.outliers_influence import variance_inflation_factor\nvif = pd.DataFrame()',
'from statsmodels.stats.outliers_influence import variance_inflation_factor  # detect multicollinearity\nvif = pd.DataFrame()'
)

print(f"p31 done ({replaced} replacements so far)")

# ============================================================
# PHASE 33 -- Time Series (remaining blocks)
# ============================================================

# p33 block[1]: warnings import mid-block
rep(
'import warnings\nwarnings.filterwarnings',
'import warnings  # suppress statsmodels convergence warnings\nwarnings.filterwarnings'
)

# p33 block[2]: Prophet imports
rep(
'<div class="code-block"><pre>from prophet import Prophet\nimport pandas as pd\n\n# Prophet requires columns',
'<div class="code-block"><pre>from prophet import Prophet  # Meta\'s time series forecasting library (handles trend + seasonality + holidays)\nimport pandas as pd  # load and reshape time series data\n\n# Prophet requires columns'
)

rep(
'from prophet.make_holidays import make_holidays_df\nholidays = make_holidays_df',
'from prophet.make_holidays import make_holidays_df  # fetch public holidays for a country\nholidays = make_holidays_df'
)

rep(
'from sklearn.metrics import mean_absolute_percentage_error\ny_pred = forecast',
'from sklearn.metrics import mean_absolute_percentage_error  # MAPE: % error, scale-independent\ny_pred = forecast'
)

# p33 block[3]: XGBoost for time series
rep(
'<div class="code-block"><pre>import pandas as pd\nimport numpy as np\nfrom xgboost import XGBRegressor\nfrom sklearn.metrics import mean_absolute_error',
'<div class="code-block"><pre>import pandas as pd  # date indexing and feature creation\nimport numpy as np   # array operations\nfrom xgboost import XGBRegressor    # gradient boosted trees for time series (via lag features)\nfrom sklearn.metrics import mean_absolute_error  # MAE: average absolute prediction error'
)

# p33 block[4]: TimeSeriesSplit
rep(
'<div class="code-block"><pre>from sklearn.model_selection import TimeSeriesSplit\n\n# NEVER use KFold',
'<div class="code-block"><pre>from sklearn.model_selection import TimeSeriesSplit  # walk-forward cross-validation (no future leakage)\n\n# NEVER use KFold'
)

print(f"p33 done ({replaced} replacements so far)")

# ============================================================
# PHASE 34 -- Pandas (remaining blocks)
# ============================================================

# p34 block[4]: pivot_table
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# pivot_table',
'<div class="code-block"><pre>import pandas as pd  # pivot_table, melt, stack/unstack, crosstab operations\n\n# pivot_table'
)

# p34 block[5]: string operations
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# All string methods via .str accessor',
'<div class="code-block"><pre>import pandas as pd  # .str accessor for vectorized string operations\n\n# All string methods via .str accessor'
)

# p34 block[8]: data cleaning
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# 1. Find duplicates and remove',
'<div class="code-block"><pre>import pandas as pd  # duplicates, ranking, rolling, cumulative operations\n\n# 1. Find duplicates and remove'
)

print(f"p34 done ({replaced} replacements so far)")

# ============================================================
# PHASE 36 -- Statistics (remaining: block [4] sample array)
# ============================================================

# Already fixed in fix_missed_blocks.py
# Verify by checking if there's still a miss
rep(
'<div class="code-block"><pre>import numpy as np\nimport scipy.stats as stats\n\nsample = np.array([12.5',
'<div class="code-block"><pre>import numpy as np               # array operations and statistics\nimport scipy.stats as stats      # t-test and confidence intervals\n\nsample = np.array([12.5'
)

print(f"p36 done ({replaced} replacements so far)")

# ============================================================
# PHASE 37 -- ML Algorithms (remaining blocks)
# ============================================================

# Check if any blocks still missing after previous rewrites
# p37 had 7 missing -- these are likely mid-block imports in model-specific blocks

# ============================================================
# PHASE 48 -- MLOps (remaining blocks)
# ============================================================

# block[1]: compare experiments
rep(
'<div class="code-block"><pre>import mlflow\nfrom mlflow.tracking import MlflowClient\n\n# Run experiments with different hyperparameters',
'<div class="code-block"><pre>import mlflow                        # core experiment tracking (log params, metrics)\nfrom mlflow.tracking import MlflowClient  # programmatic API to query runs and experiments\n\n# Run experiments with different hyperparameters'
)

# block[2]: model registry
rep(
'<div class="code-block"><pre>from mlflow.tracking import MlflowClient\nimport mlflow\n\nclient = MlflowClient()',
'<div class="code-block"><pre>from mlflow.tracking import MlflowClient  # query model registry and manage lifecycle\nimport mlflow                # log and register models\n\nclient = MlflowClient()'
)

# block[3]: autologging
rep(
'<div class="code-block"><pre>import mlflow\nimport mlflow.sklearn\nimport mlflow.xgboost\n\n# Autologging:',
'<div class="code-block"><pre>import mlflow              # core tracking functionality\nimport mlflow.sklearn      # auto-log sklearn models (params, metrics, artifacts)\nimport mlflow.xgboost      # auto-log XGBoost models\n\n# Autologging:'
)

# block[4]: retraining pipeline
rep(
'# Simplified automated retraining script (runs on schedule or data trigger)\nimport mlflow\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import roc_auc_score',
'# Simplified automated retraining script (runs on schedule or data trigger)\nimport mlflow                    # log metrics and register retrained model\nimport pandas as pd              # load and preprocess new data\nfrom sklearn.model_selection import train_test_split  # hold out evaluation set\nfrom sklearn.ensemble import RandomForestClassifier  # model to retrain\nfrom sklearn.metrics import roc_auc_score  # evaluation metric for classification'
)

print(f"p48 done ({replaced} replacements so far)")

# ============================================================
# PHASE 49 -- Data Engineering (remaining blocks)
# ============================================================

# block[3]: BashOperator (partial already has comments)
rep(
'from airflow.operators.bash import BashOperator\nfrom datetime import datetime, timedelta',
'from airflow.operators.bash import BashOperator  # operator that runs a bash shell command\nfrom datetime import datetime, timedelta  # define schedule intervals and execution dates'
)

# block[4]: data quality checks
rep(
'<div class="code-block"><pre>import pandas as pd\nimport numpy as np\n\ndef run_data_quality_checks',
'<div class="code-block"><pre>import pandas as pd  # load tables and compute statistics\nimport numpy as np   # numerical thresholds and value checks\n\ndef run_data_quality_checks'
)

print(f"p49 done ({replaced} replacements so far)")

# ============================================================
# PHASE 50 -- PySpark (remaining blocks)
# ============================================================

# p50 block[0]: StructType line (already has SparkSession and F comments)
rep(
'from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType\n# type classes:',
'from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType  # schema types\n# type classes:'
)

# p50 blocks [1], [2], [3]: all start with `from pyspark.sql import functions as F`
# block[1] context: KEY CONCEPT Transformations
rep(
'<div class="code-block"><pre>from pyspark.sql import functions as F\n\n# KEY CONCEPT: Transformations are LAZY',
'<div class="code-block"><pre>from pyspark.sql import functions as F  # Spark built-in functions (col, sum, count, avg, etc.)\n\n# KEY CONCEPT: Transformations are LAZY'
)

# block[2] context: GroupBy
rep(
'<div class="code-block"><pre>from pyspark.sql import functions as F\n\n# GroupBy',
'<div class="code-block"><pre>from pyspark.sql import functions as F  # aggregation functions (sum, avg, count, etc.)\n\n# GroupBy'
)

# block[3] context: Regular joins
rep(
'<div class="code-block"><pre>from pyspark.sql import functions as F\n\n# Regular joins',
'<div class="code-block"><pre>from pyspark.sql import functions as F  # broadcast(), col(), and other join helpers\n\n# Regular joins'
)

rep(
'from pyspark.sql.window import Window\n',
'from pyspark.sql.window import Window  # define window frames for row_number, rank, lag\n'
)

rep(
'from pyspark.sql.functions import broadcast\n',
'from pyspark.sql.functions import broadcast  # hint Spark to broadcast small table to all workers\n'
)

print(f"p50 done ({replaced} replacements so far)")

# ============================================================
# PHASE 51 -- Model Monitoring (remaining blocks)
# ============================================================

# block[1]: Evidently library
rep(
'<div class="code-block"><pre>from evidently.report import Report\nfrom evidently.metric_preset import DataDriftPreset, ClassificationPreset\nfrom evidently.metrics import *\nimport pandas as pd\n\n# pip install evidently',
'<div class="code-block"><pre>from evidently.report import Report  # generate HTML/JSON monitoring reports\nfrom evidently.metric_preset import DataDriftPreset, ClassificationPreset  # pre-built metric sets\nfrom evidently.metrics import *  # individual metrics (DatasetDriftMetric, etc.)\nimport pandas as pd  # load reference and current data\n\n# pip install evidently'
)

# block[2]: prediction logging
rep(
'<div class="code-block"><pre>import pandas as pd\nimport numpy as np\nfrom datetime import datetime, timedelta\n\n# Log predictions in production',
'<div class="code-block"><pre>import pandas as pd  # store prediction logs as DataFrames\nimport numpy as np   # statistical calculations for drift detection\nfrom datetime import datetime, timedelta  # timestamp predictions and define monitoring windows\n\n# Log predictions in production'
)

print(f"p51 done ({replaced} replacements so far)")

# ============================================================
# PHASE 52 -- Cloud (remaining blocks)
# ============================================================

# block[0]: pyarrow and s3fs (mid-block imports)
rep(
'import pyarrow as pa\nimport pyarrow.parquet as pq',
'import pyarrow as pa           # Apache Arrow format: columnar in-memory data\nimport pyarrow.parquet as pq  # write/read Parquet files directly to/from S3'
)

rep(
'import s3fs\n',
'import s3fs  # S3 filesystem interface -- lets pandas read s3:// paths directly\n'
)

# block[1]: BigQuery
rep(
'<div class="code-block"><pre>from google.cloud import bigquery\nimport pandas as pd\n\n# BigQuery: serverless data warehouse',
'<div class="code-block"><pre>from google.cloud import bigquery  # Google BigQuery client -- run SQL on cloud warehouse\nimport pandas as pd  # convert BigQuery results to DataFrame\n\n# BigQuery: serverless data warehouse'
)

rep(
'import pandas_gbq\n',
'import pandas_gbq  # convenience wrapper: pd.read_gbq() and pd.to_gbq()\n'
)

# block[2]: SageMaker
rep(
'<div class="code-block"><pre>import sagemaker\nfrom sagemaker.sklearn.estimator import SKLearn\nfrom sagemaker import get_execution_role\nimport boto3\n\nrole',
'<div class="code-block"><pre>import sagemaker                          # AWS ML platform SDK\nfrom sagemaker.sklearn.estimator import SKLearn  # run sklearn on managed SageMaker instances\nfrom sagemaker import get_execution_role  # IAM role that grants SageMaker S3 and ECR access\nimport boto3                              # AWS SDK for S3 uploads and other AWS services\n\nrole'
)

rep(
'import numpy as np\npreds = predictor',
'import numpy as np  # convert predictions to array\npreds = predictor'
)

# block[3]: Vertex AI
rep(
'<div class="code-block"><pre>from google.cloud import aiplatform\nimport pandas as pd\n\naiplatform.init',
'<div class="code-block"><pre>from google.cloud import aiplatform  # Google Vertex AI SDK for managed ML\nimport pandas as pd  # prepare training data as DataFrame\n\naiplatform.init'
)

# block[4]: AWS Lambda ETL
rep(
'<div class="code-block"><pre>import boto3\nimport pandas as pd\nimport os\n\n# Pattern 1: Load data from S3',
'<div class="code-block"><pre>import boto3      # AWS SDK -- read/write S3, trigger Lambda, send SNS alerts\nimport pandas as pd  # process data in memory between S3 read and write\nimport os  # read environment variables (S3 bucket names, credentials)\n\n# Pattern 1: Load data from S3'
)

print(f"p52 done ({replaced} replacements so far)")

# ============================================================
# SAVE
# ============================================================

print(f"\nTotal replacements: {replaced}")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
