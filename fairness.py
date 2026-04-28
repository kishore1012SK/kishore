from fairlearn.metrics import demographic_parity_difference
import numpy as np

def calculate_fairness(y_true, y_pred, sensitive):
    """
    Calculates the Demographic Parity Difference.
    Lower is better (closer to 0 is more fair).
    """
    try:
        dp = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive)
        return dp
    except Exception as e:
        return 0.0
