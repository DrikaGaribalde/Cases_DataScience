"""MMM simplificado: transforms (adstock/saturation), modelagem e decomposição.

"""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd

@dataclass(frozen=True)
class TransformParams:
    decay: float
    alpha: float
    gamma: float

def adstock(x: np.ndarray, decay: float) -> np.ndarray:
    """Adstock recursivo: efeito carregado no tempo.
    decay em [0,1)."""
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    carry = 0.0
    for i, v in enumerate(x):
        carry = v + decay * carry
        out[i] = carry
    return out

def hill(x: np.ndarray, alpha: float, gamma: float) -> np.ndarray:
    """Curva de saturação (Hill): retorna valores em (0,1)."""
    x = np.asarray(x, dtype=float)
    return (x**alpha) / (x**alpha + gamma**alpha + 1e-12)

def apply_transform(series: pd.Series, params: TransformParams) -> pd.Series:
    """Aplica adstock + saturação em uma série de gastos."""
    x = series.to_numpy(dtype=float)
    return pd.Series(hill(adstock(x, params.decay), params.alpha, params.gamma), index=series.index)

def build_design_matrix(df: pd.DataFrame, channel_params: dict[str, TransformParams]) -> tuple[pd.DataFrame, list[str]]:
    """Cria matriz X com canais transformados + controles.
    Retorna (X, feature_names)."""
    X = pd.DataFrame(index=df.index)
    feature_names = []

    for ch, p in channel_params.items():
        col = f"{ch}_transformed"
        X[col] = apply_transform(df[ch], p)
        feature_names.append(col)

    # controles típicos
    X["price_index"] = df["price_index"].astype(float)
    X["promo"] = df["promo"].astype(int)
    feature_names += ["price_index", "promo"]
    return X, feature_names

def train_linear_model(X: pd.DataFrame, y: pd.Series):
    """Treina regressão linear via statsmodels (com intercepto) para ter sumário e p-values."""
    import statsmodels.api as sm
    Xc = sm.add_constant(X, has_constant='add')
    model = sm.OLS(y, Xc).fit()
    return model

def decompose_contributions(model, X: pd.DataFrame) -> pd.DataFrame:
    """Decompõe a predição em contribuições por feature e intercepto."""
    import numpy as np
    import pandas as pd
    params = model.params
    Xc = X.copy()
    Xc = Xc.assign(constant=1.0)
    # alinhar ordem
    cols = [c for c in params.index if c != 'const']
    contrib = pd.DataFrame(index=X.index)
    contrib["intercept"] = params.get("const", 0.0)
    for c in cols:
        if c in X.columns:
            contrib[c] = X[c] * params[c]
    contrib["prediction"] = contrib.sum(axis=1)
    return contrib

def simple_budget_simulation(model, base_row: pd.Series, channel_cols: list[str], deltas: dict[str, float]) -> float:
    """Simula mudança de orçamento em features já transformadas.
    deltas: ex {"tv_transformed": +0.02}.
    Retorna delta de vendas prevista."""
    import numpy as np
    params = model.params
    before = params.get("const", 0.0) + float(np.dot(base_row[channel_cols], params[channel_cols]))
    after_row = base_row.copy()
    for k, v in deltas.items():
        after_row[k] = float(after_row[k] + v)
    after = params.get("const", 0.0) + float(np.dot(after_row[channel_cols], params[channel_cols]))
    return after - before
