import pandas as pd
from hmmlearn import hmm


def hmm_predict(df, x, n_components=3, covariance_type="diag", n_iter=50, random_state=42):
    X = df[[x]].values
    model = hmm.GaussianHMM(
        n_components=n_components,
        covariance_type=covariance_type,
        n_iter=n_iter,
        random_state=random_state
    )
    model.fit(X)
    Z = model.predict(X)
    states = pd.unique(Z)
    return Z, states, model

