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

# p34 merge/join block (has em dash in original)
rep(
'<div class="code-block"><pre>import pandas as pd\n\n# pd.merge = SQL JOIN\n# how: "inner", "left", "right", "outer"\nresult = pd.merge(employees, departments, on="dept_id", how="left")\nresult = pd.merge(df1, df2, left_on="emp_id", right_on="id", how="inner")\n\n# Merge on multiple keys\nresult = pd.merge(orders, products,\n                  on=["product_id", "category"], how="inner")\n\n# Concat — stack DataFrames vertically or horizontally\ncombined = pd.concat([df_2022, df_2023], axis=0, ignore_index=True)\nwide_df  = pd.concat([df_features, df_labels], axis=1)  # side by side\n\n# Join (index-based merge)\ndf1.join(df2, how="left")\n\n# Check for duplicate keys after merge (common bug!)\nresult = pd.merge(df1, df2, on="id", how="left")\nassert result.shape[0] == df1.shape[0], "Merge created extra rows — duplicate keys in df2!"',
'<div class="code-block"><pre>import pandas as pd              # data manipulation library\n\n# -- pd.merge: equivalent of SQL JOIN --------------------------------\n# how options: "inner" (matching rows only), "left" (all left rows), "right", "outer" (all rows)\nresult = pd.merge(employees, departments, on="dept_id", how="left")    # keep all employees, add dept info\nresult = pd.merge(df1, df2, left_on="emp_id", right_on="id", how="inner")  # different key names in each df\n\n# Merge on multiple columns (composite key)\nresult = pd.merge(orders, products,\n                  on=["product_id", "category"], how="inner")  # both columns must match\n\n# pd.concat: stack DataFrames vertically (axis=0) or horizontally (axis=1)\ncombined = pd.concat([df_2022, df_2023], axis=0, ignore_index=True)  # add rows (new data)\nwide_df  = pd.concat([df_features, df_labels], axis=1)               # add columns side by side\n\n# join: index-based merge (simpler when DataFrames share an index)\ndf1.join(df2, how="left")   # joins df2 onto df1 using index as key\n\n# ALWAYS validate after merge -- duplicate keys in df2 silently expand row count\nresult = pd.merge(df1, df2, on="id", how="left")\nassert result.shape[0] == df1.shape[0], "Merge created extra rows -- duplicate keys in df2!"'
)

# p36 block [2]: Normal distribution
rep(
'<div class="code-block"><pre>import numpy as np\nimport scipy.stats as stats\n\n# Normal distribution\nmu, sigma = 170, 10',
'<div class="code-block"><pre>import numpy as np               # array operations and mathematical functions\nimport scipy.stats as stats      # statistical distributions (norm, t, chi2, etc.)\n\n# Normal distribution\nmu, sigma = 170, 10'
)

# p36 block [3]: CLT demo with matplotlib
rep(
'<div class="code-block"><pre>import numpy as np\nimport matplotlib.pyplot as plt\n\n# CLT: regardless of the population distribution,',
'<div class="code-block"><pre>import numpy as np               # array operations and random sampling\nimport matplotlib.pyplot as plt  # plotting histograms to visualise distributions\n\n# CLT: regardless of the population distribution,'
)

# p50 block [5]: PySpark MLlib Pipeline
rep(
'<div class="code-block"><pre>from pyspark.ml import Pipeline\nfrom pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler\nfrom pyspark.ml.classification import RandomForestClassifier\nfrom pyspark.ml.evaluation im',
'<div class="code-block"><pre>from pyspark.ml import Pipeline              # chains multiple stages into one reusable workflow\nfrom pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler  # feature transformers\nfrom pyspark.ml.classification import RandomForestClassifier  # distributed ensemble classifier\nfrom pyspark.ml.evaluation im'
)

print(f"Fixed {replaced} missed blocks")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved -- {kb:.0f} KB")
