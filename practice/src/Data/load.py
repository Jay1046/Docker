import pandas as pd
from sklearn.datasets import load_iris

def load_data():
    X, y = load_iris(as_frame=True, return_X_y=True)
    
    return X, y