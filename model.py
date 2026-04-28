from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

def train_model(df, target):
    # Filter numeric columns for simplicity in this MVP
    X = df.drop(columns=[target]).select_dtypes(include=[np.number])
    y = df[target]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, X, y

def predict(model, input_data):
    df_input = pd.DataFrame([input_data])
    return model.predict(df_input)[0]
