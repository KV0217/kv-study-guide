# -*- coding: utf-8 -*-
with open("KV_Ultimate_Guide.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── P32 Block 1: Forward pass + backprop ─────────────────────────────────────
html = html.replace(
    '''<div class="code-block"><pre>import torch
import torch.nn as nn

# Simple neural network
class SimpleNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu   = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.layer1(x)   # linear transformation: Wx + b
        x = self.relu(x)     # non-linearity
        x = self.layer2(x)   # output layer
        return x

model = SimpleNet(10, 64, 1)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.BCEWithLogitsLoss()  # for binary classification

# Training loop
for epoch in range(100):
    optimizer.zero_grad()          # reset gradients
    output = model(X_train)        # forward pass
    loss = criterion(output, y_train)  # compute loss
    loss.backward()                # backpropagation — compute gradients
    optimizer.step()               # update weights: w = w - lr * gradient
</pre></div>''',
    '''<div class="code-block"><pre>import torch                         # PyTorch deep learning framework
import torch.nn as nn                # neural network building blocks (layers, activations, losses)

class SimpleNet(nn.Module):          # inherit from Module — gives .parameters(), .train(), .eval()
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()           # initialize parent Module class (required)
        self.layer1 = nn.Linear(input_size, hidden_size)  # fully connected: y = Wx + b
        self.relu   = nn.ReLU()      # activation: max(0, x) — adds non-linearity
        self.layer2 = nn.Linear(hidden_size, output_size) # output layer, 1 unit for binary

    def forward(self, x):            # defines the computation graph (called by model(X))
        x = self.layer1(x)           # linear transformation: 10 inputs → 64 hidden units
        x = self.relu(x)             # apply ReLU: negative activations become 0
        x = self.layer2(x)           # 64 hidden → 1 output (raw logit, not probability)
        return x                     # return raw logit — BCEWithLogitsLoss applies sigmoid internally

model     = SimpleNet(10, 64, 1)                           # 10 features, 64 hidden, 1 output
optimizer = torch.optim.Adam(model.parameters(), lr=0.001) # Adam: adaptive lr per parameter
criterion = nn.BCEWithLogitsLoss()                         # combines sigmoid + BCE — numerically stable

for epoch in range(100):             # train for 100 full passes over the data
    optimizer.zero_grad()            # MUST clear gradients — they accumulate by default in PyTorch
    output = model(X_train)          # forward pass: compute predictions
    loss   = criterion(output, y_train)  # compute how wrong predictions are
    loss.backward()                  # backprop: compute dL/dW for every weight via chain rule
    optimizer.step()                 # gradient descent: W = W - lr * dL/dW
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")  # monitor every 10 epochs
</pre></div>'''
)

# ── P32 Block 2: Regularization ───────────────────────────────────────────────
html = html.replace(
    '''<div class="code-block"><pre>import torch.nn as nn

# Dropout — randomly zero out neurons during training
class RegularizedNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1  = nn.Linear(100, 256)
        self.dropout = nn.Dropout(p=0.3)  # 30% neurons dropped each forward pass
        self.layer2  = nn.Linear(256, 1)
        self.bn      = nn.BatchNorm1d(256)  # batch normalization

    def forward(self, x):
        x = self.layer1(x)
        x = self.bn(x)          # normalize activations (helps training stability)
        x = nn.ReLU()(x)
        x = self.dropout(x)     # only active during training, disabled at test time
        return self.layer2(x)

# L2 Regularization (weight decay) — in optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

# Early Stopping — stop when validation loss stops improving
best_val_loss = float("inf")
patience = 10
counter  = 0
for epoch in range(1000):
    train_loss = train_one_epoch(model, train_loader)
    val_loss   = evaluate(model, val_loader)
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        torch.save(model.state_dict(), "best_model.pt")
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print(f"Early stopping at epoch {epoch}")
            break
</pre></div>''',
    '''<div class="code-block"><pre>import torch.nn as nn                # nn module for all layer types

class RegularizedNet(nn.Module):     # network with 3 anti-overfitting techniques
    def __init__(self):
        super().__init__()           # required parent class init
        self.layer1  = nn.Linear(100, 256)      # input layer: 100 features → 256 hidden
        self.dropout = nn.Dropout(p=0.3)        # dropout: randomly zeros 30% of neurons each step
        self.layer2  = nn.Linear(256, 1)        # output layer: 256 → 1 prediction
        self.bn      = nn.BatchNorm1d(256)      # batch norm: normalize across the batch dimension

    def forward(self, x):
        x = self.layer1(x)           # linear transformation (no activation yet)
        x = self.bn(x)               # normalize: mean~0, std~1 per feature over the batch
        x = nn.ReLU()(x)             # apply ReLU after batch norm (recommended order: Linear → BN → ReLU)
        x = self.dropout(x)          # randomly drop neurons during train; pass-through during eval
        return self.layer2(x)        # output logit (no sigmoid — use BCEWithLogitsLoss)

# Technique 2: L2 regularization via weight_decay parameter
optimizer = torch.optim.Adam(model.parameters(), lr=0.001,
                              weight_decay=1e-4)  # adds lambda*||W||^2 penalty to loss

# Technique 3: Early stopping — halt training when val loss stops improving
best_val_loss = float("inf")         # track the best validation loss seen so far
patience = 10                        # stop if val loss doesn't improve for 10 consecutive epochs
counter  = 0                         # counts consecutive epochs without improvement
for epoch in range(1000):            # set high max epochs — early stopping will cut short
    train_loss = train_one_epoch(model, train_loader)  # one gradient step over all batches
    val_loss   = evaluate(model, val_loader)           # no gradients, just measure performance
    if val_loss &lt; best_val_loss:      # new best → save checkpoint
        best_val_loss = val_loss
        torch.save(model.state_dict(), "best_model.pt")  # save weights only (not optimizer state)
        counter = 0                  # reset patience counter
    else:
        counter += 1                 # one more epoch without improvement
        if counter &gt;= patience:      # patience exhausted
            print(f"Early stopping at epoch {epoch}")
            break                    # exit training loop; load best_model.pt for inference
</pre></div>'''
)

# ── P32 Block 3: CNN ──────────────────────────────────────────────────────────
html = html.replace(
    '''<div class="code-block"><pre>import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        # Conv layer: learns spatial patterns (edges, textures, shapes)
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)  # 3 channels in, 32 filters
        self.pool  = nn.MaxPool2d(2, 2)  # downsample: 32x32 → 16x16
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1   = nn.Linear(64 * 8 * 8, 512)  # flatten + dense
        self.fc2   = nn.Linear(512, num_classes)

    def forward(self, x):
        x = self.pool(nn.ReLU()(self.conv1(x)))  # (N,32,16,16)
        x = self.pool(nn.ReLU()(self.conv2(x)))  # (N,64,8,8)
        x = x.view(x.size(0), -1)                # flatten
        x = nn.ReLU()(self.fc1(x))
        return self.fc2(x)

# In practice: use pretrained models (transfer learning) — much better
from torchvision import models
resnet = models.resnet50(pretrained=True)
resnet.fc = nn.Linear(2048, num_classes)  # replace final layer for your task
</pre></div>''',
    '''<div class="code-block"><pre>import torch.nn as nn                # neural network modules

class SimpleCNN(nn.Module):          # Convolutional Neural Network for image classification
    def __init__(self, num_classes=10):
        super().__init__()           # initialize nn.Module
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        # Conv2d: 3 input channels (RGB), 32 filters, 3x3 kernel, padding keeps spatial size
        # learns to detect low-level features: edges, colour blobs
        self.pool  = nn.MaxPool2d(2, 2)  # 2x2 max pooling: halves width and height (32→16)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # second conv: 32 channels → 64 filters; learns higher-level features (shapes, textures)
        self.fc1   = nn.Linear(64 * 8 * 8, 512)  # flatten 64 feature maps of 8x8 → 512 dense
        self.fc2   = nn.Linear(512, num_classes)  # final classifier: 512 → 10 class scores

    def forward(self, x):            # input x: (batch, 3, 32, 32) — batch of RGB 32x32 images
        x = self.pool(nn.ReLU()(self.conv1(x)))  # conv → ReLU → pool: (N,32,16,16)
        x = self.pool(nn.ReLU()(self.conv2(x)))  # conv → ReLU → pool: (N,64,8,8)
        x = x.view(x.size(0), -1)    # flatten: (N, 64*8*8=4096) — needed for Linear layer
        x = nn.ReLU()(self.fc1(x))   # dense layer with ReLU: (N, 512)
        return self.fc2(x)           # raw class scores (logits), shape (N, num_classes)

# In practice: always use transfer learning — pretrained models are far better
from torchvision import models
resnet = models.resnet50(pretrained=True)     # 50-layer ResNet trained on 1.2M ImageNet images
resnet.fc = nn.Linear(2048, num_classes)      # replace final classification head for our task
# freeze early layers: for param in resnet.parameters(): param.requires_grad = False
# then only train resnet.fc — faster + needs less data
</pre></div>'''
)

# ── P32 Block 4: LSTM ─────────────────────────────────────────────────────────
html = html.replace(
    '''<div class="code-block"><pre>import torch.nn as nn

class SentimentLSTM(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True,
                            num_layers=2, dropout=0.3, bidirectional=True)
        self.fc   = nn.Linear(hidden_dim * 2, num_classes)  # *2 for bidirectional

    def forward(self, x):
        x = self.embedding(x)           # (batch, seq_len, embed_dim)
        out, (hidden, cell) = self.lstm(x)  # out: (batch, seq_len, hidden*2)
        out = out[:, -1, :]             # take last time step
        return self.fc(out)

# Key LSTM concepts:
# hidden state: short-term memory (passed between time steps)
# cell state: long-term memory (controlled by gates)
# forget gate: what to forget from cell state
# input gate: what new info to add
# output gate: what to output as hidden state
</pre></div>''',
    '''<div class="code-block"><pre>import torch.nn as nn                # imports all layer types

class SentimentLSTM(nn.Module):      # LSTM-based text classifier
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()           # required nn.Module init
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        # Embedding: lookup table (vocab_size x embed_dim); maps each word index → dense vector
        self.lstm = nn.LSTM(
            embed_dim,               # input size: each timestep is an embed_dim vector
            hidden_dim,              # number of LSTM units (memory capacity)
            batch_first=True,        # input shape: (batch, seq_len, features) — easier to use
            num_layers=2,            # stack 2 LSTM layers for deeper representation
            dropout=0.3,             # dropout between stacked LSTM layers (not last layer)
            bidirectional=True       # process sequence both forward AND backward
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
        # *2 because bidirectional: concatenates forward + backward hidden states

    def forward(self, x):            # x: (batch, seq_len) — integer token IDs
        x = self.embedding(x)        # (batch, seq_len, embed_dim) — dense word vectors
        out, (hidden, cell) = self.lstm(x)
        # out: (batch, seq_len, hidden*2) — output at every time step
        # hidden: (2*num_layers, batch, hidden) — final hidden state (short-term memory)
        # cell: (2*num_layers, batch, hidden) — final cell state (long-term memory)
        out = out[:, -1, :]          # take output at last time step: (batch, hidden*2)
        return self.fc(out)          # classify: (batch, num_classes)

# LSTM gate summary:
# Forget gate: sigmoid decides what % of cell state to erase
# Input gate:  sigmoid decides what new info to store in cell
# Output gate: sigmoid decides what to output as hidden state from cell
</pre></div>'''
)

# ── P32 Block 5: Self-attention ───────────────────────────────────────────────
html = html.replace(
    '''<div class="code-block"><pre># Self-attention in plain English:
# Each token looks at ALL other tokens and decides which ones to pay attention to.
# "The bank on the river bank" — "bank" attends differently in each position.

# Scaled Dot-Product Attention:
# Attention(Q, K, V) = softmax(QKᵀ / sqrt(d_k)) × V
# Q = what am I looking for?
# K = what do I have to offer?
# V = what do I actually give?

import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / d_k**0.5  # scale to prevent vanishing gradients
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, V), weights

# Multi-head attention: run attention H times in parallel with different Q,K,V projections
# Each head can attend to different aspects of the input
</pre></div>''',
    '''<div class="code-block"><pre># Self-attention: each token looks at ALL other tokens and decides which to attend to
# Example: "The bank on the river bank" — both "bank"s share a word but different meanings
# Self-attention resolves meaning by looking at surrounding context

# Formula: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
# Q (Query)  = "what information am I looking for?"
# K (Key)    = "what information does each token offer?"
# V (Value)  = "what information does each token actually contain?"

import torch                          # PyTorch tensor operations
import torch.nn.functional as F       # softmax, relu, etc.

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)                  # dimension of key vectors (for scaling)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / d_k**0.5
    # QK^T: similarity between each query and every key; divide by sqrt(d_k) to stabilise gradients
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        # mask future positions in decoder (causal/autoregressive mask): set to -inf before softmax
    weights = F.softmax(scores, dim=-1) # convert similarities to attention probabilities (sum to 1)
    return torch.matmul(weights, V), weights
    # weighted sum of V using attention weights + return weights for visualisation

# Multi-head attention: run H attention functions in parallel with different Q,K,V projections
# Head 1 might focus on syntax, Head 2 on coreference, Head 3 on semantics — each specialises
</pre></div>'''
)

print("p32 done")

# ── P33: Time Series code blocks ──────────────────────────────────────────────

# Block 1: EDA
html = html.replace(
    '''<div class="code-block"><pre>import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller

df = pd.read_csv("sales.csv", parse_dates=["date"], index_col="date")
ts = df["sales"]

# 1. Decomposition
result = seasonal_decompose(ts, model="additive", period=12)  # monthly → period=12
result.plot()
plt.show()

# 2. ACF and PACF plots (for ARIMA order selection)
plot_acf(ts, lags=40)   # correlation with past values → MA order
plot_pacf(ts, lags=40)  # partial correlation → AR order
plt.show()

# 3. Stationarity test (Augmented Dickey-Fuller)
result = adfuller(ts)
print(f"ADF Statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")
# p < 0.05 → stationary (reject null of unit root)
# p > 0.05 → non-stationary → need differencing

# 4. Make stationary via differencing
ts_diff = ts.diff().dropna()        # first-order differencing
ts_diff2 = ts.diff().diff().dropna()  # second-order (rarely needed)

# 5. Log transform for multiplicative seasonality
ts_log = np.log(ts)
ts_log_diff = ts_log.diff().dropna()
</pre></div>''',
    '''<div class="code-block"><pre>import pandas as pd                    # data loading and manipulation
import numpy as np                     # numerical operations
import matplotlib.pyplot as plt        # plotting
from statsmodels.tsa.seasonal import seasonal_decompose  # decompose into trend/seasonal/residual
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf  # autocorrelation plots
from statsmodels.tsa.stattools import adfuller  # Augmented Dickey-Fuller stationarity test

df = pd.read_csv("sales.csv", parse_dates=["date"], index_col="date")  # parse date as datetime index
ts = df["sales"]                       # extract the time series as a pandas Series

# Step 1: Decompose into Trend + Seasonality + Residual
result = seasonal_decompose(ts, model="additive", period=12)  # period=12 for monthly data
result.plot()                          # visualise all 4 components on one figure
plt.show()                             # display the plot

# Step 2: ACF and PACF — used to choose ARIMA (p, q) orders
plot_acf(ts, lags=40)                  # ACF lag where it cuts off → MA(q) order
plot_pacf(ts, lags=40)                 # PACF lag where it cuts off → AR(p) order
plt.show()

# Step 3: ADF test for stationarity (H0: series has a unit root = non-stationary)
result_adf = adfuller(ts)
print(f"ADF Statistic: {result_adf[0]:.4f}")  # more negative = more evidence of stationarity
print(f"p-value: {result_adf[1]:.4f}")         # p &lt; 0.05: reject H0 → series IS stationary
# p &gt; 0.05: cannot reject H0 → series is NON-stationary → must difference before ARIMA

# Step 4: Differencing to achieve stationarity
ts_diff  = ts.diff().dropna()          # first difference: ts[t] - ts[t-1]; removes linear trend
ts_diff2 = ts.diff().diff().dropna()   # second difference: removes quadratic trend (rare)

# Step 5: Log transform (use when variance grows with level — multiplicative seasonality)
ts_log      = np.log(ts)               # log stabilises variance; must be positive values
ts_log_diff = ts_log.diff().dropna()   # log + diff: the most common fix for non-stationary TS
</pre></div>'''
)

# Block 2: ARIMA
html = html.replace(
    '''<div class="code-block"><pre>from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings("ignore")

# ARIMA(p, d, q)
# p = AR order: how many past values to use (from PACF)
# d = differencing order: how many times to difference for stationarity
# q = MA order: how many past errors to use (from ACF)

model = ARIMA(train, order=(2, 1, 2))
result = model.fit()
print(result.summary())

forecast = result.forecast(steps=12)  # 12-step ahead forecast
conf_int = result.get_forecast(steps=12).conf_int()  # confidence interval

# SARIMA(p,d,q)(P,D,Q,m) — adds seasonal component
# m = seasonal period (12 for monthly, 7 for daily with weekly seasonality)
sarima = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12))
sarima_result = sarima.fit(disp=False)
forecast = sarima_result.forecast(steps=24)

# Auto-select ARIMA orders
from pmdarima import auto_arima
model = auto_arima(train, seasonal=True, m=12,
                   information_criterion="aic",
                   stepwise=True, suppress_warnings=True)
print(model.summary())
</pre></div>''',
    '''<div class="code-block"><pre>from statsmodels.tsa.arima.model import ARIMA      # classic ARIMA model
from statsmodels.tsa.statespace.sarimax import SARIMAX  # seasonal extension of ARIMA
import warnings
warnings.filterwarnings("ignore")                  # suppress convergence warnings during fit

# ARIMA(p, d, q) — three hyperparameters:
# p = autoregressive order: use last p values as predictors (from PACF plot cutoff)
# d = differencing order: how many times to diff to make series stationary (ADF test)
# q = moving average order: use last q forecast errors (from ACF plot cutoff)

model  = ARIMA(train, order=(2, 1, 2))  # AR(2): use 2 past values, d=1: one diff, MA(2): 2 errors
result = model.fit()                    # MLE parameter estimation
print(result.summary())                 # shows AIC, BIC, coefficients, p-values

forecast = result.forecast(steps=12)   # point forecast 12 steps ahead
conf_int = result.get_forecast(steps=12).conf_int()  # 95% confidence interval for each step

# SARIMA(p,d,q)(P,D,Q,m): adds a SEASONAL component on top of ARIMA
# P=seasonal AR, D=seasonal differencing, Q=seasonal MA, m=seasonal period
sarima        = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12))
# seasonal_order=(1,1,1,12): one seasonal AR, one seasonal diff, one seasonal MA, monthly (m=12)
sarima_result = sarima.fit(disp=False)    # disp=False: suppress iteration output
forecast      = sarima_result.forecast(steps=24)  # 2-year forecast

# Auto-select best ARIMA orders using grid search + AIC criterion
from pmdarima import auto_arima         # pip install pmdarima
model = auto_arima(train,
    seasonal=True,                      # consider seasonal component
    m=12,                               # monthly seasonality
    information_criterion="aic",        # pick model with lowest AIC (penalises complexity)
    stepwise=True,                      # stepwise search: faster than exhaustive grid
    suppress_warnings=True)             # clean output
print(model.summary())                  # shows chosen (p,d,q)(P,D,Q,m) and AIC
</pre></div>'''
)

print("p33 blocks done")

with open("KV_Ultimate_Guide.html", "w", encoding="utf-8") as f:
    f.write(html)

kb = len(html) / 1024
print(f"Saved — {kb:.0f} KB")
